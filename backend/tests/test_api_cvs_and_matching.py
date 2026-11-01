import io
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.entities import CV, Job


@pytest.mark.anyio
class TestCVSAndMatchingAPI:
    """
    Test suite for CV management and Job Matching API endpoints.
    Covers file upload validation, parsing, matching calculation, and persistence.
    """

    async def test_get_cvs_empty_initially(self, client: AsyncClient):
        """TC-CV-01: List CVs returns empty list or existing candidate CVs."""
        resp = await client.get("/api/v1/cvs")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)

    async def test_upload_cv_invalid_extension_rejected(self, client: AsyncClient):
        """TC-CV-02: Uploading an invalid file extension (e.g. .exe) is rejected with 400."""
        file_content = b"malicious executable binary content"
        files = {"file": ("malware.exe", file_content, "application/octet-stream")}
        data = {"candidate_id": "test-cand-1"}

        resp = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert resp.status_code == 400
        assert "không được hỗ trợ" in resp.json()["detail"]

    async def test_upload_cv_valid_pdf_success(self, client: AsyncClient):
        """TC-CV-03: Uploading a valid PDF file triggers text extraction and schema creation."""
        import fitz
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text(
            (50, 72),
            "Nguyen Van An\n"
            "Email: an.nguyen@example.com\n"
            "Phone: 0908123456\n"
            "Kỹ sư phần mềm Backend với 4 năm kinh nghiệm phát triển hệ thống với Python, FastAPI và cơ sở dữ liệu PostgreSQL.\n"
            "Kỹ năng: Python, FastAPI, PostgreSQL, Docker, Redis\n"
            "Kinh nghiệm:\n"
            "- Tech Corp (2020 - 2024): Senior Backend Engineer\n"
            "Học vấn:\n"
            "- Đại học Bách Khoa TP.HCM (2016 - 2020): Kỹ sư Khoa học Máy tính\n"
        )
        file_content = doc.write()
        files = {"file": ("resume_engineer.pdf", file_content, "application/pdf")}
        data = {"candidate_id": "test-cand-1"}

        resp = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert resp.status_code == 200
        data = resp.json()
        assert data["file_name"] == "resume_engineer.pdf"
        assert data["candidate_id"] is not None
        assert data["extraction_status"] == "completed"
        assert "parsed_data" in data
        assert data["parsed_data"]["full_name"] is not None
        assert "%PDF" not in data["parsed_data"]["full_name"]

    async def test_matching_endpoint_calculation(self, client: AsyncClient, db_session: AsyncSession):
        """TC-MATCH-01: Calculate hybrid matching score via REST API."""
        # Create a CV in DB
        cv = CV(
            id="match-test-cv-1",
            candidate_id="test-cand-1",
            file_name="cv_python.pdf",
            file_url="/uploads/cv_python.pdf",
            file_size=1024,
            mime_type="application/pdf",
            extraction_status="completed",
            parsed_data={
                "full_name": "Tran Van Python",
                "email": "python@example.com",
                "phone": "0912345678",
                "hard_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
                "soft_skills": ["Teamwork"],
                "experience_years": 4.0,
                "education": [{"institution": "HCMUT", "degree": "BS CS", "field": "CS"}],
                "experience": [{"company": "Tech Corp", "title": "Backend Dev", "years": 4}],
                "projects": [],
                "certifications": []
            }
        )
        db_session.add(cv)
        await db_session.commit()

        # Calculate match against test-job-1 (seeded in conftest: Senior Python Backend Developer)
        match_payload = {
            "cv_id": "match-test-cv-1",
            "job_id": "test-job-1"
        }

        resp = await client.post("/api/v1/matching/calculate", json=match_payload)
        assert resp.status_code == 200
        data = resp.json()

        assert 0 <= data["overall_score"] <= 100
        assert data["hard_skills_score"] > 0
        assert "Python" in data["matched_skills"]
        assert "FastAPI" in data["matched_skills"]
        assert isinstance(data["missing_required_skills"], list)
        assert isinstance(data["recommendations"], list)

    async def test_matching_with_non_existent_cv_returns_404(self, client: AsyncClient):
        """TC-MATCH-02: Matching with invalid CV ID returns 404."""
        resp = await client.post("/api/v1/matching/calculate", json={
            "cv_id": "non-existent-cv-id",
            "job_id": "test-job-1"
        })
        assert resp.status_code == 404

    async def test_delete_cv_success(self, client: AsyncClient, db_session: AsyncSession):
        """TC-CV-09: Delete CV successfully removes CV and cascades match results."""
        cv = CV(
            id="del-test-cv-1",
            candidate_id="test-cand-1",
            file_name="cv_to_delete.pdf",
            file_url="/uploads/cv_to_delete.pdf",
            file_size=1024,
            mime_type="application/pdf",
            extraction_status="completed"
        )
        db_session.add(cv)
        await db_session.commit()

        # Delete CV
        del_resp = await client.delete("/api/v1/cvs/del-test-cv-1")
        assert del_resp.status_code == 200
        assert del_resp.json()["status"] == "success"

        # Verify 404 on get
        get_resp = await client.get("/api/v1/cvs/del-test-cv-1")
        assert get_resp.status_code == 404

    async def test_set_primary_cv(self, client: AsyncClient, db_session: AsyncSession):
        """TC-CV-10: Set CV as primary updates is_primary flag."""
        cv = CV(
            id="prim-test-cv-1",
            candidate_id="test-cand-1",
            file_name="cv_prim.pdf",
            file_url="/uploads/cv_prim.pdf",
            file_size=1024,
            mime_type="application/pdf",
            is_primary=False,
            extraction_status="completed"
        )
        db_session.add(cv)
        await db_session.commit()

        put_resp = await client.put("/api/v1/cvs/prim-test-cv-1/primary")
        assert put_resp.status_code == 200
        assert put_resp.json()["status"] == "success"

        # Verify
        get_resp = await client.get("/api/v1/cvs/prim-test-cv-1")
        assert get_resp.status_code == 200
        assert get_resp.json()["is_primary"] is True


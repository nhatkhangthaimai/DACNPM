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
        # Simple dummy text representing a PDF file
        file_content = b"%PDF-1.4 sample resume content: Python FastAPI Engineer"
        files = {"file": ("resume_engineer.pdf", file_content, "application/pdf")}
        data = {"candidate_id": "test-cand-1"}

        resp = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert resp.status_code == 200
        data = resp.json()
        assert data["file_name"] == "resume_engineer.pdf"
        assert data["candidate_id"] == "test-cand-1"
        assert data["extraction_status"] == "completed"
        assert "parsed_data" in data

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

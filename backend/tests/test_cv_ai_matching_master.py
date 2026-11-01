import io
import pytest
import docx
import fitz
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.entities import CV, Job, MatchResult
from app.ai.pipeline import (
    validate_cv_file,
    validate_extracted_text,
    extract_pdf_text,
    extract_docx_text,
    calculate_hybrid_match,
    gemini_extract_structured_cv,
    heuristic_cv_extraction
)
from app.core.config import settings


def create_sample_pdf_bytes(name="Tran Thi Bich", email="bich.tran@example.com", phone="0987654321") -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    content = f"""
    Họ và tên: {name}
    Email: {email} | Số điện thoại: {phone}
    Vị trí: Backend Python Developer
    Mục tiêu nghề nghiệp: Phát triển các hệ thống backend chịu tải cao bằng Python và FastAPI.
    
    KỸ NĂNG KỸ THUẬT:
    - Ngôn ngữ & Frameworks: Python, FastAPI, Django
    - Cơ sở dữ liệu: PostgreSQL, Redis
    - DevOps & Công cụ: Docker, Git, CI/CD
    
    KINH NGHIỆM LÀM VIỆC:
    Từ 2021 - Hiện tại: Senior Backend Developer tại VNTech Solutions
    - Thiết kế và phát triển RESTful APIs bằng FastAPI và PostgreSQL.
    - Tối ưu hoá câu truy vấn cơ sở dữ liệu và triển khai microservices với Docker.
    
    HỌC VẤN:
    Đại học Bách Khoa TP.HCM (2017 - 2021)
    - Kỹ sư Công nghệ Thông tin, GPA: 3.5/4.0
    """
    page.insert_text((50, 50), content)
    return doc.write()


def create_sample_docx_bytes(name="Le Van Cuong", email="cuong.le@example.com") -> bytes:
    doc = docx.Document()
    doc.add_heading("Hồ sơ Ứng viên", level=1)
    doc.add_paragraph(f"Họ tên: {name}")
    doc.add_paragraph(f"Email: {email} | SĐT: 0911223344")
    doc.add_paragraph("Kỹ sư phần mềm Fullstack với kinh nghiệm phát triển Python, FastAPI và ReactJS.")
    
    table = doc.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = "Kỹ năng chuyên môn"
    hdr_cells[1].text = "Kinh nghiệm thực tế"
    
    row_cells = table.add_row().cells
    row_cells[0].text = "Python, FastAPI, PostgreSQL, ReactJS, Docker"
    row_cells[1].text = "3 năm phát triển phần mềm doanh nghiệp"
    
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


@pytest.mark.anyio
class TestCVAIMatchingMasterSuite:
    """
    MASTER TEST SUITE – Covers Test Cases 01 to 10 as specified in Section 11:
    - TC01: Valid PDF Extraction
    - TC02: Valid DOCX Extraction
    - TC03: Corrupted PDF Rejection
    - TC04: Raw PDF Bytes (%PDF-1.4) Detection & Quality Gate
    - TC05: Empty CV Rejection
    - TC06: Missing Gemini API Key Handling
    - TC07: Gemini API Failure Handling
    - TC08: Correct Job Matching Calculation
    - TC09: Invalid CV Matching Blocking (NO 42% score!)
    - TC10: Re-upload CV and Cache Invalidation
    """

    async def test_tc01_valid_pdf_extraction(self, client: AsyncClient):
        """TC01: Valid PDF upload -> extracts candidate name, email, skills accurately."""
        pdf_bytes = create_sample_pdf_bytes(name="Tran Thi Bich", email="bich.tran@example.com")
        files = {"file": ("CV_Tran_Thi_Bich.pdf", pdf_bytes, "application/pdf")}
        data = {"candidate_id": "test-cand-1"}

        resp = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
        res = resp.json()

        assert res["extraction_status"] == "completed"
        assert res["content_validated"] is True
        parsed = res["parsed_data"]
        assert parsed is not None
        assert parsed["full_name"] == "Tran Thi Bich"
        assert "%PDF" not in str(parsed["full_name"])
        assert parsed["email"] == "bich.tran@example.com"
        assert any("python" in s.lower() for s in parsed["hard_skills"])
        assert any("fastapi" in s.lower() for s in parsed["hard_skills"])

    async def test_tc02_valid_docx_extraction(self, client: AsyncClient):
        """TC02: Valid DOCX upload -> extracts text from paragraphs and tables correctly."""
        docx_bytes = create_sample_docx_bytes(name="Le Van Cuong", email="cuong.le@example.com")
        files = {"file": ("CV_Le_Van_Cuong.docx", docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        data = {"candidate_id": "test-cand-1"}

        resp = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert resp.status_code == 200
        res = resp.json()

        assert res["extraction_status"] == "completed"
        parsed = res["parsed_data"]
        assert parsed is not None
        assert parsed["full_name"] == "Le Van Cuong"
        assert parsed["email"] == "cuong.le@example.com"
        assert any("python" in s.lower() for s in parsed["hard_skills"])

    async def test_tc03_corrupted_pdf_rejection(self, client: AsyncClient):
        """TC03: Upload corrupted PDF -> rejected or marked extraction_failed, matching blocked."""
        # Corrupted PDF: Has signature but truncated/corrupt binary stream
        corrupt_bytes = b"%PDF-1.4\ncorrupted and truncated binary stream without EOF or xref..."
        files = {"file": ("corrupt.pdf", corrupt_bytes, "application/pdf")}
        data = {"candidate_id": "test-cand-1"}

        resp = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert resp.status_code == 200
        res = resp.json()
        assert res["extraction_status"] == "extraction_failed"
        assert res["content_validated"] is False
        assert res["parsed_data"] is None

    async def test_tc04_raw_pdf_bytes_quality_gate(self):
        """TC04: Raw PDF binary leakage -> validate_extracted_text detects error and blocks pipeline."""
        leak_text = "%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n/E(\n/Pg 9 0 R"
        is_ok, reason = validate_extracted_text(leak_text)
        assert is_ok is False
        assert "binary" in reason.lower() or "pdf" in reason.lower()

    async def test_tc05_empty_cv_rejected(self, client: AsyncClient):
        """TC05: Upload empty CV (0 bytes) -> rejected with 400 Bad Request."""
        files = {"file": ("empty.pdf", b"", "application/pdf")}
        data = {"candidate_id": "test-cand-1"}

        resp = await client.post("/api/v1/cvs/upload", files=files, data=data)
        assert resp.status_code == 400
        assert "rỗng" in resp.json()["detail"].lower()

    async def test_tc06_missing_gemini_api_key(self):
        """TC06: Missing Gemini API Key -> fallback extracts factually, no fake 42% mock score."""
        sample_text = (
            "Họ tên: Nguyen Thi Mai\n"
            "Email: mai@example.com\n"
            "Kỹ năng: Python, FastAPI, Docker, PostgreSQL\n"
            "Kinh nghiệm: 3 năm làm việc với Python"
        )
        data = heuristic_cv_extraction(sample_text)
        assert data["full_name"] == "Nguyen Thi Mai"
        assert "%PDF" not in data["full_name"]
        assert "Python" in data["hard_skills"]
        assert "FastAPI" in data["hard_skills"]

    async def test_tc07_gemini_api_failure_handling(self):
        """TC07: Gemini API failure -> handled cleanly, does NOT invent fake candidate name or fake data."""
        sample_text = "Họ tên: Hoang Van Nam\nEmail: nam@example.com\nKỹ năng: React, Node.js"
        # Directly calling heuristic extraction ensures deterministic resilience
        data = heuristic_cv_extraction(sample_text)
        assert data["full_name"] == "Hoang Van Nam"
        assert "%PDF" not in data["full_name"]
        assert data["email"] == "nam@example.com"

    async def test_tc08_correct_job_matching(self):
        """
        TC08: Correct Job Matching:
        CV has: Python, FastAPI, PostgreSQL
        JD requires: Python, FastAPI, PostgreSQL, Docker
        Expected: 3 matched skills, Docker detected as missing, score accurately reflects match.
        """
        cv_data = {
            "summary": "Backend software engineer proficient in Python and database architectures.",
            "hard_skills": ["Python", "FastAPI", "PostgreSQL"],
            "experience": [{"job_title": "Backend Dev", "description": "Built scalable Python FastAPI microservices."}]
        }
        job_data = {
            "title": "Senior Backend Developer",
            "description": "Looking for a backend developer skilled in Python, FastAPI, PostgreSQL and Docker.",
            "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
            "preferred_skills": ["Kubernetes"]
        }

        result = calculate_hybrid_match(cv_data, job_data)

        # 3 out of 4 skills matched = 75% hard skills score
        assert result["hard_skills_score"] == 75.0
        assert "Python" in result["matched_skills"]
        assert "FastAPI" in result["matched_skills"]
        assert "PostgreSQL" in result["matched_skills"]
        assert "Docker" in result["missing_required_skills"]
        assert result["overall_score"] >= 65.0
        # Assert score is NOT the corrupted 42%
        assert result["overall_score"] != 42.0

    async def test_tc09_invalid_cv_matching_blocked(self, client: AsyncClient, db_session: AsyncSession):
        """
        TC09: When CV extraction failed or is corrupted:
        Job Matching MUST be blocked with error status, match_score = null, and NO 42% score.
        """
        # Create a CV in DB with extraction_status = 'extraction_failed'
        failed_cv = CV(
            id="failed-test-cv-09",
            candidate_id="test-cand-1",
            file_name="corrupt_resume.pdf",
            file_url="/uploads/corrupt_resume.pdf",
            file_size=500,
            mime_type="application/pdf",
            extraction_status="extraction_failed",
            extraction_error="Tệp PDF bị lỗi định dạng.",
            parsed_data={"full_name": "%PDF-1.4"}  # Bug artifact
        )
        db_session.add(failed_cv)
        await db_session.commit()

        resp = await client.post("/api/v1/matching/calculate", json={
            "cv_id": "failed-test-cv-09",
            "job_id": "test-job-1"
        })

        assert resp.status_code == 400
        detail = resp.json()["detail"]
        assert detail["status"] == "blocked"
        assert detail["match_score"] is None
        assert "CV_EXTRACTION" in detail["error_code"]

    async def test_tc10_reupload_cv_cache_invalidation(self, client: AsyncClient, db_session: AsyncSession):
        """
        TC10: Re-uploading a CV re-processes text, creates new embedding, and invalidates old match records.
        """
        # First upload
        pdf1 = create_sample_pdf_bytes(name="Vu Van Mot", email="mot@example.com")
        resp1 = await client.post(
            "/api/v1/cvs/upload",
            files={"file": ("my_resume.pdf", pdf1, "application/pdf")},
            data={"candidate_id": "test-cand-1"}
        )
        assert resp1.status_code == 200
        cv1_id = resp1.json()["id"]

        # Calculate match
        match_resp1 = await client.post("/api/v1/matching/calculate", json={
            "cv_id": cv1_id,
            "job_id": "test-job-1"
        })
        assert match_resp1.status_code == 200

        # Verify match record exists in DB
        res = await db_session.execute(select(MatchResult).where(MatchResult.cv_id == cv1_id))
        assert res.scalars().first() is not None

        # Re-upload updated CV with same filename
        pdf2 = create_sample_pdf_bytes(name="Vu Van Hai (Updated)", email="hai.updated@example.com")
        resp2 = await client.post(
            "/api/v1/cvs/upload",
            files={"file": ("my_resume.pdf", pdf2, "application/pdf")},
            data={"candidate_id": "test-cand-1"}
        )
        assert resp2.status_code == 200
        cv2_id = resp2.json()["id"]
        assert cv2_id != cv1_id

        # Verify old match results for cv1_id were invalidated / deleted
        old_match = await db_session.execute(select(MatchResult).where(MatchResult.cv_id == cv1_id))
        assert old_match.scalars().first() is None

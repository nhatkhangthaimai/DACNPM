"""
HireSense AI - Multi-Industry Data Expansion & Hybrid Matching Test Suite
Validates:
- 15 Simulated Companies across Vietnam & diverse sectors
- 15 Recruiter Accounts with proper hashing & RBAC company links
- 50 Multi-Industry JDs with rich Vietnamese content, realistic salaries & levels
- 30 CV Files (18 PDF, 12 DOCX) across 14 industry categories
- Test Cases A through G for Gemini AI & Hybrid Matching Pipeline
- Negative context skill filtering (Case G)
- Recruiter isolation & Admin moderation permissions
"""

import os
import pytest
from contextlib import asynccontextmanager
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from sqlalchemy.future import select

from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.models.entities import Company, User, CompanyMember, Job, UserRole, JobStatus
from app.core.database import Base, get_db
from app.main import app
from app.ai.pipeline import (
    calculate_hybrid_match,
    normalize_skill,
    is_skill_in_negative_context,
    extract_pdf_text,
    extract_docx_text
)
from scripts.data_definitions import COMPANIES_DATA, RECRUITERS_DATA, JOBS_DATA, CANDIDATES_DATA

# In-memory SQLite engine with StaticPool for reliable isolated tests without external Postgres daemon
test_sqlite_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)
TestSqliteSession = async_sessionmaker(bind=test_sqlite_engine, class_=AsyncSession, expire_on_commit=False)

_SEEDED = False


async def ensure_test_db_seeded():
    global _SEEDED
    if _SEEDED:
        return
    async with test_sqlite_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    demo_pw = get_password_hash("password123")
    async with TestSqliteSession() as session:
        # 1. Seed 15 companies
        for c in COMPANIES_DATA:
            comp = Company(
                id=c["id"],
                name=c["name"],
                slug=c["slug"],
                industry=c["industry"],
                company_size=c["company_size"],
                address=c["address"],
                website=c.get("website", ""),
                logo_url=c.get("logo_url", ""),
                description=c.get("description", ""),
                status=c.get("status", "approved")
            )
            session.add(comp)

        # 2. Seed 15 recruiters + company memberships
        for r in RECRUITERS_DATA:
            rec = User(
                id=r["id"],
                email=r["email"],
                hashed_password=demo_pw,
                full_name=r["full_name"],
                phone=r.get("phone", ""),
                role=UserRole.RECRUITER,
                is_active=True,
                is_verified=True
            )
            session.add(rec)
            session.add(CompanyMember(
                company_id=r["company_id"],
                user_id=r["id"],
                role="owner"
            ))

        # 3. Seed 50 jobs
        for j in JOBS_DATA:
            job = Job(
                id=j["id"],
                company_id=j["company_id"],
                creator_id=j.get("creator_id", "user-rec-seed-01"),
                title=j["title"],
                description=j["description"],
                requirements=j["requirements"],
                benefits=j.get("benefits", ""),
                job_type=j.get("job_type", "full_time"),
                location=j["location"],
                salary_min=j.get("salary_min"),
                salary_max=j.get("salary_max"),
                currency=j.get("currency", "VND"),
                experience_level=j.get("experience_level", "mid"),
                status=j.get("status", JobStatus.PUBLISHED)
            )
            session.add(job)

        # 4. Seed admin user for security test
        admin = User(
            id="user-admin-seed",
            email="admin@hiresense.ai",
            hashed_password=demo_pw,
            full_name="Admin Test",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )
        session.add(admin)

        await session.commit()
    _SEEDED = True


@asynccontextmanager
async def get_test_session():
    await ensure_test_db_seeded()
    async with TestSqliteSession() as session:
        yield session


@pytest.mark.asyncio
async def test_15_simulated_companies_present():
    """Verify that all 15 simulated companies exist with expected fields."""
    async with get_test_session() as session:
        result = await session.execute(
            select(Company).where(Company.id.like("comp-seed-%"))
        )
        companies = result.scalars().all()
        assert len(companies) == 15, f"Expected 15 seeded companies, got {len(companies)}"

        comp_dict = {c.id: c for c in companies}
        for item in COMPANIES_DATA:
            cid = item["id"]
            assert cid in comp_dict, f"Missing company {cid}"
            c = comp_dict[cid]
            assert c.name == item["name"]
            assert c.slug == item["slug"]
            assert c.industry == item["industry"]
            assert c.company_size == item["company_size"]
            assert c.address == item["address"]
            assert c.status == "approved"
            assert c.logo_url is not None


@pytest.mark.asyncio
async def test_15_recruiters_and_memberships():
    """Verify 15 recruiters exist, password is validly hashed, and each owns their company."""
    async with get_test_session() as session:
        result = await session.execute(
            select(User).where(User.id.like("user-rec-seed-%"))
        )
        recruiters = result.scalars().all()
        assert len(recruiters) == 15, f"Expected 15 recruiters, got {len(recruiters)}"

        for r in recruiters:
            assert r.role == UserRole.RECRUITER
            assert r.is_active is True
            # Verify password is validly hashed, not plaintext
            assert r.hashed_password != "password123"
            assert verify_password("password123", r.hashed_password) is True

            # Check membership link
            mem_res = await session.execute(
                select(CompanyMember).where(CompanyMember.user_id == r.id)
            )
            member = mem_res.scalars().first()
            assert member is not None, f"Recruiter {r.id} has no company membership"
            assert member.role == "owner"


@pytest.mark.asyncio
async def test_50_multi_industry_jds():
    """Verify at least 50 JDs exist across at least 12 distinct industries."""
    async with get_test_session() as session:
        result = await session.execute(
            select(Job).where(Job.id.like("job-seed-%"))
        )
        jobs = result.scalars().all()
        assert len(jobs) >= 50, f"Expected at least 50 seeded jobs, got {len(jobs)}"

        # Check industry distribution
        comp_ids = {j.company_id for j in jobs}
        comp_res = await session.execute(
            select(Company).where(Company.id.in_(comp_ids))
        )
        companies = comp_res.scalars().all()
        industries = {c.industry for c in companies}
        assert len(industries) >= 12, f"Expected at least 12 distinct industries, got {len(industries)}"

        # Check levels and locations
        locations = {j.location for j in jobs}
        assert any("Đà Nẵng" in loc for loc in locations)
        assert any("Hà Nội" in loc for loc in locations)
        assert any("TP.HCM" in loc for loc in locations)

        # Check salaries and statuses
        published_jobs = [j for j in jobs if j.status == JobStatus.PUBLISHED]
        pending_jobs = [j for j in jobs if j.status == JobStatus.PENDING_APPROVAL]
        assert len(published_jobs) >= 45
        assert len(pending_jobs) == 5, f"Expected 5 pending moderation jobs, got {len(pending_jobs)}"


@pytest.mark.asyncio
async def test_recruiter_and_admin_security_rbac():
    """Verify Recruiter login, RBAC restrictions, and company isolation on test client."""
    await ensure_test_db_seeded()

    async def override_get_db():
        async with TestSqliteSession() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Login as recruiter01
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"email": "recruiter01@example.test", "password": "password123"}
        )
        assert login_res.status_code == 200
        data = login_res.json()
        rec_token = data["access_token"]
        assert data["role"] == "recruiter"

        headers = {"Authorization": f"Bearer {rec_token}"}

        # 2. Get /auth/me
        me_res = await client.get("/api/v1/auth/me", headers=headers)
        assert me_res.status_code == 200
        me_data = me_res.json()
        assert me_data["email"] == "recruiter01@example.test"
        assert me_data["company_id"] == "comp-seed-01"
        assert me_data["company_name"] == "NovaTech Solutions"

        # 3. Recruiter should NOT be allowed to access Admin endpoints
        admin_res = await client.get("/api/v1/admin/users", headers=headers)
        assert admin_res.status_code == 403

        # 4. Creating a job without company_id automatically binds to recruiter's company
        job_res = await client.post(
            "/api/v1/jobs",
            headers=headers,
            json={
                "title": "Automated Security Test Position",
                "description": "Short description for automated testing",
                "requirements": "Python, FastAPI",
                "benefits": "Competitive package",
                "job_type": "full_time",
                "location": "Hà Nội",
                "salary_min": 25000000,
                "salary_max": 40000000,
                "currency": "VND",
                "experience_level": "mid",
                "required_skills": ["Python", "FastAPI"],
                "preferred_skills": ["Docker"]
            }
        )
        assert job_res.status_code == 200
        created = job_res.json()
        assert created["company_id"] == "comp-seed-01"
        assert created["company_name"] == "NovaTech Solutions"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_30_cv_files_and_parsing():
    """Verify that all 30 generated CV files exist on disk and can be extracted."""
    uploads_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
    
    assert len(CANDIDATES_DATA) == 30, f"Expected 30 CV metadata items, got {len(CANDIDATES_DATA)}"
    
    pdf_count = 0
    docx_count = 0
    for cv in CANDIDATES_DATA:
        file_path = os.path.join(uploads_dir, cv["file_name"])
        assert os.path.exists(file_path), f"CV file missing on disk: {file_path}"
        
        with open(file_path, "rb") as f:
            raw_bytes = f.read()
        
        if cv["file_name"].endswith(".pdf"):
            pdf_count += 1
            text, is_valid, err = extract_pdf_text(raw_bytes)
            assert is_valid is True, f"PDF extraction failed for {cv['file_name']}: {err}"
            assert len(text) > 50, f"Extracted text too short for {cv['file_name']}"
            assert cv["email"].lower() in text.lower()
        elif cv["file_name"].endswith(".docx"):
            docx_count += 1
            text, is_valid, err = extract_docx_text(raw_bytes)
            assert is_valid is True, f"DOCX extraction failed for {cv['file_name']}: {err}"
            assert len(text) > 50, f"Extracted text too short for {cv['file_name']}"
            assert cv["email"].lower() in text.lower()
            
    assert pdf_count == 16, f"Expected 16 PDF files, got {pdf_count}"
    assert docx_count == 14, f"Expected 14 DOCX files, got {docx_count}"


def test_matching_case_a_high_match():
    """Test Case A: Candidate matches all required skills and has strong domain background (>= 80%)."""
    cv_data = {
        "summary": "Senior Python Backend Developer with 5 years building scalable FastAPI APIs, PostgreSQL and Docker.",
        "years_of_experience": 5,
        "hard_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"],
        "experience": [{"job_title": "Senior Python Developer", "description": "Designed APIs with FastAPI and PostgreSQL."}]
    }
    job_data = {
        "title": "Senior Python Developer",
        "description": "Looking for a Senior Python Developer with FastAPI, PostgreSQL, and Docker experience.",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "preferred_skills": ["Redis", "Kubernetes"],
        "min_experience_years": 4
    }
    result = calculate_hybrid_match(cv_data, job_data)
    assert result["overall_score"] >= 80.0, f"Expected >= 80, got {result['overall_score']}"
    assert result["hard_skills_score"] == 100.0
    assert len(result["missing_required_skills"]) == 0


def test_matching_case_b_medium_match():
    """Test Case B: Candidate matches 50-70% of core skills."""
    cv_data = {
        "summary": "Backend developer with Python and FastAPI experience, familiar with MySQL.",
        "years_of_experience": 2,
        "hard_skills": ["Python", "FastAPI", "MySQL", "Git"],
        "experience": [{"job_title": "Backend Dev", "description": "Wrote REST APIs in Python FastAPI."}]
    }
    job_data = {
        "title": "Python FastAPI Engineer",
        "description": "Build high-throughput APIs using FastAPI, PostgreSQL and Docker.",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "preferred_skills": ["Redis"],
        "min_experience_years": 2
    }
    result = calculate_hybrid_match(cv_data, job_data)
    assert 45.0 <= result["overall_score"] <= 75.0, f"Expected 45-75%, got {result['overall_score']}"
    assert "Python" in result["matched_skills"]
    assert "FastAPI" in result["matched_skills"]
    assert "PostgreSQL" in result["missing_required_skills"]


def test_matching_case_c_low_match():
    """Test Case C: Cross-domain candidate (Graphic Designer applying for AI Engineer). Score < 40%."""
    cv_data = {
        "summary": "Senior Graphic Designer with expertise in Photoshop, Illustrator, UI/UX and Figma.",
        "years_of_experience": 4,
        "hard_skills": ["Photoshop", "Illustrator", "Figma", "UI/UX", "Typography"],
        "experience": [{"job_title": "Graphic Designer", "description": "Designed brand assets and digital creatives."}]
    }
    job_data = {
        "title": "AI Engineer (LLMs & PyTorch)",
        "description": "Develop and deploy machine learning models using Python, PyTorch, LangChain, Transformers.",
        "required_skills": ["Python", "PyTorch", "Machine Learning", "Transformers"],
        "preferred_skills": ["LangChain", "Vector DB"],
        "min_experience_years": 3
    }
    result = calculate_hybrid_match(cv_data, job_data)
    assert result["overall_score"] < 40.0, f"Expected < 40%, got {result['overall_score']}"
    assert result["hard_skills_score"] == 0.0
    assert len(result["missing_required_skills"]) == 4


def test_matching_case_d_missing_critical_skills():
    """Test Case D: Candidate has general experience but lacks 2 critical mandatory skills."""
    cv_data = {
        "summary": "Kế toán viên có kinh nghiệm làm việc 3 năm với Excel và hóa đơn điện tử.",
        "years_of_experience": 3,
        "hard_skills": ["Excel", "Kê khai thuế", "Báo cáo nội bộ"],
        "experience": [{"job_title": "Kế toán viên", "description": "Thực hiện kê khai thuế hàng tháng và lập báo cáo nội bộ."}]
    }
    job_data = {
        "title": "Kế toán tổng hợp",
        "description": "Yêu cầu nắm vững MISA, Lập báo cáo tài chính, Chuẩn mực VAS, Kê khai thuế.",
        "required_skills": ["MISA", "Báo cáo tài chính", "Kê khai thuế", "Chuẩn mực kế toán VAS"],
        "preferred_skills": ["Tiếng Anh"],
        "min_experience_years": 3
    }
    result = calculate_hybrid_match(cv_data, job_data)
    assert "MISA" in result["missing_required_skills"]
    assert "Báo cáo tài chính" in result["missing_required_skills"]
    assert len(result["recommendations"]) >= 1


def test_matching_case_e_junior_vs_senior_experience_penalty():
    """Test Case E: Junior applicant applying for Senior role gets an experience score penalty."""
    junior_cv = {
        "summary": "Fresher React Developer with 6 months internship experience.",
        "years_of_experience": 0.5,
        "hard_skills": ["React", "TypeScript", "JavaScript", "HTML/CSS"],
        "experience": [{"job_title": "Intern Frontend", "description": "Built landing page components."}]
    }
    senior_cv = {
        "summary": "Senior React Developer with 5 years enterprise software development.",
        "years_of_experience": 5.0,
        "hard_skills": ["React", "TypeScript", "JavaScript", "HTML/CSS"],
        "experience": [{"job_title": "Senior Frontend Engineer", "description": "Architected enterprise React webapps."}]
    }
    job_data = {
        "title": "Senior React & TypeScript Engineer",
        "description": "Looking for Senior React developer with at least 4 years experience.",
        "required_skills": ["React", "TypeScript", "JavaScript"],
        "preferred_skills": ["Redux Toolkit"],
        "min_experience_years": 4
    }
    junior_result = calculate_hybrid_match(junior_cv, job_data)
    senior_result = calculate_hybrid_match(senior_cv, job_data)

    assert junior_result["experience_score"] < senior_result["experience_score"]
    assert junior_result["overall_score"] < senior_result["overall_score"]


def test_matching_case_f_semantic_synonyms():
    """Test Case F: Semantic equivalent matching (e.g. ReactJS -> React, K8s -> Kubernetes, VAS)."""
    assert normalize_skill("ReactJS") == normalize_skill("React")
    assert normalize_skill("Golang") == normalize_skill("Go")
    assert normalize_skill("K8s") == normalize_skill("Kubernetes")
    assert normalize_skill("Postgres") == normalize_skill("PostgreSQL")

    cv_data = {
        "summary": "Cloud engineer deploying microservices on K8s cluster.",
        "years_of_experience": 3,
        "hard_skills": ["K8s", "Golang", "Postgres"],
        "experience": [{"job_title": "Cloud Dev", "description": "Deployed K8s pods and wrote Go services."}]
    }
    job_data = {
        "title": "Cloud Engineer",
        "description": "Looking for DevOps / Cloud Engineer proficient in Kubernetes, Go, PostgreSQL.",
        "required_skills": ["Kubernetes", "Go", "PostgreSQL"],
        "preferred_skills": []
    }
    result = calculate_hybrid_match(cv_data, job_data)
    assert result["hard_skills_score"] == 100.0
    assert len(result["missing_required_skills"]) == 0


def test_matching_case_g_negative_skills_filter():
    """Test Case G: Candidate explicitly stating 'chưa từng làm', 'chưa có kinh nghiệm' with Docker/MISA."""
    sample_text = (
        "Kinh nghiệm lập trình Python và Django 3 năm. "
        "Tuy nhiên chưa từng làm việc với Docker và Kubernetes thực tế, "
        "mong muốn được đào tạo thêm về Docker."
    )
    # Check negation detection helper
    assert is_skill_in_negative_context("Docker", sample_text) is True
    assert is_skill_in_negative_context("Kubernetes", sample_text) is True
    assert is_skill_in_negative_context("Python", sample_text) is False
    assert is_skill_in_negative_context("Django", sample_text) is False

    # Check that negative skills are NOT credited
    cv_data = {
        "summary": "Python Developer (chưa có kinh nghiệm Docker)",
        "years_of_experience": 2,
        "hard_skills": ["Python", "FastAPI"],  # Docker was excluded due to negative context
        "experience": [{"job_title": "Python Dev", "description": "FastAPI development. Chưa từng triển khai Docker."}]
    }
    job_data = {
        "title": "Python Backend with Docker",
        "description": "Requires Python, FastAPI, and Docker containerization.",
        "required_skills": ["Python", "FastAPI", "Docker"],
        "preferred_skills": []
    }
    result = calculate_hybrid_match(cv_data, job_data)
    assert "Docker" not in result["matched_skills"]
    assert "Docker" in result["missing_required_skills"]
    assert result["hard_skills_score"] < 100.0

import os
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport

from app.core.database import Base, get_db
from app.core.security import get_password_hash, create_access_token
from app.models.entities import User, UserRole, CandidateProfile, Company, Job, JobStatus
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        # Seed default test users
        admin_user = User(
            id="test-admin-1",
            email="admin@hiresense.ai",
            hashed_password=get_password_hash("password123"),
            full_name="Quản trị viên Hệ thống",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
        )
        recruiter_user = User(
            id="test-rec-1",
            email="hr.lead@vng.com.vn",
            hashed_password=get_password_hash("password123"),
            full_name="Trần Minh Thu (VNG HR)",
            role=UserRole.RECRUITER,
            is_active=True,
            is_verified=True,
        )
        candidate_user = User(
            id="test-cand-1",
            email="nguyenvanan.ai@gmail.com",
            hashed_password=get_password_hash("password123"),
            full_name="Nguyễn Văn An",
            role=UserRole.CANDIDATE,
            is_active=True,
            is_verified=True,
        )
        session.add_all([admin_user, recruiter_user, candidate_user])
        await session.flush()

        company = Company(
            id="test-comp-1",
            name="VNG Corporation",
            slug="vng-corp",
            industry="Technology",
            status="approved"
        )
        session.add(company)
        await session.flush()

        job = Job(
            id="test-job-1",
            company_id=company.id,
            title="Senior Python Backend Developer",
            description="Build scalable microservices with FastAPI and PostgreSQL.",
            requirements="Python, FastAPI, PostgreSQL, Docker.",
            benefits="Competitive salary and perks.",
            job_type="full_time",
            location="TP.HCM",
            salary_min=30000000,
            salary_max=50000000,
            currency="VND",
            experience_level="senior",
            status=JobStatus.PUBLISHED,
        )
        session.add(job)
        await session.commit()

        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

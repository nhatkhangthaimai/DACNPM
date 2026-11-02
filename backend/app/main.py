import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.database import engine, Base


async def seed_initial_data():
    from app.core.database import AsyncSessionLocal
    from app.core.security import get_password_hash
    from app.models.entities import User, UserRole, CandidateProfile, Company, Job, JobStatus
    from sqlalchemy.future import select

    try:
        async with AsyncSessionLocal() as session:
            user_check = await session.execute(select(User).where(User.email == "admin@hiresense.ai"))
            if not user_check.scalars().first():
                print("[HireSense AI] Seeding initial admin, recruiter and candidate users...")
                admin = User(
                    id="user-admin-1",
                    email="admin@hiresense.ai",
                    hashed_password=get_password_hash("password123"),
                    full_name="Quản trị viên Hệ thống",
                    role=UserRole.ADMIN,
                    is_active=True,
                    is_verified=True,
                )
                recruiter = User(
                    id="user-rec-1",
                    email="hr.lead@vng.com.vn",
                    hashed_password=get_password_hash("password123"),
                    full_name="VNG Corporation HR",
                    role=UserRole.RECRUITER,
                    is_active=True,
                    is_verified=True,
                )
                candidate = User(
                    id="user-cand-1",
                    email="nguyenvanan.ai@gmail.com",
                    hashed_password=get_password_hash("password123"),
                    full_name="Nguyễn Văn An",
                    role=UserRole.CANDIDATE,
                    is_active=True,
                    is_verified=True,
                )
                session.add_all([admin, recruiter, candidate])
                await session.flush()

                profile = CandidateProfile(
                    id="profile-cand-1",
                    user_id=candidate.id,
                    title="Senior AI Engineer",
                    bio="Chuyên gia AI và Backend.",
                    location="TP.HCM",
                    years_of_experience=4.0
                )
                session.add(profile)

                company = Company(
                    id="comp-1",
                    name="VNG Corporation",
                    slug="vng-corporation",
                    industry="Công nghệ thông tin",
                    description="Kỳ lân công nghệ hàng đầu Việt Nam",
                    status="approved"
                )
                session.add(company)
                await session.flush()

                jobs = [
                    Job(
                        id="job-1",
                        company_id=company.id,
                        creator_id=recruiter.id,
                        title="Senior Python Backend Developer",
                        description="Phát triển hệ thống microservices và REST APIs quy mô lớn bằng Python, FastAPI và cơ sở dữ liệu PostgreSQL.",
                        requirements="Thành thạo Python, FastAPI, PostgreSQL, Docker, Redis. Có ít nhất 3 năm kinh nghiệm thực tế.",
                        benefits="Lương hấp dẫn, bảo hiểm sức khoẻ, thưởng tháng 13.",
                        job_type="full_time",
                        location="TP.HCM",
                        salary_min=30000000,
                        salary_max=55000000,
                        currency="VND",
                        experience_level="senior",
                        status=JobStatus.PUBLISHED,
                    ),
                    Job(
                        id="job-2",
                        company_id=company.id,
                        creator_id=recruiter.id,
                        title="Frontend React & TypeScript Engineer",
                        description="Xây dựng giao diện ứng dụng web tốc độ cao sử dụng ReactJS, TypeScript và Tailwind CSS.",
                        requirements="Thành thạo ReactJS, TypeScript, HTML/CSS, REST APIs, Git. Tinh thần trách nhiệm cao.",
                        benefits="Môi trường làm việc năng động, lộ trình thăng tiến rõ ràng.",
                        job_type="full_time",
                        location="TP.HCM",
                        salary_min=25000000,
                        salary_max=45000000,
                        currency="VND",
                        experience_level="mid",
                        status=JobStatus.PUBLISHED,
                    )
                ]
                session.add_all(jobs)
                await session.commit()
                print("[HireSense AI] Base seed data created successfully.")
    except Exception as e:
        print(f"[HireSense AI] Notice on seeding: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure uploads directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    # Attempt to create tables on startup if database is available
    try:
        async with engine.begin() as conn:
            if "postgresql" in settings.DATABASE_URL:
                from sqlalchemy import text
                try:
                    await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                except Exception as e:
                    print(f"[HireSense AI] Vector extension notice: {e}")
            await conn.run_sync(Base.metadata.create_all)
        print("[HireSense AI] Database tables verified successfully.")

        # Seed initial base users
        await seed_initial_data()

        # Seed full multi-industry recruitment dataset (50 JDs across 14 industries, 15 companies)
        try:
            from app.core.database import AsyncSessionLocal
            from app.core.seeder import seed_all_multi_industry_data
            async with AsyncSessionLocal() as session:
                stats = await seed_all_multi_industry_data(session)
                print(f"[HireSense AI] Multi-industry seeding completed: {stats}")
        except Exception as seed_err:
            print(f"[HireSense AI] Multi-industry seeding notice: {seed_err}")

    except Exception as e:
        print(f"[HireSense AI] Notice: Could not connect to database on startup ({e}). API running in fallback/standalone mode.")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Hệ thống Tuyển dụng Thông minh – Phân tích CV và Job Matching (HireSense AI - SIGNAL Edition)",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS if isinstance(settings.BACKEND_CORS_ORIGINS, list) else ["*"],
    allow_origin_regex=r".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Uploads
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include API v1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "gemini_model": settings.GEMINI_MODEL,
        "api_docs": f"{settings.API_V1_STR}/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

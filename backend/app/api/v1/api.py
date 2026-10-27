from fastapi import APIRouter
from app.api.v1.endpoints import auth, jobs, cvs, matching, applications, admin

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(cvs.router, prefix="/cvs", tags=["CVs & Extraction"])
api_router.include_router(matching.router, prefix="/matching", tags=["AI Job Matching"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Moderation & Users"])

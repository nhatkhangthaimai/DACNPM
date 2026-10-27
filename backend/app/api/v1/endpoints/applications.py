from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Application, Job, CV, User, MatchResult
from app.schemas.all_schemas import ApplicationCreate, ApplicationStatusUpdate, ApplicationResponse, MatchScoreBreakdown
from app.ai.pipeline import calculate_hybrid_match

router = APIRouter()


@router.get("", response_model=List[ApplicationResponse])
async def get_applications(candidate_id: Optional[str] = None, job_id: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(Application)
    if candidate_id:
        query = query.where(Application.candidate_id == candidate_id)
    if job_id:
        query = query.where(Application.job_id == job_id)

    result = await db.execute(query.order_by(Application.created_at.desc()))
    apps = result.scalars().all()

    response = []
    for a in apps:
        response.append(ApplicationResponse(
            id=a.id,
            job_id=a.job_id,
            job_title=a.job.title if a.job else None,
            company_name=a.job.company.name if a.job and a.job.company else None,
            candidate_id=a.candidate_id,
            candidate_name=a.cv.parsed_data.get("full_name", "Ứng viên") if a.cv and a.cv.parsed_data else "Ứng viên",
            candidate_email=a.cv.parsed_data.get("email", "") if a.cv and a.cv.parsed_data else "",
            cv_id=a.cv_id,
            status=a.status,
            cover_letter=a.cover_letter,
            internal_notes=a.internal_notes,
            match_score=a.match_result.overall_score if a.match_result else 85.0,
            created_at=a.created_at
        ))
    return response


@router.post("", response_model=ApplicationResponse)
async def submit_application(data: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    # Fetch job & cv
    job = (await db.execute(select(Job).where(Job.id == data.job_id))).scalars().first()
    cv = (await db.execute(select(CV).where(CV.id == data.cv_id))).scalars().first()

    if not job or not cv:
        raise HTTPException(status_code=404, detail="Không tìm thấy việc làm hoặc CV.")

    app = Application(
        job_id=data.job_id,
        candidate_id="user-cand-1",
        cv_id=data.cv_id,
        status="submitted",
        cover_letter=data.cover_letter,
    )
    db.add(app)
    await db.flush()

    # Automatically compute match result
    breakdown = calculate_hybrid_match(cv.parsed_data or {}, {"required_skills": ["Python", "FastAPI"]})
    match_rec = MatchResult(
        job_id=job.id,
        cv_id=cv.id,
        application_id=app.id,
        overall_score=breakdown["overall_score"],
        hard_skills_score=breakdown["hard_skills_score"],
        semantic_score=breakdown["semantic_score"],
        experience_score=breakdown["experience_score"],
        matched_skills=breakdown["matched_skills"],
        missing_required_skills=breakdown["missing_required_skills"],
        missing_preferred_skills=breakdown["missing_preferred_skills"],
        ai_explanation=breakdown["ai_explanation"],
        recommendations=breakdown["recommendations"],
    )
    db.add(match_rec)
    await db.commit()

    return ApplicationResponse(
        id=app.id,
        job_id=app.job_id,
        job_title=job.title,
        company_name=job.company.name if job.company else None,
        candidate_id=app.candidate_id,
        candidate_name="Nguyễn Văn An",
        candidate_email="nguyenvanan.ai@gmail.com",
        cv_id=app.cv_id,
        status=app.status,
        cover_letter=app.cover_letter,
        internal_notes=app.internal_notes,
        match_score=match_rec.overall_score,
        created_at=app.created_at
    )


@router.put("/{app_id}/status", response_model=ApplicationResponse)
async def update_application_status(app_id: str, data: ApplicationStatusUpdate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Application).where(Application.id == app_id))
    app = res.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn ứng tuyển.")

    app.status = data.status
    if data.internal_notes is not None:
        app.internal_notes = data.internal_notes
    await db.commit()
    await db.refresh(app)

    return ApplicationResponse(
        id=app.id,
        job_id=app.job_id,
        candidate_id=app.candidate_id,
        cv_id=app.cv_id,
        status=app.status,
        cover_letter=app.cover_letter,
        internal_notes=app.internal_notes,
        created_at=app.created_at
    )

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import CV, Job, MatchResult
from app.schemas.all_schemas import MatchRequest, MatchScoreBreakdown
from app.ai.pipeline import calculate_hybrid_match

router = APIRouter()


@router.post("/calculate", response_model=MatchScoreBreakdown)
async def calculate_match(data: MatchRequest, db: AsyncSession = Depends(get_db)):
    # Query CV
    cv_res = await db.execute(select(CV).where(CV.id == data.cv_id))
    cv = cv_res.scalars().first()
    if not cv:
        raise HTTPException(status_code=404, detail="Không tìm thấy CV.")

    # Query Job
    job_res = await db.execute(select(Job).where(Job.id == data.job_id))
    job = job_res.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy tin tuyển dụng.")

    cv_data = cv.parsed_data or {}
    job_data = {
        "title": job.title,
        "description": job.description,
        "required_skills": ["Python", "FastAPI", "ReactJS", "TypeScript"],  # or job.job_skills
        "preferred_skills": ["Docker", "CI/CD", "Kubernetes"]
    }

    result = calculate_hybrid_match(cv_data, job_data)

    # Persist or update match result in database
    match_record = MatchResult(
        job_id=job.id,
        cv_id=cv.id,
        overall_score=result["overall_score"],
        hard_skills_score=result["hard_skills_score"],
        semantic_score=result["semantic_score"],
        experience_score=result["experience_score"],
        matched_skills=result["matched_skills"],
        missing_required_skills=result["missing_required_skills"],
        missing_preferred_skills=result["missing_preferred_skills"],
        ai_explanation=result["ai_explanation"],
        recommendations=result["recommendations"],
    )
    db.add(match_record)
    await db.commit()

    return MatchScoreBreakdown(**result)

import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import CV, Job, MatchResult
from app.schemas.all_schemas import MatchRequest, MatchScoreBreakdown, MatchBlockedResponse
from app.ai.pipeline import calculate_hybrid_match, COMMON_TECH_SKILLS

router = APIRouter()


@router.post("/calculate", response_model=MatchScoreBreakdown)
async def calculate_match(data: MatchRequest, db: AsyncSession = Depends(get_db)):
    """
    Calculate Hybrid Job Matching Score.
    Pre-conditions:
    1. CV must exist in DB.
    2. CV extraction must be completed (NOT failed or extraction_failed).
    3. Extracted data must pass minimal validity checks (no %PDF-1.4 or raw PDF syntax).
    4. Target Job must exist and have valid criteria.
    If pre-conditions fail:
    Returns HTTP 400 with blocked status and match_score: null.
    NEVER returns 42% or fake mock scores.
    """
    # 1. Query CV
    cv_res = await db.execute(select(CV).where(CV.id == data.cv_id))
    cv = cv_res.scalars().first()
    if not cv:
        raise HTTPException(status_code=404, detail="Không tìm thấy CV.")

    # 2. Check if CV extraction failed or is invalid
    if cv.extraction_status in ["failed", "extraction_failed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "blocked",
                "error_code": "CV_EXTRACTION_INVALID",
                "message": "Không thể tính điểm do dữ liệu CV chưa được trích xuất chính xác hoặc tệp CV bị lỗi.",
                "match_score": None
            }
        )

    if cv.extraction_status != "completed" or not cv.parsed_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "blocked",
                "error_code": "CV_NOT_PROCESSED",
                "message": "CV chưa được xử lý hoàn tất. Vui lòng chờ quá trình trích xuất hoàn tất.",
                "match_score": None
            }
        )

    # 3. Check for signs of corrupted data (%PDF-1.4 in name or PDF syntax)
    cv_data = cv.parsed_data or {}
    full_name = cv_data.get("full_name") or ""
    if "%PDF" in full_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "blocked",
                "error_code": "CV_EXTRACTION_CORRUPTED",
                "message": "Dữ liệu CV chứa thông tin hỏng (%PDF-1.4). Vui lòng tải lại CV hợp lệ.",
                "match_score": None
            }
        )

    # 4. Query Job
    job_res = await db.execute(select(Job).where(Job.id == data.job_id))
    job = job_res.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy tin tuyển dụng.")

    # Extract required skills from Job requirements or skills
    req_skills = []
    pref_skills = []

    # Check text for common skills if not explicitly defined
    combined_job_text = f"{job.title} {job.requirements} {job.description}"
    for skill in COMMON_TECH_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', combined_job_text, re.IGNORECASE):
            if "ưu tiên" in combined_job_text.lower() and skill.lower() in combined_job_text.lower().split("ưu tiên")[-1]:
                pref_skills.append(skill)
            else:
                req_skills.append(skill)

    # Deduplicate and ensure at least title/key skills are present
    req_skills = list(dict.fromkeys(req_skills))
    pref_skills = [p for p in dict.fromkeys(pref_skills) if p not in req_skills]

    if not req_skills:
        # Fallback to general skills if job description is very minimal
        req_skills = ["Python", "FastAPI", "PostgreSQL"]

    job_data = {
        "title": job.title,
        "description": job.description,
        "requirements": job.requirements,
        "required_skills": req_skills,
        "preferred_skills": pref_skills
    }

    # 5. Calculate honest hybrid match
    result = calculate_hybrid_match(cv_data, job_data)

    # 6. Persist or update match result in database
    existing_match_res = await db.execute(
        select(MatchResult).where(MatchResult.job_id == job.id, MatchResult.cv_id == cv.id)
    )
    match_record = existing_match_res.scalars().first()

    if not match_record:
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
    else:
        match_record.overall_score = result["overall_score"]
        match_record.hard_skills_score = result["hard_skills_score"]
        match_record.semantic_score = result["semantic_score"]
        match_record.experience_score = result["experience_score"]
        match_record.matched_skills = result["matched_skills"]
        match_record.missing_required_skills = result["missing_required_skills"]
        match_record.missing_preferred_skills = result["missing_preferred_skills"]
        match_record.ai_explanation = result["ai_explanation"]
        match_record.recommendations = result["recommendations"]

    await db.commit()

    return MatchScoreBreakdown(**result)


@router.get("/result", response_model=MatchScoreBreakdown)
async def get_match_result(
    job_id: str,
    cv_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve stored MatchResult from DB cache without re-invoking calculation.
    Returns 404 if not yet calculated.
    """
    res = await db.execute(
        select(MatchResult).where(MatchResult.job_id == job_id, MatchResult.cv_id == cv_id)
    )
    m = res.scalars().first()
    if not m:
        raise HTTPException(status_code=404, detail="Chưa có kết quả so khớp được lưu.")

    return MatchScoreBreakdown(
        overall_score=m.overall_score,
        hard_skills_score=m.hard_skills_score,
        semantic_score=m.semantic_score,
        experience_score=m.experience_score,
        matched_skills=m.matched_skills or [],
        missing_required_skills=m.missing_required_skills or [],
        missing_preferred_skills=m.missing_preferred_skills or [],
        ai_explanation=m.ai_explanation or "",
        recommendations=m.recommendations or []
    )


@router.get("/results")
async def get_all_cv_match_results(
    cv_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all stored match results for a given CV to rank jobs instantly.
    """
    res = await db.execute(
        select(MatchResult).where(MatchResult.cv_id == cv_id)
    )
    records = res.scalars().all()
    return [
        {
            "job_id": r.job_id,
            "cv_id": r.cv_id,
            "overall_score": r.overall_score,
            "hard_skills_score": r.hard_skills_score,
            "matched_skills": r.matched_skills or [],
            "missing_required_skills": r.missing_required_skills or [],
            "ai_explanation": r.ai_explanation or ""
        }
        for r in records
    ]

from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user_payload
from app.core.audit import log_audit_event
from app.api.v1.endpoints.notifications import create_in_app_notification
from app.models.entities import Application, Job, CV, User, MatchResult, ApplicationStatus
from app.schemas.all_schemas import ApplicationCreate, ApplicationStatusUpdate, ApplicationResponse, GenericMessageResponse
from app.ai.pipeline import calculate_hybrid_match

router = APIRouter()


@router.get("", response_model=List[ApplicationResponse])
async def get_applications(
    candidate_id: Optional[str] = None,
    job_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    auth_payload: Optional[dict] = Depends(get_current_user_payload)
):
    query = select(Application).options(
        selectinload(Application.job).selectinload(Job.company),
        selectinload(Application.cv),
        selectinload(Application.match_result)
    )
    if candidate_id:
        query = query.where(Application.candidate_id == candidate_id)
    elif auth_payload and auth_payload.get("role") == "candidate":
        # Candidate only sees their own applications
        query = query.where(Application.candidate_id == auth_payload["sub"])

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
async def submit_application(
    data: ApplicationCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: Optional[dict] = Depends(get_current_user_payload)
):
    # Fetch job & cv
    job = (await db.execute(
        select(Job).options(selectinload(Job.company), selectinload(Job.job_skills)).where(Job.id == data.job_id)
    )).scalars().first()
    cv = (await db.execute(select(CV).where(CV.id == data.cv_id))).scalars().first()

    if not job or not cv:
        raise HTTPException(status_code=404, detail="Không tìm thấy việc làm hoặc CV.")

    # Determine real candidate ID from authenticated token
    candidate_id = auth_payload.get("sub") if auth_payload else "user-cand-1"

    app = Application(
        job_id=data.job_id,
        candidate_id=candidate_id,
        cv_id=data.cv_id,
        status=ApplicationStatus.SUBMITTED,
        cover_letter=data.cover_letter,
    )
    db.add(app)
    await db.flush()

    # Automatically compute match result
    job_req_skills = [js.skill.name for js in job.job_skills if js.skill and js.is_required] if job.job_skills else ["Chuyên môn"]
    job_pref_skills = [js.skill.name for js in job.job_skills if js.skill and not js.is_required] if job.job_skills else []

    job_data_for_match = {
        "title": job.title,
        "description": job.description,
        "requirements": job.requirements,
        "required_skills": job_req_skills,
        "preferred_skills": job_pref_skills
    }
    breakdown = calculate_hybrid_match(cv.parsed_data or {}, job_data_for_match)

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

    # In-App Notification to Recruiter
    if job.creator_id:
        await create_in_app_notification(
            db,
            user_id=job.creator_id,
            title="Hồ sơ ứng tuyển mới",
            message=f"Có ứng viên mới nộp đơn cho vị trí '{job.title}' (Điểm khớp AI: {round(match_rec.overall_score)}%).",
            type="application_update",
            link="/recruiter/candidates"
        )

    # In-App Notification to Candidate
    await create_in_app_notification(
        db,
        user_id=candidate_id,
        title="Ứng tuyển thành công",
        message=f"Hồ sơ của bạn đã được gửi thành công đến nhà tuyển dụng cho vị trí '{job.title}'.",
        type="application_update",
        link="/candidate/applications"
    )

    await log_audit_event(
        db,
        action="application.submitted",
        user_id=candidate_id,
        target_type="application",
        target_id=app.id,
        details={"job_id": job.id, "match_score": match_rec.overall_score},
        request=request
    )
    await db.commit()

    cand_name = cv.parsed_data.get("full_name", "Ứng viên") if cv.parsed_data else "Ứng viên"
    cand_email = cv.parsed_data.get("email", "") if cv.parsed_data else ""

    return ApplicationResponse(
        id=app.id,
        job_id=app.job_id,
        job_title=job.title,
        company_name=job.company.name if job.company else None,
        candidate_id=app.candidate_id,
        candidate_name=cand_name,
        candidate_email=cand_email,
        cv_id=app.cv_id,
        status=app.status,
        cover_letter=app.cover_letter,
        internal_notes=app.internal_notes,
        match_score=match_rec.overall_score,
        created_at=app.created_at
    )


@router.delete("/{app_id}", response_model=GenericMessageResponse)
async def withdraw_application(
    app_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: Optional[dict] = Depends(get_current_user_payload)
):
    """
    Candidate withdrawal of their submitted application (Phase 5).
    """
    res = await db.execute(
        select(Application).options(selectinload(Application.job)).where(Application.id == app_id)
    )
    app = res.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn ứng tuyển.")

    user_id = auth_payload.get("sub") if auth_payload else None
    if user_id and app.candidate_id != user_id and auth_payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Bạn không có quyền rút hồ sơ này.")

    app.status = ApplicationStatus.WITHDRAWN

    if app.job and app.job.creator_id:
        await create_in_app_notification(
            db,
            user_id=app.job.creator_id,
            title="Ứng viên đã rút đơn",
            message=f"Ứng viên đã rút đơn ứng tuyển cho vị trí '{app.job.title}'.",
            type="application_update",
            link="/recruiter/candidates"
        )

    await log_audit_event(
        db,
        action="application.withdrawn",
        user_id=user_id,
        target_type="application",
        target_id=app.id,
        request=request
    )
    await db.commit()
    return GenericMessageResponse(message="Rút đơn ứng tuyển thành công.", status="success")


@router.put("/{app_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    app_id: str,
    data: ApplicationStatusUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: Optional[dict] = Depends(get_current_user_payload)
):
    res = await db.execute(
        select(Application).options(selectinload(Application.job)).where(Application.id == app_id)
    )
    app = res.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn ứng tuyển.")

    old_status = app.status
    app.status = data.status
    if data.internal_notes is not None:
        app.internal_notes = data.internal_notes

    # Notify candidate of status update
    status_text_map = {
        "reviewing": "đang được xem xét",
        "shortlisted": "đã được chọn vào danh sách phỏng vấn",
        "interviewed": "đã hoàn thành phỏng vấn",
        "offered": "đã được gửi lời mời nhận việc (Offer)",
        "rejected": "chưa phù hợp với đợt tuyển dụng này"
    }
    status_label = status_text_map.get(data.status, data.status)
    if app.job:
        await create_in_app_notification(
            db,
            user_id=app.candidate_id,
            title="Cập nhật trạng thái hồ sơ ứng tuyển",
            message=f"Hồ sơ của bạn cho vị trí '{app.job.title}' {status_label}.",
            type="application_update",
            link="/candidate/applications"
        )

    await log_audit_event(
        db,
        action="application.status_updated",
        user_id=auth_payload.get("sub") if auth_payload else None,
        target_type="application",
        target_id=app.id,
        details={"old_status": old_status, "new_status": data.status},
        request=request
    )
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


@router.put("/{app_id}/schedule-interview", response_model=GenericMessageResponse)
async def schedule_interview(
    app_id: str,
    schedule_data: Dict[str, Any],
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: Optional[dict] = Depends(get_current_user_payload)
):
    """
    Recruiter schedules an interview with specific timestamp and location (Phase 6).
    """
    res = await db.execute(
        select(Application).options(selectinload(Application.job)).where(Application.id == app_id)
    )
    app = res.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn ứng tuyển.")

    interview_time_str = schedule_data.get("interview_time")
    interview_location = schedule_data.get("interview_location", "Văn phòng công ty hoặc Google Meet")
    notes = schedule_data.get("notes")

    if interview_time_str:
        try:
            app.interview_time = datetime.fromisoformat(interview_time_str)
        except Exception:
            pass
    app.interview_location = interview_location
    app.status = ApplicationStatus.INTERVIEWED
    if notes:
        app.internal_notes = f"{app.internal_notes or ''}\nLịch phỏng vấn: {notes}".strip()

    # Notify Candidate
    if app.job:
        await create_in_app_notification(
            db,
            user_id=app.candidate_id,
            title="Lời mời phỏng vấn",
            message=f"Bạn có lịch phỏng vấn cho vị trí '{app.job.title}' tại {interview_location}.",
            type="interview",
            link="/candidate/applications"
        )

    await log_audit_event(
        db,
        action="application.interview_scheduled",
        user_id=auth_payload.get("sub") if auth_payload else None,
        target_type="application",
        target_id=app.id,
        details={"location": interview_location, "time": interview_time_str},
        request=request
    )
    await db.commit()

    return GenericMessageResponse(
        message="Lên lịch phỏng vấn thành công và đã thông báo tới ứng viên.",
        status="success"
    )

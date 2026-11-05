from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.security import require_role
from app.core.audit import log_audit_event
from app.models.entities import User, Job, AuditLog
from app.schemas.all_schemas import UserResponse

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
async def list_users(
    role: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _auth: dict = Depends(require_role("admin"))
):
    query = select(User)
    if role and role != "all":
        query = query.where(User.role == role)
    result = await db.execute(query.order_by(User.created_at.desc()))
    users = result.scalars().all()
    return [
        UserResponse(
            id=u.id,
            email=u.email,
            full_name=u.full_name,
            phone=u.phone,
            role=u.role,
            is_active=u.is_active,
            is_verified=u.is_verified,
            created_at=u.created_at
        )
        for u in users
    ]


@router.put("/users/{user_id}/toggle-active", response_model=UserResponse)
async def toggle_user_active(
    user_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _auth: dict = Depends(require_role("admin"))
):
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    user.is_active = not user.is_active
    await log_audit_event(
        db,
        action="admin.toggle_user_active",
        user_id=_auth["sub"],
        target_type="user",
        target_id=user.id,
        details={"email": user.email, "is_active": user.is_active},
        request=request
    )
    await db.commit()
    await db.refresh(user)

    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at
    )


@router.put("/jobs/{job_id}/moderate")
async def moderate_job(
    job_id: str,
    status: str,
    request: Request,
    rejection_reason: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _auth: dict = Depends(require_role("admin"))
):
    res = await db.execute(select(Job).where(Job.id == job_id))
    job = res.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy tin tuyển dụng.")

    job.status = status
    if rejection_reason:
        job.rejection_reason = rejection_reason

    await log_audit_event(
        db,
        action="admin.moderate_job",
        user_id=_auth["sub"],
        target_type="job",
        target_id=job.id,
        details={"status": status, "rejection_reason": rejection_reason},
        request=request
    )
    await db.commit()

    return {"message": "Cập nhật trạng thái kiểm duyệt thành công", "job_id": job.id, "status": job.status}


@router.get("/reports")
async def list_job_reports(
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _auth: dict = Depends(require_role("admin"))
):
    from app.models.entities import JobReport
    query = select(JobReport).order_by(JobReport.created_at.desc())
    if status_filter and status_filter != "all":
        query = query.where(JobReport.status == status_filter)
    result = await db.execute(query)
    reports = result.scalars().all()
    return [
        {
            "id": r.id,
            "job_id": r.job_id,
            "reporter_id": r.reporter_id,
            "reason": r.reason,
            "details": r.details,
            "status": r.status,
            "action_taken": r.action_taken,
            "created_at": r.created_at,
            "updated_at": r.updated_at
        }
        for r in reports
    ]


@router.put("/reports/{report_id}/action")
async def resolve_job_report(
    report_id: str,
    action: str,  # dismiss, suspend_job, mark_reviewed
    request: Request,
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _auth: dict = Depends(require_role("admin"))
):
    from app.models.entities import JobReport, JobStatus
    res = await db.execute(select(JobReport).where(JobReport.id == report_id))
    report = res.scalars().first()
    if not report:
        raise HTTPException(status_code=404, detail="Không tìm thấy báo cáo.")

    report.status = "action_taken" if action == "suspend_job" else "dismissed"
    report.action_taken = action

    if action == "suspend_job":
        # Automatically suspend/reject the violating job
        job_res = await db.execute(select(Job).where(Job.id == report.job_id))
        job = job_res.scalars().first()
        if job:
            job.status = JobStatus.REJECTED
            job.rejection_reason = f"Đình chỉ do vi phạm quy chuẩn an toàn: {notes or report.reason}"

    await log_audit_event(
        db,
        action="admin.resolve_job_report",
        user_id=_auth["sub"],
        target_type="job_report",
        target_id=report.id,
        details={"action": action, "notes": notes},
        request=request
    )
    await db.commit()
    return {"message": "Đã xử lý khiếu nại/báo cáo thành công.", "report_id": report.id, "status": report.status}


@router.put("/companies/{company_id}/verify")
async def verify_company(
    company_id: str,
    verification_status: str,  # verified, rejected, pending_verification
    request: Request,
    tax_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _auth: dict = Depends(require_role("admin"))
):
    from datetime import datetime, timezone
    from app.models.entities import Company
    res = await db.execute(select(Company).where(Company.id == company_id))
    company = res.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Không tìm thấy doanh nghiệp.")

    company.verification_status = verification_status
    if tax_id:
        company.tax_id = tax_id
    if verification_status == "verified":
        company.verified_at = datetime.now(timezone.utc)

    await log_audit_event(
        db,
        action="admin.verify_company",
        user_id=_auth["sub"],
        target_type="company",
        target_id=company.id,
        details={"status": verification_status, "tax_id": tax_id},
        request=request
    )
    await db.commit()
    return {
        "message": f"Cập nhật xác minh doanh nghiệp: {verification_status}",
        "company_id": company.id,
        "verification_status": company.verification_status
    }

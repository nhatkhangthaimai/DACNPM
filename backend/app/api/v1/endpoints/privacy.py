import os
import logging
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_authenticated_user_payload
from app.core.audit import log_audit_event
from app.models.entities import User, CandidateProfile, CV, Application, MatchResult, DataConsent, DataRequest
from app.schemas.all_schemas import GenericMessageResponse

logger = logging.getLogger("hiresense.privacy")
router = APIRouter()


@router.post("/consent", response_model=GenericMessageResponse)
async def record_user_consent(
    consent_data: Dict[str, Any],
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: dict = Depends(get_authenticated_user_payload)
):
    """
    Records explicit user consent for CV AI processing, recruitment matching,
    and storage in compliance with Vietnam Data Protection Law 91/2025/QH15.
    """
    user_id = auth_payload["sub"]
    consent_type = consent_data.get("consent_type", "cv_ai_processing")
    granted = consent_data.get("granted", True)

    forwarded = request.headers.get("X-Forwarded-For")
    ip = forwarded.split(",")[0].strip() if forwarded else (request.client.host if request.client else "127.0.0.1")

    consent = DataConsent(
        user_id=user_id,
        consent_type=consent_type,
        granted=granted,
        ip_address=ip
    )
    db.add(consent)
    await log_audit_event(
        db,
        action="privacy.consent_recorded",
        user_id=user_id,
        target_type="data_consent",
        details={"consent_type": consent_type, "granted": granted},
        request=request
    )
    await db.commit()

    return GenericMessageResponse(
        message=f"Đã ghi nhận đồng thuận {consent_type}: {'Đồng ý' if granted else 'Thu hồi'}.",
        status="success"
    )


@router.get("/consent")
async def get_user_consents(
    db: AsyncSession = Depends(get_db),
    auth_payload: dict = Depends(get_authenticated_user_payload)
):
    """Returns the candidate's active consent declarations."""
    user_id = auth_payload["sub"]
    res = await db.execute(
        select(DataConsent).where(DataConsent.user_id == user_id).order_by(DataConsent.granted_at.desc())
    )
    consents = res.scalars().all()
    return [
        {
            "id": c.id,
            "consent_type": c.consent_type,
            "granted": c.granted,
            "granted_at": c.granted_at,
            "revoked_at": c.revoked_at
        }
        for c in consents
    ]


@router.get("/export-data")
async def export_my_data(
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: dict = Depends(get_authenticated_user_payload)
):
    """
    Data Portability under Law 91/2025/QH15.
    Exports all personal profile information, uploaded CV metadata, parsed skills,
    and job applications in machine-readable JSON format.
    """
    user_id = auth_payload["sub"]
    user_res = await db.execute(
        select(User)
        .options(selectinload(User.candidate_profile))
        .where(User.id == user_id)
    )
    user = user_res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    # Get CVs
    cv_res = await db.execute(
        select(CV).where(CV.candidate_id == user.candidate_profile.id if user.candidate_profile else False)
    )
    cvs = cv_res.scalars().all()

    # Get Applications
    app_res = await db.execute(
        select(Application)
        .options(selectinload(Application.job))
        .where(Application.candidate_id == user_id)
    )
    apps = app_res.scalars().all()

    export_payload = {
        "export_metadata": {
            "platform": "HireSense AI - Smart Recruitment Platform",
            "law_compliance": "Vietnam Law 91/2025/QH15 & Decree 356/2025/ND-CP",
            "exported_at": user.updated_at.isoformat() if user.updated_at else None,
        },
        "user_account": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "role": user.role,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        },
        "candidate_profile": {
            "title": user.candidate_profile.title if user.candidate_profile else None,
            "bio": user.candidate_profile.bio if user.candidate_profile else None,
            "location": user.candidate_profile.location if user.candidate_profile else None,
            "years_of_experience": user.candidate_profile.years_of_experience if user.candidate_profile else 0,
        },
        "cv_documents": [
            {
                "id": c.id,
                "file_name": c.file_name,
                "mime_type": c.mime_type,
                "is_primary": c.is_primary,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "parsed_data": c.parsed_data
            }
            for c in cvs
        ],
        "applications": [
            {
                "id": a.id,
                "job_title": a.job.title if a.job else None,
                "company_id": a.job.company_id if a.job else None,
                "status": a.status,
                "cover_letter": a.cover_letter,
                "created_at": a.created_at.isoformat() if a.created_at else None
            }
            for a in apps
        ]
    }

    await log_audit_event(
        db,
        action="privacy.data_exported",
        user_id=user_id,
        target_type="user",
        target_id=user_id,
        request=request
    )
    await db.commit()
    return export_payload


@router.delete("/delete-all-data", response_model=GenericMessageResponse)
async def delete_all_my_data(
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: dict = Depends(get_authenticated_user_payload)
):
    """
    Right to Erasure ('Right to be Forgotten') under Law 91/2025/QH15.
    Permanently deletes all candidate CV files from storage/disk, applications,
    match results, profile records, and user account.
    """
    user_id = auth_payload["sub"]
    user_res = await db.execute(
        select(User)
        .options(selectinload(User.candidate_profile))
        .where(User.id == user_id)
    )
    user = user_res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    # Delete physical CV files from disk if stored locally
    if user.candidate_profile:
        cv_res = await db.execute(
            select(CV).where(CV.candidate_id == user.candidate_profile.id)
        )
        cvs = cv_res.scalars().all()
        for cv in cvs:
            if cv.file_url and cv.file_url.startswith("/uploads/"):
                file_rel = cv.file_url.replace("/uploads/", "")
                file_path = os.path.join("uploads", file_rel)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logger.warning(f"Could not delete physical CV file {file_path}: {e}")

    # Record audit log before deleting user
    await log_audit_event(
        db,
        action="privacy.account_erasure",
        user_id=user_id,
        target_type="user",
        target_id=user_id,
        details={"email": user.email, "compliance": "Law 91/2025/QH15"},
        request=request
    )

    # Delete User record (cascades to profile, CVs, applications, match results)
    await db.delete(user)
    await db.commit()

    return GenericMessageResponse(
        message="Toàn bộ dữ liệu cá nhân, hồ sơ CV và tài khoản đã được xóa vĩnh viễn khỏi hệ thống theo quy định.",
        status="success"
    )


from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import User, Job, AuditLog
from app.schemas.all_schemas import UserResponse

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
async def list_users(role: Optional[str] = None, db: AsyncSession = Depends(get_db)):
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
async def toggle_user_active(user_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")

    user.is_active = not user.is_active
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
async def moderate_job(job_id: str, status: str, rejection_reason: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Job).where(Job.id == job_id))
    job = res.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy tin tuyển dụng.")

    job.status = status
    if rejection_reason:
        job.rejection_reason = rejection_reason
    await db.commit()

    return {"message": "Cập nhật trạng thái kiểm duyệt thành công", "job_id": job.id, "status": job.status}

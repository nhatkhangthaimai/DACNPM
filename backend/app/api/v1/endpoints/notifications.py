from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_authenticated_user_payload
from app.models.entities import Notification
from app.schemas.all_schemas import GenericMessageResponse

router = APIRouter()


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    type: str
    link: Optional[str] = None
    is_read: bool
    created_at: datetime


async def create_in_app_notification(
    db: AsyncSession,
    user_id: str,
    title: str,
    message: str,
    type: str = "system",
    link: Optional[str] = None
) -> Notification:
    """Helper to dispatch an in-app notification to any user."""
    notif = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=type,
        link=link,
        is_read=False
    )
    db.add(notif)
    await db.flush()
    return notif


@router.get("", response_model=List[NotificationResponse])
async def get_my_notifications(
    db: AsyncSession = Depends(get_db),
    auth_payload: dict = Depends(get_authenticated_user_payload)
):
    user_id = auth_payload["sub"]
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .limit(50)
    )
    return result.scalars().all()


@router.get("/unread-count")
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    auth_payload: dict = Depends(get_authenticated_user_payload)
):
    user_id = auth_payload["sub"]
    result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id, Notification.is_read == False)
    )
    unread_items = result.scalars().all()
    return {"unread_count": len(unread_items)}


@router.put("/{notif_id}/read", response_model=GenericMessageResponse)
async def mark_as_read(
    notif_id: str,
    db: AsyncSession = Depends(get_db),
    auth_payload: dict = Depends(get_authenticated_user_payload)
):
    user_id = auth_payload["sub"]
    res = await db.execute(
        select(Notification).where(Notification.id == notif_id, Notification.user_id == user_id)
    )
    notif = res.scalars().first()
    if not notif:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông báo.")

    notif.is_read = True
    await db.commit()
    return GenericMessageResponse(message="Đã đánh dấu đã đọc.", status="success")


@router.put("/read-all", response_model=GenericMessageResponse)
async def mark_all_as_read(
    db: AsyncSession = Depends(get_db),
    auth_payload: dict = Depends(get_authenticated_user_payload)
):
    user_id = auth_payload["sub"]
    res = await db.execute(
        select(Notification).where(Notification.user_id == user_id, Notification.is_read == False)
    )
    items = res.scalars().all()
    for item in items:
        item.is_read = True
    await db.commit()
    return GenericMessageResponse(message="Đã đánh dấu tất cả thông báo là đã đọc.", status="success")


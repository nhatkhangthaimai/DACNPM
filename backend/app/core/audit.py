import uuid
import logging
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from app.models.entities import AuditLog

logger = logging.getLogger("hiresense.audit")


async def log_audit_event(
    db: AsyncSession,
    action: str,
    user_id: Optional[str] = None,
    target_type: Optional[str] = None,
    target_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    request: Optional[Request] = None,
    ip_address: Optional[str] = None
) -> AuditLog:
    """
    Persists a security or business audit log entry to the database and structured logger.
    Complies with OWASP logging guidelines and Vietnam Data Protection Law requirements.
    """
    if request and not ip_address:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip_address = forwarded.split(",")[0].strip()
        elif request.client:
            ip_address = request.client.host
        else:
            ip_address = "127.0.0.1"

    audit_entry = AuditLog(
        id=str(uuid.uuid4()),
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details or {},
        ip_address=ip_address
    )
    db.add(audit_entry)
    # Flush without committing so caller's transaction manages commit
    await db.flush()

    logger.info(
        f"[AUDIT] action={action} user_id={user_id} target={target_type}:{target_id} ip={ip_address}"
    )
    return audit_entry


import logging
from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import (
    verify_password, get_password_hash, create_access_token,
    get_current_user_payload, create_password_reset_token, decode_password_reset_token
)
from app.core.rate_limiter import auth_rate_limiter, register_rate_limiter
from app.core.audit import log_audit_event
from app.models.entities import User, CandidateProfile, Company, CompanyMember, UserRole
from app.schemas.all_schemas import (
    Token, LoginRequest, RegisterCandidateRequest, RegisterRecruiterRequest,
    UserResponse, ForgotPasswordRequest, ResetPasswordRequest, GenericMessageResponse
)

logger = logging.getLogger("hiresense.auth")
router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _rate_limit: bool = Depends(auth_rate_limiter)
):
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalars().first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        await log_audit_event(
            db,
            action="auth.login_failed",
            target_type="user",
            details={"email": login_data.email, "reason": "invalid_credentials"},
            request=request
        )
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        await log_audit_event(
            db,
            action="auth.login_blocked",
            user_id=user.id,
            target_type="user",
            target_id=user.id,
            details={"email": user.email, "reason": "account_inactive"},
            request=request
        )
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đang bị tạm khóa bởi quản trị viên."
        )

    access_token = create_access_token(subject=user.id, role=user.role)
    await log_audit_event(
        db,
        action="auth.login_success",
        user_id=user.id,
        target_type="user",
        target_id=user.id,
        details={"role": user.role},
        request=request
    )
    await db.commit()

    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        full_name=user.full_name,
        email=user.email
    )


@router.post("/register/candidate", response_model=Token)
async def register_candidate(
    data: RegisterCandidateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _rate_limit: bool = Depends(register_rate_limiter)
):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email này đã được sử dụng.")

    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        full_name=data.full_name,
        phone=data.phone,
        role=UserRole.CANDIDATE,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    await db.flush()

    profile = CandidateProfile(
        user_id=user.id,
        title=data.title,
    )
    db.add(profile)

    await log_audit_event(
        db,
        action="auth.register_candidate",
        user_id=user.id,
        target_type="candidate_profile",
        target_id=profile.id,
        request=request
    )
    await db.commit()

    access_token = create_access_token(subject=user.id, role=user.role)
    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        full_name=user.full_name,
        email=user.email
    )


@router.post("/register/recruiter", response_model=Token)
async def register_recruiter(
    data: RegisterRecruiterRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _rate_limit: bool = Depends(register_rate_limiter)
):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email này đã được sử dụng.")

    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        full_name=data.full_name,
        phone=data.phone,
        role=UserRole.RECRUITER,
        is_active=True,
        is_verified=True,
    )
    db.add(user)
    await db.flush()

    slug = data.company_name.lower().replace(" ", "-") + f"-{user.id[:4]}"
    company = Company(
        name=data.company_name,
        slug=slug,
        website=data.company_website,
        industry=data.company_industry,
        status="approved"
    )
    db.add(company)
    await db.flush()

    member = CompanyMember(
        company_id=company.id,
        user_id=user.id,
        role="owner"
    )
    db.add(member)

    await log_audit_event(
        db,
        action="auth.register_recruiter",
        user_id=user.id,
        target_type="company",
        target_id=company.id,
        details={"company_name": company.name},
        request=request
    )
    await db.commit()

    access_token = create_access_token(subject=user.id, role=user.role)
    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        full_name=user.full_name,
        email=user.email
    )


@router.post("/forgot-password", response_model=GenericMessageResponse)
async def forgot_password(
    data: ForgotPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _rate_limit: bool = Depends(auth_rate_limiter)
):
    """
    OWASP ASVS compliant password reset request.
    Always returns success to prevent user email enumeration.
    Generates a secure signed token valid for 15 minutes.
    """
    res = await db.execute(select(User).where(User.email == data.email))
    user = res.scalars().first()

    if user:
        reset_token = create_password_reset_token(user.email)
        logger.info(f"[Password Reset Token Generated] email={user.email} token_prefix={reset_token[:12]}...")
        await log_audit_event(
            db,
            action="auth.password_reset_requested",
            user_id=user.id,
            target_type="user",
            target_id=user.id,
            request=request
        )
        await db.commit()

    return GenericMessageResponse(
        message="Nếu địa chỉ email tồn tại trên hệ thống, hướng dẫn đặt lại mật khẩu đã được xử lý.",
        status="success"
    )


@router.post("/reset-password", response_model=GenericMessageResponse)
async def reset_password(
    data: ResetPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Validates token and updates user's password with fresh bcrypt hash.
    """
    email = decode_password_reset_token(data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã đặt lại mật khẩu không hợp lệ hoặc đã hết hạn (tối đa 15 phút)."
        )

    res = await db.execute(select(User).where(User.email == email))
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy tài khoản người dùng.")

    if len(data.new_password) < 8:
        raise HTTPException(status_code=400, detail="Mật khẩu mới phải có ít nhất 8 ký tự.")

    user.hashed_password = get_password_hash(data.new_password)
    await log_audit_event(
        db,
        action="auth.password_reset_completed",
        user_id=user.id,
        target_type="user",
        target_id=user.id,
        request=request
    )
    await db.commit()

    return GenericMessageResponse(
        message="Mật khẩu của bạn đã được đặt lại thành công. Vui lòng đăng nhập bằng mật khẩu mới.",
        status="success"
    )


@router.post("/logout", response_model=GenericMessageResponse)
async def logout(
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: Optional[dict] = Depends(get_current_user_payload)
):
    if auth_payload and auth_payload.get("sub"):
        await log_audit_event(
            db,
            action="auth.logout",
            user_id=auth_payload["sub"],
            target_type="user",
            target_id=auth_payload["sub"],
            request=request
        )
        await db.commit()
    return GenericMessageResponse(message="Đăng xuất thành công.", status="success")


@router.get("/me", response_model=UserResponse)
async def get_me(
    db: AsyncSession = Depends(get_db),
    auth_payload: dict = Depends(get_current_user_payload)
):
    if not auth_payload or not auth_payload.get("sub"):
        raise HTTPException(status_code=401, detail="Chưa xác thực người dùng.")
    
    user_id = auth_payload["sub"]
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng.")
    
    company_id = None
    company_name = None
    if user.role == UserRole.RECRUITER:
        mem_res = await db.execute(
            select(CompanyMember, Company)
            .join(Company, CompanyMember.company_id == Company.id)
            .where(CompanyMember.user_id == user.id)
        )
        row = mem_res.first()
        if row:
            company_id = row[1].id
            company_name = row[1].name

    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        role=user.role,
        is_active=user.is_active,
        is_verified=user.is_verified,
        company_id=company_id,
        company_name=company_name,
        created_at=user.created_at
    )

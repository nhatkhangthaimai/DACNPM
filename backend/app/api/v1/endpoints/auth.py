from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.entities import User, CandidateProfile, Company, CompanyMember, UserRole
from app.schemas.all_schemas import Token, LoginRequest, RegisterCandidateRequest, RegisterRecruiterRequest, UserResponse

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == login_data.email))
    user = result.scalars().first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản của bạn đang bị tạm khóa bởi quản trị viên."
        )

    access_token = create_access_token(subject=user.id, role=user.role)
    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        full_name=user.full_name,
        email=user.email
    )


@router.post("/register/candidate", response_model=Token)
async def register_candidate(data: RegisterCandidateRequest, db: AsyncSession = Depends(get_db)):
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
async def register_recruiter(data: RegisterRecruiterRequest, db: AsyncSession = Depends(get_db)):
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

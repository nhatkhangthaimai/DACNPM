from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user_payload, require_role
from app.models.entities import Company, CompanyMember, User, UserRole
from app.schemas.all_schemas import CompanyResponse, CompanyBase

router = APIRouter()


@router.get("", response_model=List[CompanyResponse])
async def list_companies(
    search: Optional[str] = None,
    industry: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    skip: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """List all companies with optional search, industry filter, and pagination."""
    query = select(Company)

    if status_filter and status_filter != "all":
        query = query.where(Company.status == status_filter)
    else:
        # Default to approved companies for public/candidate visibility
        query = query.where(Company.status == "approved")

    if industry and industry != "all":
        query = query.where(Company.industry.ilike(f"%{industry}%"))

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            Company.name.ilike(search_pattern) | 
            Company.description.ilike(search_pattern) |
            Company.address.ilike(search_pattern)
        )

    query = query.order_by(Company.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    companies = result.scalars().all()
    return companies


@router.get("/me", response_model=CompanyResponse)
async def get_my_company(
    db: AsyncSession = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_payload)
):
    """Retrieve the company associated with the current recruiter."""
    if not current_user:
        # Fallback to the first company for demo mode if no auth token
        result = await db.execute(select(Company).where(Company.status == "approved").limit(1))
        company = result.scalars().first()
        if not company:
            raise HTTPException(status_code=404, detail="Chưa có dữ liệu doanh nghiệp.")
        return company

    user_id = current_user.get("sub")
    # Check company membership
    mem_res = await db.execute(
        select(CompanyMember).options(selectinload(CompanyMember.company)).where(CompanyMember.user_id == user_id)
    )
    membership = mem_res.scalars().first()
    if membership and membership.company:
        return membership.company

    # Fallback to first company
    res = await db.execute(select(Company).limit(1))
    comp = res.scalars().first()
    if not comp:
        raise HTTPException(status_code=404, detail="Không tìm thấy doanh nghiệp của bạn.")
    return comp


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company_detail(company_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieve details for a single company."""
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Không tìm thấy doanh nghiệp.")
    return company


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: str,
    data: CompanyBase,
    db: AsyncSession = Depends(get_db),
    _auth: Optional[dict] = Depends(get_current_user_payload)
):
    """Update company details."""
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalars().first()
    if not company:
        raise HTTPException(status_code=404, detail="Không tìm thấy doanh nghiệp.")

    company.name = data.name
    company.website = data.website
    company.industry = data.industry
    company.company_size = data.company_size
    company.address = data.address
    company.description = data.description

    await db.commit()
    await db.refresh(company)
    return company

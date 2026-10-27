from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.entities import Job, JobSkill, Skill, JobStatus, Company
from app.schemas.all_schemas import JobCreate, JobUpdate, JobResponse

router = APIRouter()


@router.get("", response_model=List[JobResponse])
async def get_jobs(
    search: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Job).join(Company)
    if status_filter:
        query = query.where(Job.status == status_filter)
    else:
        query = query.where(Job.status == JobStatus.PUBLISHED)

    if location and location != "all":
        query = query.where(Job.location.ilike(f"%{location}%"))
    if job_type and job_type != "all":
        query = query.where(Job.job_type == job_type)
    if experience_level and experience_level != "all":
        query = query.where(Job.experience_level == experience_level)
    if search:
        query = query.where(Job.title.ilike(f"%{search}%") | Job.description.ilike(f"%{search}%"))

    result = await db.execute(query.order_by(Job.created_at.desc()))
    jobs = result.scalars().all()

    response = []
    for j in jobs:
        response.append(JobResponse(
            id=j.id,
            company_id=j.company_id,
            company_name=j.company.name if j.company else "Đối tác",
            company_logo=j.company.logo_url if j.company else None,
            title=j.title,
            description=j.description,
            requirements=j.requirements,
            benefits=j.benefits,
            job_type=j.job_type,
            location=j.location,
            salary_min=j.salary_min,
            salary_max=j.salary_max,
            currency=j.currency,
            experience_level=j.experience_level,
            status=j.status,
            required_skills=[],
            preferred_skills=[],
            created_at=j.created_at
        ))
    return response


@router.get("/{job_id}", response_model=JobResponse)
async def get_job_detail(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy tin tuyển dụng.")
    
    return JobResponse(
        id=job.id,
        company_id=job.company_id,
        company_name=job.company.name if job.company else "Đối tác",
        company_logo=job.company.logo_url if job.company else None,
        title=job.title,
        description=job.description,
        requirements=job.requirements,
        benefits=job.benefits,
        job_type=job.job_type,
        location=job.location,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        currency=job.currency,
        experience_level=job.experience_level,
        status=job.status,
        required_skills=[],
        preferred_skills=[],
        created_at=job.created_at
    )


@router.post("", response_model=JobResponse)
async def create_job(data: JobCreate, db: AsyncSession = Depends(get_db)):
    # Find or use default company
    result = await db.execute(select(Company))
    company = result.scalars().first()
    if not company:
        company = Company(name="HireSense Tech Partner", slug="hiresense-partner", status="approved")
        db.add(company)
        await db.flush()

    job = Job(
        company_id=company.id,
        title=data.title,
        description=data.description,
        requirements=data.requirements,
        benefits=data.benefits,
        job_type=data.job_type,
        location=data.location,
        salary_min=data.salary_min,
        salary_max=data.salary_max,
        currency=data.currency,
        experience_level=data.experience_level,
        status=JobStatus.PUBLISHED,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    return JobResponse(
        id=job.id,
        company_id=job.company_id,
        company_name=company.name,
        company_logo=company.logo_url,
        title=job.title,
        description=job.description,
        requirements=job.requirements,
        benefits=job.benefits,
        job_type=job.job_type,
        location=job.location,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        currency=job.currency,
        experience_level=job.experience_level,
        status=job.status,
        required_skills=data.required_skills,
        preferred_skills=data.preferred_skills,
        created_at=job.created_at
    )

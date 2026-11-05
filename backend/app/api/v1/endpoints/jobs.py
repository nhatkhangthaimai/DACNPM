import re
import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user_payload
from app.core.audit import log_audit_event
from app.core.scam_detector import analyze_job_scam_risk
from app.models.entities import Job, JobSkill, Skill, JobStatus, Company, CompanyMember, JobReport
from app.schemas.all_schemas import JobCreate, JobUpdate, JobResponse, GenericMessageResponse
import time
from functools import lru_cache
from app.ai.pipeline import COMMON_MULTI_INDUSTRY_SKILLS, normalize_skill

# Pre-compile regexes once for high-throughput job listing
_COMPILED_SKILLS = [
    (s, s.lower(), re.compile(r'(?:\b|\s|^)' + re.escape(s.lower()) + r'(?:\b|\s|$|[,\.\:\;\(\)])'))
    for s in COMMON_MULTI_INDUSTRY_SKILLS
]

@lru_cache(maxsize=1000)
def extract_job_skills(title: str, requirements: str, description: str):
    """Fallback skill extractor across multiple industries with precompiled regexes & LRU cache."""
    text = f"{title or ''} {requirements or ''} {description or ''}"
    reqs = []
    prefs = []
    text_lower = text.lower()
    has_uu_tien = "ưu tiên" in text_lower
    split_uu_tien = text_lower.split("ưu tiên")[-1] if has_uu_tien else ""

    for s, s_low, pat in _COMPILED_SKILLS:
        if pat.search(text_lower):
            if has_uu_tien and s_low in split_uu_tien:
                prefs.append(s)
            else:
                reqs.append(s)
    reqs = list(dict.fromkeys(reqs))
    prefs = [p for p in dict.fromkeys(prefs) if p not in reqs]
    return reqs or ["Chuyên môn"], prefs


# In-memory short-lived cache for GET /jobs responses (TTL: 30s)
_JOBS_CACHE: Dict[str, Any] = {}
_JOBS_CACHE_TIMESTAMP = 0.0
_JOBS_CACHE_TTL = 30.0  # seconds

def invalidate_jobs_cache():
    global _JOBS_CACHE, _JOBS_CACHE_TIMESTAMP
    _JOBS_CACHE.clear()
    _JOBS_CACHE_TIMESTAMP = 0.0


router = APIRouter()


@router.get("", response_model=List[JobResponse])
async def get_jobs(
    search: Optional[str] = None,
    location: Optional[str] = None,
    job_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    company_id: Optional[str] = None,
    industry: Optional[str] = None,
    min_salary: Optional[int] = None,
    max_salary: Optional[int] = None,
    sort_by: Optional[str] = None,
    limit: int = Query(100, ge=1, le=200),
    skip: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    global _JOBS_CACHE, _JOBS_CACHE_TIMESTAMP
    now = time.time()
    cache_key = f"{search}_{location}_{job_type}_{experience_level}_{status_filter}_{company_id}_{industry}_{min_salary}_{max_salary}_{sort_by}_{limit}_{skip}"

    if now - _JOBS_CACHE_TIMESTAMP < _JOBS_CACHE_TTL and cache_key in _JOBS_CACHE:
        return _JOBS_CACHE[cache_key]

    query = select(Job).options(
        selectinload(Job.company),
        selectinload(Job.job_skills).selectinload(JobSkill.skill)
    )

    if status_filter and status_filter != "all":
        query = query.where(Job.status == status_filter)
    elif not status_filter:
        # Default public view shows published jobs
        query = query.where(Job.status == JobStatus.PUBLISHED)

    if company_id:
        query = query.where(Job.company_id == company_id)

    if location and location != "all":
        query = query.where(Job.location.ilike(f"%{location}%"))

    if job_type and job_type != "all":
        query = query.where(Job.job_type == job_type)

    if experience_level and experience_level != "all":
        query = query.where(Job.experience_level == experience_level)

    if min_salary is not None:
        query = query.where(Job.salary_max >= min_salary)

    if max_salary is not None:
        query = query.where(Job.salary_min <= max_salary)

    if industry and industry != "all":
        query = query.join(Job.company).where(Company.industry.ilike(f"%{industry}%"))

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            Job.title.ilike(search_pattern) | 
            Job.description.ilike(search_pattern) |
            Job.requirements.ilike(search_pattern)
        )

    # Sorting
    if sort_by == "salary_desc":
        query = query.order_by(Job.salary_max.desc().nullslast(), Job.created_at.desc())
    elif sort_by == "salary_asc":
        query = query.order_by(Job.salary_min.asc().nullslast(), Job.created_at.desc())
    elif sort_by == "title":
        query = query.order_by(Job.title.asc())
    else:
        query = query.order_by(Job.created_at.desc())

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    jobs = result.scalars().all()

    response = []
    for j in jobs:
        # Check if structured skills are attached
        r_skills = []
        p_skills = []
        if j.job_skills:
            for js in j.job_skills:
                if js.skill:
                    if js.is_required:
                        r_skills.append(js.skill.name)
                    else:
                        p_skills.append(js.skill.name)
        if not r_skills and not p_skills:
            r_skills, p_skills = extract_job_skills(j.title, j.requirements, j.description)

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
            required_skills=r_skills,
            preferred_skills=p_skills,
            created_at=j.created_at
        ))

    if now - _JOBS_CACHE_TIMESTAMP >= _JOBS_CACHE_TTL:
        _JOBS_CACHE.clear()
        _JOBS_CACHE_TIMESTAMP = now
    _JOBS_CACHE[cache_key] = response
    return response


@router.post("/seed-multi-industry", tags=["Jobs"])
@router.get("/seed-multi-industry", tags=["Jobs"])
async def trigger_seed_multi_industry(db: AsyncSession = Depends(get_db)):
    """
    Public & Admin trigger endpoint to seed all 50 multi-industry jobs and 15 companies.
    100% idempotent: will not create duplicates.
    """
    invalidate_jobs_cache()
    from app.core.seeder import seed_all_multi_industry_data
    stats = await seed_all_multi_industry_data(db)
    
    count_res = await db.execute(select(Job))
    total_jobs = len(count_res.scalars().all())
    
    return {
        "status": "success",
        "message": "Seeded 50 multi-industry jobs and 15 companies successfully.",
        "newly_created": stats,
        "total_jobs_in_db": total_jobs
    }


@router.get("/{job_id}", response_model=JobResponse)
async def get_job_detail(job_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Job).options(
            selectinload(Job.company),
            selectinload(Job.job_skills).selectinload(JobSkill.skill)
        ).where(Job.id == job_id)
    )
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy tin tuyển dụng.")

    r_skills = []
    p_skills = []
    if job.job_skills:
        for js in job.job_skills:
            if js.skill:
                if js.is_required:
                    r_skills.append(js.skill.name)
                else:
                    p_skills.append(js.skill.name)
    if not r_skills and not p_skills:
        r_skills, p_skills = extract_job_skills(job.title, job.requirements, job.description)

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
        required_skills=r_skills,
        preferred_skills=p_skills,
        created_at=job.created_at
    )


@router.post("/{job_id}/report", response_model=GenericMessageResponse)
async def report_job(
    job_id: str,
    report_data: Dict[str, Any],
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: Optional[dict] = Depends(get_current_user_payload)
):
    """
    Submits a trust & safety report for a suspicious or fraudulent job posting.
    Complies with Phase 4 recruitment safety standards.
    """
    res = await db.execute(select(Job).where(Job.id == job_id))
    job = res.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy tin tuyển dụng.")

    reporter_id = auth_payload.get("sub") if auth_payload else None
    reason = report_data.get("reason", "scam")
    details = report_data.get("details", "")

    report = JobReport(
        job_id=job_id,
        reporter_id=reporter_id,
        reason=reason,
        details=details,
        status="pending"
    )
    db.add(report)

    await log_audit_event(
        db,
        action="job.reported_suspicious",
        user_id=reporter_id,
        target_type="job",
        target_id=job_id,
        details={"reason": reason, "details": details[:200]},
        request=request
    )
    await db.commit()

    return GenericMessageResponse(
        message="Báo cáo của bạn đã được ghi nhận. Quản trị viên sẽ kiểm tra và xử lý theo quy định.",
        status="success"
    )


@router.post("", response_model=JobResponse)
async def create_job(
    data: JobCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_payload)
):
    target_company_id = data.company_id
    creator_id = current_user.get("sub") if current_user else None

    # If no company_id provided, find company of logged-in user
    if not target_company_id and creator_id:
        mem_res = await db.execute(
            select(CompanyMember).where(CompanyMember.user_id == creator_id)
        )
        membership = mem_res.scalars().first()
        if membership:
            target_company_id = membership.company_id

    # Fallback to first company
    if not target_company_id:
        res = await db.execute(select(Company))
        company = res.scalars().first()
        if not company:
            company = Company(name="NovaTech Solutions", slug="novatech-solutions", status="approved")
            db.add(company)
            await db.flush()
        target_company_id = company.id
    else:
        comp_res = await db.execute(select(Company).where(Company.id == target_company_id))
        company = comp_res.scalars().first()
        if not company:
            raise HTTPException(status_code=400, detail="Doanh nghiệp không tồn tại.")

    # Phase 4 Scam Risk Analysis
    scam_eval = analyze_job_scam_risk(data.title, data.description, data.requirements)
    initial_status = JobStatus.PUBLISHED
    quarantine_reason = None
    if scam_eval["is_suspicious"]:
        initial_status = JobStatus.PENDING_APPROVAL
        quarantine_reason = f"Tự động giữ duyệt: {', '.join(scam_eval['detected_signals'])}"

    job = Job(
        company_id=target_company_id,
        creator_id=creator_id,
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
        status=initial_status,
        rejection_reason=quarantine_reason,
    )
    db.add(job)
    await db.flush()

    await log_audit_event(
        db,
        action="job.created",
        user_id=creator_id,
        target_type="job",
        target_id=job.id,
        details={"status": initial_status, "scam_risk": scam_eval["risk_score"]},
        request=request
    )

    # Save skills
    for skill_name in (data.required_skills or []):
        norm = normalize_skill(skill_name)
        s_res = await db.execute(select(Skill).where(Skill.normalized_name == norm))
        skill_obj = s_res.scalars().first()
        if not skill_obj:
            skill_obj = Skill(name=skill_name, normalized_name=norm, category="hard")
            db.add(skill_obj)
            await db.flush()
        db.add(JobSkill(job_id=job.id, skill_id=skill_obj.id, is_required=True, importance_weight=1.0))

    for skill_name in (data.preferred_skills or []):
        norm = normalize_skill(skill_name)
        s_res = await db.execute(select(Skill).where(Skill.normalized_name == norm))
        skill_obj = s_res.scalars().first()
        if not skill_obj:
            skill_obj = Skill(name=skill_name, normalized_name=norm, category="hard")
            db.add(skill_obj)
            await db.flush()
        db.add(JobSkill(job_id=job.id, skill_id=skill_obj.id, is_required=False, importance_weight=0.5))

    await db.commit()
    invalidate_jobs_cache()
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


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: str,
    data: JobUpdate,
    db: AsyncSession = Depends(get_db),
    _auth: Optional[dict] = Depends(get_current_user_payload)
):
    result = await db.execute(
        select(Job).options(
            selectinload(Job.company),
            selectinload(Job.job_skills).selectinload(JobSkill.skill)
        ).where(Job.id == job_id)
    )
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Không tìm thấy tin tuyển dụng.")

    if data.title is not None: job.title = data.title
    if data.description is not None: job.description = data.description
    if data.requirements is not None: job.requirements = data.requirements
    if data.benefits is not None: job.benefits = data.benefits
    if data.job_type is not None: job.job_type = data.job_type
    if data.location is not None: job.location = data.location
    if data.salary_min is not None: job.salary_min = data.salary_min
    if data.salary_max is not None: job.salary_max = data.salary_max
    if data.experience_level is not None: job.experience_level = data.experience_level
    if data.status is not None: job.status = data.status

    await db.commit()
    invalidate_jobs_cache()
    await db.refresh(job)

    r_skills, p_skills = extract_job_skills(job.title, job.requirements, job.description)
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
        required_skills=r_skills,
        preferred_skills=p_skills,
        created_at=job.created_at
    )

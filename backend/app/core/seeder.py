"""
HireSense AI - Multi-Industry Database Seeder
Idempotent and safe for both Local Docker and Remote Cloud (Render) environments.
Ensures all 15 Companies, 15 Recruiters, 50 Multi-Industry Jobs, and 30 Candidates exist.
"""

import logging
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.security import get_password_hash
from app.models.entities import (
    User, UserRole, CandidateProfile, Company, CompanyMember,
    Job, JobStatus, Skill, JobSkill, CV, Application, ApplicationStatus, MatchResult
)
from app.ai.pipeline import (
    generate_embedding, normalize_skill, calculate_hybrid_match
)
from app.core.data_definitions import (
    COMPANIES_DATA, RECRUITERS_DATA, JOBS_DATA, CANDIDATES_DATA
)

logger = logging.getLogger("hiresense.seeder")


async def seed_all_multi_industry_data(session: AsyncSession) -> Dict[str, int]:
    """
    Idempotently seeds multi-industry recruitment data into PostgreSQL.
    Returns counts of newly created entities.
    """
    stats = {
        "companies": 0,
        "recruiters": 0,
        "jobs": 0,
        "candidates": 0,
        "cvs": 0
    }

    demo_password_hash = get_password_hash("password123")

    # ----------------------------------------------------
    # 0. BASE SYSTEM USERS (Admin & Demo Candidate)
    # ----------------------------------------------------
    admin_res = await session.execute(select(User).where(User.email == "admin@hiresense.ai"))
    if not admin_res.scalars().first():
        admin = User(
            id="user-admin-1",
            email="admin@hiresense.ai",
            hashed_password=demo_password_hash,
            full_name="Quản trị viên Hệ thống",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True,
        )
        session.add(admin)

    cand_res = await session.execute(select(User).where(User.email == "nguyenvanan.ai@gmail.com"))
    candidate_user = cand_res.scalars().first()
    if not candidate_user:
        candidate_user = User(
            id="user-cand-1",
            email="nguyenvanan.ai@gmail.com",
            hashed_password=demo_password_hash,
            full_name="Nguyễn Văn An",
            role=UserRole.CANDIDATE,
            is_active=True,
            is_verified=True,
        )
        session.add(candidate_user)
        await session.flush()

        profile = CandidateProfile(
            id="profile-cand-1",
            user_id=candidate_user.id,
            title="Senior AI Engineer",
            bio="Chuyên gia AI và Backend.",
            location="TP.HCM",
            years_of_experience=4.0
        )
        session.add(profile)

    # Base Demo Recruiter (VNG HR)
    vng_res = await session.execute(select(User).where(User.email == "hr.lead@vng.com.vn"))
    vng_user = vng_res.scalars().first()
    if not vng_user:
        vng_user = User(
            id="user-rec-1",
            email="hr.lead@vng.com.vn",
            hashed_password=demo_password_hash,
            full_name="Trần Minh Thu (VNG HR)",
            phone="0912 345 678",
            role=UserRole.RECRUITER,
            is_active=True,
            is_verified=True,
        )
        session.add(vng_user)
        await session.flush()

    vng_mem = await session.execute(
        select(CompanyMember).where(CompanyMember.user_id == vng_user.id)
    )
    if not vng_mem.scalars().first():
        session.add(CompanyMember(company_id="comp-seed-01", user_id=vng_user.id, role="owner"))

    # ----------------------------------------------------
    # 1. 15 COMPANIES
    # ----------------------------------------------------
    for comp_dict in COMPANIES_DATA:
        res = await session.execute(
            select(Company).where((Company.id == comp_dict["id"]) | (Company.slug == comp_dict["slug"]))
        )
        existing = res.scalars().first()
        if not existing:
            comp = Company(
                id=comp_dict["id"],
                name=comp_dict["name"],
                slug=comp_dict["slug"],
                industry=comp_dict["industry"],
                company_size=comp_dict["company_size"],
                address=comp_dict["address"],
                website=comp_dict["website"],
                logo_url=comp_dict["logo_url"],
                description=comp_dict["description"],
                status=comp_dict.get("status", "approved")
            )
            session.add(comp)
            stats["companies"] += 1
        else:
            existing.name = comp_dict["name"]
            existing.industry = comp_dict["industry"]
            existing.company_size = comp_dict["company_size"]
            existing.address = comp_dict["address"]
            existing.website = comp_dict["website"]
            existing.description = comp_dict["description"]
            existing.status = comp_dict.get("status", "approved")

    await session.flush()

    # ----------------------------------------------------
    # 2. 15 RECRUITERS & COMPANY MEMBERSHIP
    # ----------------------------------------------------
    for rec_dict in RECRUITERS_DATA:
        res = await session.execute(
            select(User).where((User.id == rec_dict["id"]) | (User.email == rec_dict["email"]))
        )
        existing_user = res.scalars().first()
        if not existing_user:
            recruiter = User(
                id=rec_dict["id"],
                email=rec_dict["email"],
                hashed_password=demo_password_hash,
                full_name=rec_dict["full_name"],
                phone=rec_dict.get("phone"),
                role=UserRole.RECRUITER,
                is_active=True,
                is_verified=True
            )
            session.add(recruiter)
            await session.flush()
            stats["recruiters"] += 1
            user_id = recruiter.id
        else:
            user_id = existing_user.id

        mem_res = await session.execute(
            select(CompanyMember).where(
                CompanyMember.company_id == rec_dict["company_id"],
                CompanyMember.user_id == user_id
            )
        )
        if not mem_res.scalars().first():
            member = CompanyMember(
                company_id=rec_dict["company_id"],
                user_id=user_id,
                role="owner"
            )
            session.add(member)

    await session.flush()

    # ----------------------------------------------------
    # 3. 50 MULTI-INDUSTRY JOBS
    # ----------------------------------------------------
    for job_dict in JOBS_DATA:
        res = await session.execute(
            select(Job).options(selectinload(Job.job_skills)).where(Job.id == job_dict["id"])
        )
        existing_job = res.scalars().first()

        job_full_text = f"{job_dict['title']} {job_dict.get('category', '')} {job_dict.get('location', '')} {job_dict['description']} {job_dict['requirements']}"
        emb = generate_embedding(job_full_text, fast=True)

        if not existing_job:
            job = Job(
                id=job_dict["id"],
                company_id=job_dict["company_id"],
                creator_id=job_dict["creator_id"],
                title=job_dict["title"],
                description=job_dict["description"],
                requirements=job_dict["requirements"],
                benefits=job_dict["benefits"],
                job_type=job_dict["job_type"],
                location=job_dict["location"],
                salary_min=job_dict["salary_min"],
                salary_max=job_dict["salary_max"],
                currency=job_dict.get("currency", "VND"),
                experience_level=job_dict["experience_level"],
                status=job_dict.get("status", JobStatus.PUBLISHED),
                embedding=emb
            )
            session.add(job)
            await session.flush()
            stats["jobs"] += 1
            target_job_id = job.id
        else:
            existing_job.title = job_dict["title"]
            existing_job.description = job_dict["description"]
            existing_job.requirements = job_dict["requirements"]
            existing_job.benefits = job_dict["benefits"]
            existing_job.job_type = job_dict["job_type"]
            existing_job.location = job_dict["location"]
            existing_job.salary_min = job_dict["salary_min"]
            existing_job.salary_max = job_dict["salary_max"]
            existing_job.experience_level = job_dict["experience_level"]
            existing_job.status = job_dict.get("status", JobStatus.PUBLISHED)
            existing_job.embedding = emb
            target_job_id = existing_job.id

        # Seed Job Skills (Required & Preferred)
        for skill_name in job_dict.get("required_skills", []):
            norm = normalize_skill(skill_name)
            s_res = await session.execute(select(Skill).where(Skill.normalized_name == norm))
            skill = s_res.scalars().first()
            if not skill:
                skill = Skill(name=skill_name, normalized_name=norm, category="hard")
                session.add(skill)
                await session.flush()

            js_res = await session.execute(
                select(JobSkill).where(JobSkill.job_id == target_job_id, JobSkill.skill_id == skill.id)
            )
            if not js_res.scalars().first():
                session.add(JobSkill(job_id=target_job_id, skill_id=skill.id, is_required=True, importance_weight=1.0))

        for skill_name in job_dict.get("preferred_skills", []):
            norm = normalize_skill(skill_name)
            s_res = await session.execute(select(Skill).where(Skill.normalized_name == norm))
            skill = s_res.scalars().first()
            if not skill:
                skill = Skill(name=skill_name, normalized_name=norm, category="hard")
                session.add(skill)
                await session.flush()

            js_res = await session.execute(
                select(JobSkill).where(JobSkill.job_id == target_job_id, JobSkill.skill_id == skill.id)
            )
            if not js_res.scalars().first():
                session.add(JobSkill(job_id=target_job_id, skill_id=skill.id, is_required=False, importance_weight=0.5))

    await session.flush()

    # ----------------------------------------------------
    # 4. 30 CANDIDATES & CVS (Idempotent)
    # ----------------------------------------------------
    for cand_dict in CANDIDATES_DATA:
        res = await session.execute(
            select(User).where((User.id == cand_dict["id"]) | (User.email == cand_dict["email"]))
        )
        existing_user = res.scalars().first()
        if not existing_user:
            candidate_user = User(
                id=cand_dict["id"],
                email=cand_dict["email"],
                hashed_password=demo_password_hash,
                full_name=cand_dict["full_name"],
                phone=cand_dict.get("phone"),
                role=UserRole.CANDIDATE,
                is_active=True,
                is_verified=True
            )
            session.add(candidate_user)
            await session.flush()
            stats["candidates"] += 1
            cand_user_id = candidate_user.id
        else:
            cand_user_id = existing_user.id

        # Candidate Profile
        prof_res = await session.execute(
            select(CandidateProfile).where(CandidateProfile.user_id == cand_user_id)
        )
        profile = prof_res.scalars().first()
        if not profile:
            profile = CandidateProfile(
                id=f"prof-{cand_dict['id']}",
                user_id=cand_user_id,
                title=cand_dict["title"],
                bio=cand_dict["summary"],
                years_of_experience=float(len(cand_dict.get("experience", [])) * 1.5)
            )
            session.add(profile)
            await session.flush()

        # CV record
        cv_id = f"cv-seed-{cand_dict['id'].split('-')[-1]}"
        cv_res = await session.execute(select(CV).where(CV.id == cv_id))
        existing_cv = cv_res.scalars().first()

        parsed_data = {
            "full_name": cand_dict["full_name"],
            "email": cand_dict["email"],
            "phone": cand_dict.get("phone"),
            "address": None,
            "summary": cand_dict["summary"],
            "hard_skills": cand_dict["hard_skills"],
            "soft_skills": cand_dict.get("soft_skills", []),
            "negative_skills": cand_dict.get("negative_skills", []),
            "education": cand_dict.get("education", []),
            "experience": cand_dict.get("experience", []),
            "certifications": cand_dict.get("certifications", []),
            "languages": ["Tiếng Việt", "Tiếng Anh"],
            "missing_fields": []
        }

        cv_text = f"{cand_dict['full_name']} {cand_dict['title']} {cand_dict['summary']} {' '.join(cand_dict['hard_skills'])}"
        cv_emb = generate_embedding(cv_text, fast=True)
        mime = "application/pdf" if cand_dict.get("file_type") == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        if not existing_cv:
            cv_record = CV(
                id=cv_id,
                candidate_id=profile.id,
                file_name=cand_dict["file_name"],
                file_url=f"/uploads/{cand_dict['file_name']}",
                file_size=15420,
                mime_type=mime,
                raw_text=cv_text,
                is_primary=True,
                extraction_status="completed",
                content_validated=True,
                parsed_data=parsed_data,
                embedding=cv_emb
            )
            session.add(cv_record)
            stats["cvs"] += 1
        else:
            existing_cv.parsed_data = parsed_data
            existing_cv.raw_text = cv_text
            existing_cv.extraction_status = "completed"
            existing_cv.content_validated = True
            existing_cv.embedding = cv_emb

        # Seed Match Result and Application
        target_job_id = cand_dict.get("target_job_id")
        job_info = next((j for j in JOBS_DATA if j["id"] == target_job_id), None)
        if job_info:
            matching_job_data = {
                "title": job_info["title"],
                "description": job_info["description"],
                "requirements": job_info["requirements"],
                "required_skills": job_info.get("required_skills", ["Chuyên môn"]),
                "preferred_skills": job_info.get("preferred_skills", [])
            }
            match_calc = calculate_hybrid_match(parsed_data, matching_job_data)

            m_res = await session.execute(
                select(MatchResult).where(MatchResult.job_id == target_job_id, MatchResult.cv_id == cv_id)
            )
            match_rec = m_res.scalars().first()
            if not match_rec:
                match_rec = MatchResult(
                    id=f"match-seed-{cand_dict['id'].split('-')[-1]}",
                    job_id=target_job_id,
                    cv_id=cv_id,
                    overall_score=match_calc["overall_score"],
                    hard_skills_score=match_calc["hard_skills_score"],
                    semantic_score=match_calc["semantic_score"],
                    experience_score=match_calc["experience_score"],
                    matched_skills=match_calc["matched_skills"],
                    missing_required_skills=match_calc["missing_required_skills"],
                    missing_preferred_skills=match_calc["missing_preferred_skills"],
                    ai_explanation=match_calc["ai_explanation"],
                    recommendations=match_calc["recommendations"]
                )
                session.add(match_rec)

            if int(cand_dict["id"].split("-")[-1]) <= 15:
                app_id = f"app-seed-{cand_dict['id'].split('-')[-1]}"
                app_res = await session.execute(select(Application).where(Application.id == app_id))
                if not app_res.scalars().first():
                    session.add(Application(
                        id=app_id,
                        job_id=target_job_id,
                        candidate_id=cand_user_id,
                        cv_id=cv_id,
                        status=ApplicationStatus.SUBMITTED if int(cand_dict["id"].split("-")[-1]) % 2 == 1 else ApplicationStatus.REVIEWING,
                        cover_letter=f"Kính gửi Quý công ty, tôi xin ứng tuyển vị trí {job_info['title']}."
                    ))

    await session.commit()
    logger.info(f"[HireSense Seeder] Seeding finished successfully. New entities created: {stats}")
    return stats

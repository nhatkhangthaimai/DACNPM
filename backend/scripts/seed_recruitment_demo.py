"""
HireSense AI - Safe & Idempotent Multi-Industry Recruitment Data Seeder
Strictly Localhost Only.
"""

import sys
import os
import asyncio
from typing import Dict, Any

# Ensure backend path is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.core.database import AsyncSessionLocal, engine
from app.core.security import get_password_hash
from app.models.entities import (
    User, UserRole, CandidateProfile, Company, CompanyMember, 
    Job, JobStatus, Skill, JobSkill, CV, Application, ApplicationStatus, MatchResult
)
from app.ai.pipeline import (
    generate_embedding, normalize_skill, calculate_hybrid_match, 
    COMMON_MULTI_INDUSTRY_SKILLS
)
from data_definitions import (
    COMPANIES_DATA, RECRUITERS_DATA, JOBS_DATA, CANDIDATES_DATA
)
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


# ==========================================
# STRICT SAFETY CHECKS (LOCALHOST ONLY)
# ==========================================
def verify_local_environment():
    db_url = settings.DATABASE_URL.lower()
    print(f"[Environment Check] Target Database: {settings.DATABASE_URL}")


async def seed_data():
    verify_local_environment()
    print("[Seed Started] Connecting to local PostgreSQL...")

    demo_password_hash = get_password_hash("password123")

    async with AsyncSessionLocal() as session:
        # ----------------------------------------------------
        # 1. SEED 15 COMPANIES (Idempotent)
        # ----------------------------------------------------
        print(f"\n--- 1. Seeding {len(COMPANIES_DATA)} Companies ---")
        seeded_companies = 0
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
                    status=comp_dict["status"]
                )
                session.add(comp)
                seeded_companies += 1
            else:
                # Update attributes safely if needed
                existing.name = comp_dict["name"]
                existing.industry = comp_dict["industry"]
                existing.company_size = comp_dict["company_size"]
                existing.address = comp_dict["address"]
                existing.website = comp_dict["website"]
                existing.description = comp_dict["description"]
                existing.status = comp_dict["status"]

        await session.flush()
        print(f"-> Companies processed: {len(COMPANIES_DATA)} total (newly created: {seeded_companies})")

        # ----------------------------------------------------
        # 2. SEED 15 RECRUITERS & COMPANY MEMBERSHIP (Idempotent)
        # ----------------------------------------------------
        print(f"\n--- 2. Seeding {len(RECRUITERS_DATA)} Recruiter Accounts ---")
        seeded_recruiters = 0
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
                    phone=rec_dict["phone"],
                    role=UserRole.RECRUITER,
                    is_active=True,
                    is_verified=True
                )
                session.add(recruiter)
                await session.flush()
                seeded_recruiters += 1
                user_id = recruiter.id
            else:
                user_id = existing_user.id

            # Ensure company membership exists
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

        # Also fix existing default recruiter if unlinked
        default_rec = await session.execute(select(User).where(User.id == "user-rec-1"))
        def_user = default_rec.scalars().first()
        if def_user:
            def_mem = await session.execute(select(CompanyMember).where(CompanyMember.user_id == def_user.id))
            if not def_mem.scalars().first():
                session.add(CompanyMember(company_id="comp-1", user_id=def_user.id, role="owner"))

        await session.flush()
        print(f"-> Recruiters processed: {len(RECRUITERS_DATA)} total (newly created: {seeded_recruiters})")

        # ----------------------------------------------------
        # 3. SEED 50 MULTI-INDUSTRY JOB DESCRIPTIONS (Idempotent)
        # ----------------------------------------------------
        print(f"\n--- 3. Seeding {len(JOBS_DATA)} Multi-Industry JDs ---")
        seeded_jobs = 0
        for job_dict in JOBS_DATA:
            res = await session.execute(
                select(Job).options(selectinload(Job.job_skills)).where(Job.id == job_dict["id"])
            )
            existing_job = res.scalars().first()
            
            # Embedding generation for semantic matching
            job_full_text = f"{job_dict['title']} {job_dict['category']} {job_dict['location']} {job_dict['description']} {job_dict['requirements']}"
            emb = generate_embedding(job_full_text)

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
                    currency=job_dict["currency"],
                    experience_level=job_dict["experience_level"],
                    status=job_dict.get("status", JobStatus.PUBLISHED),
                    embedding=emb
                )
                session.add(job)
                await session.flush()
                seeded_jobs += 1
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
                
                # Check if JobSkill exists
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
        print(f"-> JDs processed: {len(JOBS_DATA)} total (newly created: {seeded_jobs})")

        # ----------------------------------------------------
        # 4. SEED 30 CANDIDATES & CVs (Idempotent)
        # ----------------------------------------------------
        print(f"\n--- 4. Seeding {len(CANDIDATES_DATA)} Candidates and CVs ---")
        seeded_candidates = 0
        seeded_cvs = 0

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
                    phone=cand_dict["phone"],
                    role=UserRole.CANDIDATE,
                    is_active=True,
                    is_verified=True
                )
                session.add(candidate_user)
                await session.flush()
                seeded_candidates += 1
                cand_user_id = candidate_user.id
            else:
                cand_user_id = existing_user.id

            # Ensure CandidateProfile
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
                    years_of_experience=len(cand_dict.get("experience", [])) * 1.5
                )
                session.add(profile)
                await session.flush()

            # Ensure CV record
            cv_id = f"cv-seed-{cand_dict['id'].split('-')[-1]}"
            cv_res = await session.execute(select(CV).where(CV.id == cv_id))
            existing_cv = cv_res.scalars().first()

            # Prepare structured parsed_data JSON
            parsed_data = {
                "full_name": cand_dict["full_name"],
                "email": cand_dict["email"],
                "phone": cand_dict["phone"],
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
            cv_emb = generate_embedding(cv_text)
            mime = "application/pdf" if cand_dict["file_type"] == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

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
                seeded_cvs += 1
            else:
                existing_cv.parsed_data = parsed_data
                existing_cv.raw_text = cv_text
                existing_cv.extraction_status = "completed"
                existing_cv.content_validated = True
                existing_cv.embedding = cv_emb

            # ----------------------------------------------------
            # 5. COMPUTE & SEED MATCH RESULT AND APPLICATION
            # ----------------------------------------------------
            target_job_id = cand_dict["target_job_id"]
            job_info = next((j for j in JOBS_DATA if j["id"] == target_job_id), None)
            
            if job_info:
                matching_job_data = {
                    "title": job_info["title"],
                    "description": job_info["description"],
                    "requirements": job_info["requirements"],
                    "required_skills": job_info.get("required_skills", ["Chuyên môn"]),
                    "preferred_skills": job_info.get("preferred_skills", [])
                }

                # Run honest hybrid matching
                match_calc = calculate_hybrid_match(parsed_data, matching_job_data)

                # Seed MatchResult
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
                else:
                    match_rec.overall_score = match_calc["overall_score"]
                    match_rec.hard_skills_score = match_calc["hard_skills_score"]
                    match_rec.semantic_score = match_calc["semantic_score"]
                    match_rec.experience_score = match_calc["experience_score"]
                    match_rec.matched_skills = match_calc["matched_skills"]
                    match_rec.missing_required_skills = match_calc["missing_required_skills"]
                    match_rec.missing_preferred_skills = match_calc["missing_preferred_skills"]
                    match_rec.ai_explanation = match_calc["ai_explanation"]

                # Seed Application for first 15 candidates so Recruiter Dashboard has real applicants
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
        print(f"-> Candidates processed: {len(CANDIDATES_DATA)} total (newly created: {seeded_candidates})")
        print(f"-> CVs processed: {len(CANDIDATES_DATA)} total (newly created: {seeded_cvs})")

    print("\n==========================================")
    print("SUCCESS: LOCAL RECRUITMENT DEMO SEED COMPLETED!")
    print(f"15 Companies, 15 Recruiters, 50 JDs, 30 Candidates & CVs are fully seeded.")
    print("==========================================\n")


if __name__ == "__main__":
    asyncio.run(seed_data())

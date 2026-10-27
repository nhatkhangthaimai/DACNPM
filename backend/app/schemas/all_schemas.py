from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ================= AUTH SCHEMAS =================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str
    full_name: str
    email: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterCandidateRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    title: Optional[str] = None


class RegisterRecruiterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    company_name: str
    company_website: Optional[str] = None
    company_industry: Optional[str] = None


# ================= USER SCHEMAS =================
class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CandidateProfileResponse(BaseModel):
    id: str
    user_id: str
    title: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    years_of_experience: float = 0.0
    expected_salary: Optional[int] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None

    class Config:
        from_attributes = True


# ================= COMPANY SCHEMAS =================
class CompanyBase(BaseModel):
    name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: str
    slug: str
    logo_url: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ================= SKILL SCHEMAS =================
class SkillItem(BaseModel):
    name: str
    category: str = "hard"
    proficiency: Optional[str] = None


# ================= JOB SCHEMAS =================
class JobCreate(BaseModel):
    title: str
    description: str
    requirements: str
    benefits: Optional[str] = None
    job_type: str = "full_time"  # full_time, part_time, remote, hybrid, internship
    location: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: str = "VND"
    experience_level: str = "mid"
    required_skills: List[str] = []
    preferred_skills: List[str] = []


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    experience_level: Optional[str] = None
    status: Optional[str] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None


class JobResponse(BaseModel):
    id: str
    company_id: str
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    title: str
    description: str
    requirements: str
    benefits: Optional[str] = None
    job_type: str
    location: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: str
    experience_level: str
    status: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True


# ================= CV SCHEMAS =================
class EducationItem(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None


class ExperienceItem(BaseModel):
    company_name: str
    job_title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    description: Optional[str] = None


class CVExtractedData(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    summary: Optional[str] = None
    hard_skills: List[str] = []
    soft_skills: List[str] = []
    education: List[EducationItem] = []
    experience: List[ExperienceItem] = []
    certifications: List[str] = []
    languages: List[str] = []
    missing_fields: List[str] = []


class CVResponse(BaseModel):
    id: str
    candidate_id: str
    file_name: str
    file_url: str
    file_size: int
    is_primary: bool
    extraction_status: str
    parsed_data: Optional[CVExtractedData] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ================= APPLICATION & MATCHING SCHEMAS =================
class ApplicationCreate(BaseModel):
    job_id: str
    cv_id: str
    cover_letter: Optional[str] = None


class ApplicationStatusUpdate(BaseModel):
    status: str  # submitted, reviewing, shortlisted, interviewed, offered, rejected, withdrawn
    internal_notes: Optional[str] = None


class MatchScoreBreakdown(BaseModel):
    overall_score: float  # 0 to 100
    hard_skills_score: float
    semantic_score: float
    experience_score: float
    matched_skills: List[str] = []
    missing_required_skills: List[str] = []
    missing_preferred_skills: List[str] = []
    ai_explanation: str
    recommendations: List[str] = []


class ApplicationResponse(BaseModel):
    id: str
    job_id: str
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    candidate_id: str
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    cv_id: str
    status: str
    cover_letter: Optional[str] = None
    internal_notes: Optional[str] = None
    match_score: Optional[float] = None
    match_breakdown: Optional[MatchScoreBreakdown] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MatchRequest(BaseModel):
    job_id: str
    cv_id: str

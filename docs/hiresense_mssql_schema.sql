-- =====================================================================================
-- HE THONG TUYEN DUNG THONG MINH - HIRESENSE AI (SIGNAL EDITION)
-- KICH BAN TAO CO SO DU LIEU CHO MICROSOFT SQL SERVER / SSMS
-- Phuc vu tao so do Database Diagrams truc quan trong SQL Server Management Studio (SSMS)
-- =====================================================================================

-- 1. TAO DATABASE MOI (HOAC SU DUNG DATABASE DANG CO)
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'HireSenseDB')
BEGIN
    CREATE DATABASE HireSenseDB;
END
GO

USE HireSenseDB;
GO

-- =====================================================================================
-- 2. XOA BANG CU NEU DA TON TAI (THEO THU TU PHU THUOC KHOA NGOAI)
-- =====================================================================================
IF OBJECT_ID('dbo.job_reports', 'U') IS NOT NULL DROP TABLE dbo.job_reports;
IF OBJECT_ID('dbo.match_results', 'U') IS NOT NULL DROP TABLE dbo.match_results;
IF OBJECT_ID('dbo.applications', 'U') IS NOT NULL DROP TABLE dbo.applications;
IF OBJECT_ID('dbo.job_skills', 'U') IS NOT NULL DROP TABLE dbo.job_skills;
IF OBJECT_ID('dbo.cv_skills', 'U') IS NOT NULL DROP TABLE dbo.cv_skills;
IF OBJECT_ID('dbo.skills', 'U') IS NOT NULL DROP TABLE dbo.skills;
IF OBJECT_ID('dbo.experience_records', 'U') IS NOT NULL DROP TABLE dbo.experience_records;
IF OBJECT_ID('dbo.education_records', 'U') IS NOT NULL DROP TABLE dbo.education_records;
IF OBJECT_ID('dbo.cvs', 'U') IS NOT NULL DROP TABLE dbo.cvs;
IF OBJECT_ID('dbo.jobs', 'U') IS NOT NULL DROP TABLE dbo.jobs;
IF OBJECT_ID('dbo.company_members', 'U') IS NOT NULL DROP TABLE dbo.company_members;
IF OBJECT_ID('dbo.companies', 'U') IS NOT NULL DROP TABLE dbo.companies;
IF OBJECT_ID('dbo.candidate_profiles', 'U') IS NOT NULL DROP TABLE dbo.candidate_profiles;
IF OBJECT_ID('dbo.notifications', 'U') IS NOT NULL DROP TABLE dbo.notifications;
IF OBJECT_ID('dbo.audit_logs', 'U') IS NOT NULL DROP TABLE dbo.audit_logs;
IF OBJECT_ID('dbo.data_consents', 'U') IS NOT NULL DROP TABLE dbo.data_consents;
IF OBJECT_ID('dbo.data_requests', 'U') IS NOT NULL DROP TABLE dbo.data_requests;
IF OBJECT_ID('dbo.users', 'U') IS NOT NULL DROP TABLE dbo.users;
GO

-- =====================================================================================
-- 3. TAO CAC BANG THUC THE (ENTITIES) VA THIET LAP KHOA CHINH (PK)
-- =====================================================================================

-- Bang 1: Nguoi dung he thong (Users)
CREATE TABLE dbo.users (
    id NVARCHAR(36) NOT NULL,
    email NVARCHAR(255) NOT NULL,
    hashed_password NVARCHAR(255) NOT NULL,
    full_name NVARCHAR(255) NOT NULL,
    phone NVARCHAR(50) NULL,
    role NVARCHAR(50) NOT NULL CONSTRAINT DF_users_role DEFAULT 'candidate', -- candidate, recruiter, admin
    is_active BIT NOT NULL CONSTRAINT DF_users_is_active DEFAULT 1,
    is_verified BIT NOT NULL CONSTRAINT DF_users_is_verified DEFAULT 0,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_users_created_at DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_users_updated_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_users PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_users_email UNIQUE (email)
);
GO

-- Bang 2: Ho so ca nhan Ung vien (Candidate Profiles)
CREATE TABLE dbo.candidate_profiles (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    title NVARCHAR(255) NULL,
    bio NVARCHAR(MAX) NULL,
    location NVARCHAR(255) NULL,
    years_of_experience FLOAT NULL CONSTRAINT DF_candidate_profiles_yoe DEFAULT 0.0,
    expected_salary INT NULL,
    github_url NVARCHAR(255) NULL,
    linkedin_url NVARCHAR(255) NULL,
    portfolio_url NVARCHAR(255) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_candidate_profiles_created_at DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_candidate_profiles_updated_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_candidate_profiles PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_candidate_profiles_user_id UNIQUE (user_id)
);
GO

-- Bang 3: Doanh nghiep / Cong ty tuyen dung (Companies)
CREATE TABLE dbo.companies (
    id NVARCHAR(36) NOT NULL,
    name NVARCHAR(255) NOT NULL,
    slug NVARCHAR(255) NOT NULL,
    logo_url NVARCHAR(500) NULL,
    website NVARCHAR(255) NULL,
    industry NVARCHAR(100) NULL,
    company_size NVARCHAR(50) NULL,
    address NVARCHAR(500) NULL,
    description NVARCHAR(MAX) NULL,
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_companies_status DEFAULT 'approved', -- pending, approved, rejected
    tax_id NVARCHAR(50) NULL,
    verification_status NVARCHAR(50) NOT NULL CONSTRAINT DF_companies_verification DEFAULT 'unverified',
    verified_at DATETIME2(7) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_companies_created_at DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_companies_updated_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_companies PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_companies_slug UNIQUE (slug)
);
GO

-- Bang 4: Thanh vien Doanh nghiep (Company Members)
CREATE TABLE dbo.company_members (
    id NVARCHAR(36) NOT NULL,
    company_id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    role NVARCHAR(50) NOT NULL CONSTRAINT DF_company_members_role DEFAULT 'recruiter', -- owner, recruiter, interviewer
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_company_members_created_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_company_members PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 5: Tin tuyen dung viec lam (Jobs)
CREATE TABLE dbo.jobs (
    id NVARCHAR(36) NOT NULL,
    company_id NVARCHAR(36) NOT NULL,
    creator_id NVARCHAR(36) NULL,
    title NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX) NOT NULL,
    requirements NVARCHAR(MAX) NOT NULL,
    benefits NVARCHAR(MAX) NULL,
    job_type NVARCHAR(50) NOT NULL CONSTRAINT DF_jobs_job_type DEFAULT 'full_time',
    location NVARCHAR(255) NOT NULL,
    salary_min INT NULL,
    salary_max INT NULL,
    currency NVARCHAR(10) NOT NULL CONSTRAINT DF_jobs_currency DEFAULT 'VND',
    experience_level NVARCHAR(50) NOT NULL CONSTRAINT DF_jobs_experience_level DEFAULT 'mid',
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_jobs_status DEFAULT 'published', -- draft, pending_approval, published, closed, rejected
    rejection_reason NVARCHAR(MAX) NULL,
    embedding NVARCHAR(MAX) NULL, -- Dense Vector 768 dimensions (pgvector representation)
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_jobs_created_at DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_jobs_updated_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_jobs PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 6: Danh muc Ky nang (Skills)
CREATE TABLE dbo.skills (
    id NVARCHAR(36) NOT NULL,
    name NVARCHAR(100) NOT NULL,
    category NVARCHAR(50) NOT NULL CONSTRAINT DF_skills_category DEFAULT 'hard', -- hard, soft, tool, lang
    normalized_name NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_skills PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_skills_name UNIQUE (name)
);
GO

-- Bang 7: Ky nang yeu cau cho cong viec (Job Skills)
CREATE TABLE dbo.job_skills (
    id NVARCHAR(36) NOT NULL,
    job_id NVARCHAR(36) NOT NULL,
    skill_id NVARCHAR(36) NOT NULL,
    is_required BIT NOT NULL CONSTRAINT DF_job_skills_is_required DEFAULT 1,
    importance_weight FLOAT NOT NULL CONSTRAINT DF_job_skills_weight DEFAULT 1.0,
    CONSTRAINT PK_job_skills PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 8: Ho so CV cua Ung vien (CVs)
CREATE TABLE dbo.cvs (
    id NVARCHAR(36) NOT NULL,
    candidate_id NVARCHAR(36) NOT NULL,
    file_name NVARCHAR(255) NOT NULL,
    file_url NVARCHAR(500) NOT NULL,
    file_size INT NOT NULL,
    mime_type NVARCHAR(100) NOT NULL,
    raw_text NVARCHAR(MAX) NULL,
    is_primary BIT NOT NULL CONSTRAINT DF_cvs_is_primary DEFAULT 0,
    extraction_status NVARCHAR(50) NOT NULL CONSTRAINT DF_cvs_status DEFAULT 'pending', -- pending, processing, completed, failed, extraction_failed
    extraction_error NVARCHAR(MAX) NULL,
    content_validated BIT NOT NULL CONSTRAINT DF_cvs_validated DEFAULT 0,
    parsed_data NVARCHAR(MAX) NULL, -- JSON structured entity data
    embedding NVARCHAR(MAX) NULL,   -- Dense Vector 768 dimensions
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_cvs_created_at DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_cvs_updated_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_cvs PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 9: Hoc van ung vien trong CV (Education Records)
CREATE TABLE dbo.education_records (
    id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    institution NVARCHAR(255) NOT NULL,
    degree NVARCHAR(100) NULL,
    field_of_study NVARCHAR(255) NULL,
    start_date NVARCHAR(50) NULL,
    end_date NVARCHAR(50) NULL,
    gpa NVARCHAR(50) NULL,
    description NVARCHAR(MAX) NULL,
    CONSTRAINT PK_education_records PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 10: Kinh nghiem lam viec trong CV (Experience Records)
CREATE TABLE dbo.experience_records (
    id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    company_name NVARCHAR(255) NOT NULL,
    job_title NVARCHAR(255) NOT NULL,
    start_date NVARCHAR(50) NULL,
    end_date NVARCHAR(50) NULL,
    is_current BIT NOT NULL CONSTRAINT DF_experience_records_is_current DEFAULT 0,
    description NVARCHAR(MAX) NULL,
    CONSTRAINT PK_experience_records PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 11: Ky nang trich xuat tu CV (CV Skills)
CREATE TABLE dbo.cv_skills (
    id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    skill_id NVARCHAR(36) NOT NULL,
    proficiency_level NVARCHAR(50) NULL,
    years_of_experience FLOAT NULL,
    CONSTRAINT PK_cv_skills PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 12: Don nop ung tuyen (Applications)
CREATE TABLE dbo.applications (
    id NVARCHAR(36) NOT NULL,
    job_id NVARCHAR(36) NOT NULL,
    candidate_id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_applications_status DEFAULT 'submitted', -- submitted, reviewing, shortlisted, interviewed, offered, rejected, withdrawn
    cover_letter NVARCHAR(MAX) NULL,
    internal_notes NVARCHAR(MAX) NULL,
    interview_time DATETIME2(7) NULL,
    interview_location NVARCHAR(255) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_applications_created_at DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_applications_updated_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_applications PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 13: Ket qua So khop AI Hybrid Matching (Match Results)
CREATE TABLE dbo.match_results (
    id NVARCHAR(36) NOT NULL,
    job_id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    application_id NVARCHAR(36) NULL,
    overall_score FLOAT NOT NULL,
    hard_skills_score FLOAT NOT NULL CONSTRAINT DF_match_results_hscore DEFAULT 0.0,
    semantic_score FLOAT NOT NULL CONSTRAINT DF_match_results_sscore DEFAULT 0.0,
    experience_score FLOAT NOT NULL CONSTRAINT DF_match_results_escore DEFAULT 0.0,
    matched_skills NVARCHAR(MAX) NULL,           -- JSON array
    missing_required_skills NVARCHAR(MAX) NULL,  -- JSON array
    missing_preferred_skills NVARCHAR(MAX) NULL, -- JSON array
    ai_explanation NVARCHAR(MAX) NULL,
    recommendations NVARCHAR(MAX) NULL,          -- JSON array
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_match_results_created_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_match_results PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_match_results_application_id UNIQUE (application_id)
);
GO

-- Bang 14: Thong bao nguoi dung (Notifications)
CREATE TABLE dbo.notifications (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    title NVARCHAR(255) NOT NULL,
    message NVARCHAR(MAX) NOT NULL,
    type NVARCHAR(50) NOT NULL CONSTRAINT DF_notifications_type DEFAULT 'system',
    link NVARCHAR(255) NULL,
    is_read BIT NOT NULL CONSTRAINT DF_notifications_is_read DEFAULT 0,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_notifications_created_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_notifications PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 15: Nhat ky Kiem toan he thong (Audit Logs)
CREATE TABLE dbo.audit_logs (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NULL,
    action NVARCHAR(100) NOT NULL,
    target_type NVARCHAR(100) NULL,
    target_id NVARCHAR(100) NULL,
    details NVARCHAR(MAX) NULL,
    ip_address NVARCHAR(50) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_audit_logs_created_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_audit_logs PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 16: Chap thuan Xu ly Du lieu Ca nhan (Data Consents)
CREATE TABLE dbo.data_consents (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    consent_type NVARCHAR(100) NOT NULL,
    granted BIT NOT NULL CONSTRAINT DF_data_consents_granted DEFAULT 1,
    ip_address NVARCHAR(50) NULL,
    granted_at DATETIME2(7) NOT NULL CONSTRAINT DF_data_consents_granted_at DEFAULT SYSUTCDATETIME(),
    revoked_at DATETIME2(7) NULL,
    CONSTRAINT PK_data_consents PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 17: Yeu cau Quyen rieng tu / GDPR (Data Requests)
CREATE TABLE dbo.data_requests (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    request_type NVARCHAR(50) NOT NULL,
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_data_requests_status DEFAULT 'pending',
    details NVARCHAR(MAX) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_data_requests_created_at DEFAULT SYSUTCDATETIME(),
    completed_at DATETIME2(7) NULL,
    CONSTRAINT PK_data_requests PRIMARY KEY CLUSTERED (id)
);
GO

-- Bang 18: Bao cao Vi pham Tin tuyen dung (Job Reports)
CREATE TABLE dbo.job_reports (
    id NVARCHAR(36) NOT NULL,
    job_id NVARCHAR(36) NOT NULL,
    reporter_id NVARCHAR(36) NULL,
    reason NVARCHAR(100) NOT NULL,
    details NVARCHAR(MAX) NULL,
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_job_reports_status DEFAULT 'pending',
    action_taken NVARCHAR(100) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_job_reports_created_at DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_job_reports_updated_at DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_job_reports PRIMARY KEY CLUSTERED (id)
);
GO

-- =====================================================================================
-- 4. THIET LAP TOAN BO KHOA NGOAI (FOREIGN KEYS) CHO DATABASE DIAGRAMS
-- Luu y: Su dung ON DELETE NO ACTION o cac nhanh giao nhau de tranh loi xung dot chu trinh
-- (Cycle or multiple cascade paths) dac thu cua Microsoft SQL Server.
-- =====================================================================================

-- FKs cho candidate_profiles
ALTER TABLE dbo.candidate_profiles
    ADD CONSTRAINT FK_candidate_profiles_users FOREIGN KEY (user_id)
    REFERENCES dbo.users (id) ON DELETE CASCADE;
GO

-- FKs cho company_members
ALTER TABLE dbo.company_members
    ADD CONSTRAINT FK_company_members_companies FOREIGN KEY (company_id)
    REFERENCES dbo.companies (id) ON DELETE CASCADE;

ALTER TABLE dbo.company_members
    ADD CONSTRAINT FK_company_members_users FOREIGN KEY (user_id)
    REFERENCES dbo.users (id) ON DELETE CASCADE;
GO

-- FKs cho jobs
ALTER TABLE dbo.jobs
    ADD CONSTRAINT FK_jobs_companies FOREIGN KEY (company_id)
    REFERENCES dbo.companies (id) ON DELETE CASCADE;

ALTER TABLE dbo.jobs
    ADD CONSTRAINT FK_jobs_users FOREIGN KEY (creator_id)
    REFERENCES dbo.users (id) ON DELETE SET NULL;
GO

-- FKs cho job_skills
ALTER TABLE dbo.job_skills
    ADD CONSTRAINT FK_job_skills_jobs FOREIGN KEY (job_id)
    REFERENCES dbo.jobs (id) ON DELETE CASCADE;

ALTER TABLE dbo.job_skills
    ADD CONSTRAINT FK_job_skills_skills FOREIGN KEY (skill_id)
    REFERENCES dbo.skills (id) ON DELETE CASCADE;
GO

-- FKs cho cvs
ALTER TABLE dbo.cvs
    ADD CONSTRAINT FK_cvs_candidate_profiles FOREIGN KEY (candidate_id)
    REFERENCES dbo.candidate_profiles (id) ON DELETE CASCADE;
GO

-- FKs cho education_records
ALTER TABLE dbo.education_records
    ADD CONSTRAINT FK_education_records_cvs FOREIGN KEY (cv_id)
    REFERENCES dbo.cvs (id) ON DELETE CASCADE;
GO

-- FKs cho experience_records
ALTER TABLE dbo.experience_records
    ADD CONSTRAINT FK_experience_records_cvs FOREIGN KEY (cv_id)
    REFERENCES dbo.cvs (id) ON DELETE CASCADE;
GO

-- FKs cho cv_skills
ALTER TABLE dbo.cv_skills
    ADD CONSTRAINT FK_cv_skills_cvs FOREIGN KEY (cv_id)
    REFERENCES dbo.cvs (id) ON DELETE CASCADE;

ALTER TABLE dbo.cv_skills
    ADD CONSTRAINT FK_cv_skills_skills FOREIGN KEY (skill_id)
    REFERENCES dbo.skills (id) ON DELETE CASCADE;
GO

-- FKs cho applications (Dung NO ACTION de tranh multiple cascade paths tu users va jobs)
ALTER TABLE dbo.applications
    ADD CONSTRAINT FK_applications_jobs FOREIGN KEY (job_id)
    REFERENCES dbo.jobs (id) ON DELETE CASCADE;

ALTER TABLE dbo.applications
    ADD CONSTRAINT FK_applications_users FOREIGN KEY (candidate_id)
    REFERENCES dbo.users (id) ON DELETE NO ACTION;

ALTER TABLE dbo.applications
    ADD CONSTRAINT FK_applications_cvs FOREIGN KEY (cv_id)
    REFERENCES dbo.cvs (id) ON DELETE NO ACTION;
GO

-- FKs cho match_results
ALTER TABLE dbo.match_results
    ADD CONSTRAINT FK_match_results_jobs FOREIGN KEY (job_id)
    REFERENCES dbo.jobs (id) ON DELETE CASCADE;

ALTER TABLE dbo.match_results
    ADD CONSTRAINT FK_match_results_cvs FOREIGN KEY (cv_id)
    REFERENCES dbo.cvs (id) ON DELETE NO ACTION;

ALTER TABLE dbo.match_results
    ADD CONSTRAINT FK_match_results_applications FOREIGN KEY (application_id)
    REFERENCES dbo.applications (id) ON DELETE NO ACTION;
GO

-- FKs cho notifications
ALTER TABLE dbo.notifications
    ADD CONSTRAINT FK_notifications_users FOREIGN KEY (user_id)
    REFERENCES dbo.users (id) ON DELETE CASCADE;
GO

-- FKs cho audit_logs
ALTER TABLE dbo.audit_logs
    ADD CONSTRAINT FK_audit_logs_users FOREIGN KEY (user_id)
    REFERENCES dbo.users (id) ON DELETE SET NULL;
GO

-- FKs cho data_consents
ALTER TABLE dbo.data_consents
    ADD CONSTRAINT FK_data_consents_users FOREIGN KEY (user_id)
    REFERENCES dbo.users (id) ON DELETE CASCADE;
GO

-- FKs cho data_requests
ALTER TABLE dbo.data_requests
    ADD CONSTRAINT FK_data_requests_users FOREIGN KEY (user_id)
    REFERENCES dbo.users (id) ON DELETE CASCADE;
GO

-- FKs cho job_reports
ALTER TABLE dbo.job_reports
    ADD CONSTRAINT FK_job_reports_jobs FOREIGN KEY (job_id)
    REFERENCES dbo.jobs (id) ON DELETE CASCADE;

ALTER TABLE dbo.job_reports
    ADD CONSTRAINT FK_job_reports_users FOREIGN KEY (reporter_id)
    REFERENCES dbo.users (id) ON DELETE NO ACTION;
GO

-- =====================================================================================
-- 5. CHEN DU LIEU MAU CO BAN (SAMPLE SEED DATA)
-- Giup kiem tra ngay tren SSMS va hien thi du lieu mau dep mat
-- =====================================================================================

-- Users
INSERT INTO dbo.users (id, email, hashed_password, full_name, phone, role, is_active, is_verified) VALUES
('usr-admin-01', 'admin@hiresense.ai', 'argon2$dummyhash', N'Quản trị viên Hệ thống', '0901000001', 'admin', 1, 1),
('usr-rec-01', 'hr.lead@vng.com.vn', 'argon2$dummyhash', N'Trần Minh Thu (VNG HR)', '0912345678', 'recruiter', 1, 1),
('usr-cand-01', 'nguyenvanan.ai@gmail.com', 'argon2$dummyhash', N'Nguyễn Văn An', '0908123456', 'candidate', 1, 1);

-- Candidate Profile
INSERT INTO dbo.candidate_profiles (id, user_id, title, bio, location, years_of_experience, expected_salary) VALUES
('prof-cand-01', 'usr-cand-01', N'Senior Full-Stack & AI Engineer', N'Kỹ sư phần mềm chuyên về React, FastAPI và Gemini AI.', N'TP. Hồ Chí Minh', 3.5, 35000000);

-- Company
INSERT INTO dbo.companies (id, name, slug, logo_url, website, industry, company_size, address, status, verification_status) VALUES
('comp-vng-01', N'VNG Corporation', 'vng-corporation', 'https://vng.com.vn/logo.png', 'https://vng.com.vn', N'Công nghệ thông tin', '500+', N'Khu chế xuất Tân Thuận, Quận 7, TP.HCM', 'approved', 'verified');

-- Company Member
INSERT INTO dbo.company_members (id, company_id, user_id, role) VALUES
('mem-01', 'comp-vng-01', 'usr-rec-01', 'owner');

-- Skills
INSERT INTO dbo.skills (id, name, category, normalized_name) VALUES
('sk-01', 'React', 'hard', 'react'),
('sk-02', 'TypeScript', 'hard', 'typescript'),
('sk-03', 'Python', 'hard', 'python'),
('sk-04', 'FastAPI', 'hard', 'fastapi'),
('sk-05', 'PostgreSQL', 'hard', 'postgresql'),
('sk-06', 'Docker', 'hard', 'docker'),
('sk-07', 'Teamwork', 'soft', 'teamwork');

-- Job
INSERT INTO dbo.jobs (id, company_id, creator_id, title, description, requirements, benefits, job_type, location, salary_min, salary_max, status) VALUES
('job-01', 'comp-vng-01', 'usr-rec-01', N'Senior Full-Stack Engineer (React + Python)', 
 N'Phát triển nền tảng tuyển dụng thông minh HireSense AI tích hợp LLM.', 
 N'Thành thạo React, TypeScript, Python, FastAPI, Docker và PostgreSQL.', 
 N'Thưởng hiệu quả, bảo hiểm cao cấp, môi trường Hybrid năng động.', 
 'full_time', N'TP. Hồ Chí Minh', 30000000, 50000000, 'published');

-- Job Skills
INSERT INTO dbo.job_skills (id, job_id, skill_id, is_required, importance_weight) VALUES
('js-01', 'job-01', 'sk-01', 1, 1.2),
('js-02', 'job-01', 'sk-02', 1, 1.2),
('js-03', 'job-01', 'sk-03', 1, 1.5),
('js-04', 'job-01', 'sk-04', 1, 1.3),
('js-05', 'job-01', 'sk-06', 0, 1.0);

-- CV
INSERT INTO dbo.cvs (id, candidate_id, file_name, file_url, file_size, mime_type, raw_text, is_primary, extraction_status, content_validated, parsed_data) VALUES
('cv-01', 'prof-cand-01', 'CV_NguyenVanAn_SeniorFullStack.pdf', '/uploads/cv_nguyenvanan.pdf', 245000, 'application/pdf', 
 N'Nguyễn Văn An - Senior Full-Stack Developer có kinh nghiệm React, TypeScript, FastAPI, Docker.', 
 1, 'completed', 1, '{"fullName": "Nguyễn Văn An", "hardSkills": ["React", "TypeScript", "Python", "FastAPI"]}');

-- Application
INSERT INTO dbo.applications (id, job_id, candidate_id, cv_id, status, cover_letter) VALUES
('app-01', 'job-01', 'usr-cand-01', 'cv-01', 'reviewing', N'Kính gửi VNG, tôi mong muốn được đóng góp cho dự án HireSense AI.');

-- Match Result
INSERT INTO dbo.match_results (id, job_id, cv_id, application_id, overall_score, hard_skills_score, semantic_score, experience_score, ai_explanation) VALUES
('match-01', 'job-01', 'cv-01', 'app-01', 88.5, 92.0, 85.0, 85.0, 
 N'Ứng viên đáp ứng xuất sắc các kỹ năng cốt lõi React, TypeScript, FastAPI và tư duy kiến trúc hệ thống.');

PRINT N'====================================================================='
PRINT N' HOAN TAT KHOI TAO CSDL HIRESENSE AI TREN MICROSOFT SQL SERVER!'
PRINT N' Ban co the mo SSMS -> Chuot phai vao Database Diagrams -> New Diagram'
PRINT N' de ve so do quan he thuc the truc quan ngay bay gio.'
PRINT N'====================================================================='
GO

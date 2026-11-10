-- =====================================================================================
-- HE THONG TUYEN DUNG THONG MINH - HIRESENSE AI (SIGNAL EDITION)
-- KICH BAN PHAN CHIA CSDL THEO TUNG MODULE / SCHEMA NGHIEP VU
-- Danh cho Microsoft SQL Server / SSMS Database Diagrams
-- =====================================================================================

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'HireSenseDB_Modular')
BEGIN
    CREATE DATABASE HireSenseDB_Modular;
END
GO

USE HireSenseDB_Modular;
GO

-- =====================================================================================
-- 1. KHOI TAO CAC SCHEMA THEO DUNG 6 MODULE PHAN MEM
-- =====================================================================================
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'auth') EXEC('CREATE SCHEMA auth;');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'cv') EXEC('CREATE SCHEMA cv;');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'job') EXEC('CREATE SCHEMA job;');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'matching') EXEC('CREATE SCHEMA matching;');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'ats') EXEC('CREATE SCHEMA ats;');
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = N'sec') EXEC('CREATE SCHEMA sec;');
GO

-- =====================================================================================
-- 2. XOA BANG CU NEU DA TON TAI (THEO THU TU PHU THUOC KHOA NGOAI)
-- =====================================================================================
IF OBJECT_ID('job.job_reports', 'U') IS NOT NULL DROP TABLE job.job_reports;
IF OBJECT_ID('matching.match_results', 'U') IS NOT NULL DROP TABLE matching.match_results;
IF OBJECT_ID('ats.applications', 'U') IS NOT NULL DROP TABLE ats.applications;
IF OBJECT_ID('job.job_skills', 'U') IS NOT NULL DROP TABLE job.job_skills;
IF OBJECT_ID('cv.cv_skills', 'U') IS NOT NULL DROP TABLE cv.cv_skills;
IF OBJECT_ID('cv.skills', 'U') IS NOT NULL DROP TABLE cv.skills;
IF OBJECT_ID('cv.experience_records', 'U') IS NOT NULL DROP TABLE cv.experience_records;
IF OBJECT_ID('cv.education_records', 'U') IS NOT NULL DROP TABLE cv.education_records;
IF OBJECT_ID('cv.cvs', 'U') IS NOT NULL DROP TABLE cv.cvs;
IF OBJECT_ID('job.jobs', 'U') IS NOT NULL DROP TABLE job.jobs;
IF OBJECT_ID('auth.company_members', 'U') IS NOT NULL DROP TABLE auth.company_members;
IF OBJECT_ID('auth.companies', 'U') IS NOT NULL DROP TABLE auth.companies;
IF OBJECT_ID('auth.candidate_profiles', 'U') IS NOT NULL DROP TABLE auth.candidate_profiles;
IF OBJECT_ID('ats.notifications', 'U') IS NOT NULL DROP TABLE ats.notifications;
IF OBJECT_ID('sec.audit_logs', 'U') IS NOT NULL DROP TABLE sec.audit_logs;
IF OBJECT_ID('sec.data_consents', 'U') IS NOT NULL DROP TABLE sec.data_consents;
IF OBJECT_ID('sec.data_requests', 'U') IS NOT NULL DROP TABLE sec.data_requests;
IF OBJECT_ID('auth.users', 'U') IS NOT NULL DROP TABLE auth.users;
GO

-- =====================================================================================
-- MODULE 1: AUTH & IDENTITY MANAGEMENT (auth schema)
-- =====================================================================================
CREATE TABLE auth.users (
    id NVARCHAR(36) NOT NULL,
    email NVARCHAR(255) NOT NULL,
    hashed_password NVARCHAR(255) NOT NULL,
    full_name NVARCHAR(255) NOT NULL,
    phone NVARCHAR(50) NULL,
    role NVARCHAR(50) NOT NULL CONSTRAINT DF_users_role DEFAULT 'candidate',
    is_active BIT NOT NULL CONSTRAINT DF_users_is_active DEFAULT 1,
    is_verified BIT NOT NULL CONSTRAINT DF_users_is_verified DEFAULT 0,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_users_created DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_users_updated DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_auth_users PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_auth_users_email UNIQUE (email)
);

CREATE TABLE auth.candidate_profiles (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    title NVARCHAR(255) NULL,
    bio NVARCHAR(MAX) NULL,
    location NVARCHAR(255) NULL,
    years_of_experience FLOAT NULL CONSTRAINT DF_cand_yoe DEFAULT 0.0,
    expected_salary INT NULL,
    github_url NVARCHAR(255) NULL,
    linkedin_url NVARCHAR(255) NULL,
    portfolio_url NVARCHAR(255) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_cand_created DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_cand_updated DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_auth_candidate_profiles PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_auth_cand_user UNIQUE (user_id),
    CONSTRAINT FK_cand_user FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

CREATE TABLE auth.companies (
    id NVARCHAR(36) NOT NULL,
    name NVARCHAR(255) NOT NULL,
    slug NVARCHAR(255) NOT NULL,
    logo_url NVARCHAR(500) NULL,
    website NVARCHAR(255) NULL,
    industry NVARCHAR(100) NULL,
    company_size NVARCHAR(50) NULL,
    address NVARCHAR(500) NULL,
    description NVARCHAR(MAX) NULL,
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_comp_status DEFAULT 'approved',
    tax_id NVARCHAR(50) NULL,
    verification_status NVARCHAR(50) NOT NULL CONSTRAINT DF_comp_ver DEFAULT 'unverified',
    verified_at DATETIME2(7) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_comp_created DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_comp_updated DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_auth_companies PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_auth_companies_slug UNIQUE (slug)
);

CREATE TABLE auth.company_members (
    id NVARCHAR(36) NOT NULL,
    company_id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    role NVARCHAR(50) NOT NULL CONSTRAINT DF_mem_role DEFAULT 'recruiter',
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_mem_created DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_auth_company_members PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_mem_company FOREIGN KEY (company_id) REFERENCES auth.companies(id) ON DELETE CASCADE,
    CONSTRAINT FK_mem_user FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);
GO

-- =====================================================================================
-- MODULE 2: CV PROCESSING & OCR (cv schema)
-- =====================================================================================
CREATE TABLE cv.skills (
    id NVARCHAR(36) NOT NULL,
    name NVARCHAR(100) NOT NULL,
    category NVARCHAR(50) NOT NULL CONSTRAINT DF_skills_cat DEFAULT 'hard',
    normalized_name NVARCHAR(100) NOT NULL,
    CONSTRAINT PK_cv_skills PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_cv_skills_name UNIQUE (name)
);

CREATE TABLE cv.cvs (
    id NVARCHAR(36) NOT NULL,
    candidate_id NVARCHAR(36) NOT NULL,
    file_name NVARCHAR(255) NOT NULL,
    file_url NVARCHAR(500) NOT NULL,
    file_size INT NOT NULL,
    mime_type NVARCHAR(100) NOT NULL,
    raw_text NVARCHAR(MAX) NULL,
    is_primary BIT NOT NULL CONSTRAINT DF_cv_primary DEFAULT 0,
    extraction_status NVARCHAR(50) NOT NULL CONSTRAINT DF_cv_status DEFAULT 'pending',
    extraction_error NVARCHAR(MAX) NULL,
    content_validated BIT NOT NULL CONSTRAINT DF_cv_validated DEFAULT 0,
    parsed_data NVARCHAR(MAX) NULL,
    embedding NVARCHAR(MAX) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_cv_created DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_cv_updated DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_cv_cvs PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_cv_candidate FOREIGN KEY (candidate_id) REFERENCES auth.candidate_profiles(id) ON DELETE CASCADE
);

CREATE TABLE cv.education_records (
    id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    institution NVARCHAR(255) NOT NULL,
    degree NVARCHAR(100) NULL,
    field_of_study NVARCHAR(255) NULL,
    start_date NVARCHAR(50) NULL,
    end_date NVARCHAR(50) NULL,
    gpa NVARCHAR(50) NULL,
    description NVARCHAR(MAX) NULL,
    CONSTRAINT PK_cv_education PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_edu_cv FOREIGN KEY (cv_id) REFERENCES cv.cvs(id) ON DELETE CASCADE
);

CREATE TABLE cv.experience_records (
    id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    company_name NVARCHAR(255) NOT NULL,
    job_title NVARCHAR(255) NOT NULL,
    start_date NVARCHAR(50) NULL,
    end_date NVARCHAR(50) NULL,
    is_current BIT NOT NULL CONSTRAINT DF_exp_current DEFAULT 0,
    description NVARCHAR(MAX) NULL,
    CONSTRAINT PK_cv_experience PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_exp_cv FOREIGN KEY (cv_id) REFERENCES cv.cvs(id) ON DELETE CASCADE
);

CREATE TABLE cv.cv_skills (
    id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    skill_id NVARCHAR(36) NOT NULL,
    proficiency_level NVARCHAR(50) NULL,
    years_of_experience FLOAT NULL,
    CONSTRAINT PK_cv_cv_skills PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_cv_skill_cv FOREIGN KEY (cv_id) REFERENCES cv.cvs(id) ON DELETE CASCADE,
    CONSTRAINT FK_cv_skill_skill FOREIGN KEY (skill_id) REFERENCES cv.skills(id) ON DELETE CASCADE
);
GO

-- =====================================================================================
-- MODULE 3: JOB MANAGEMENT & MODERATION (job schema)
-- =====================================================================================
CREATE TABLE job.jobs (
    id NVARCHAR(36) NOT NULL,
    company_id NVARCHAR(36) NOT NULL,
    creator_id NVARCHAR(36) NULL,
    title NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX) NOT NULL,
    requirements NVARCHAR(MAX) NOT NULL,
    benefits NVARCHAR(MAX) NULL,
    job_type NVARCHAR(50) NOT NULL CONSTRAINT DF_job_type DEFAULT 'full_time',
    location NVARCHAR(255) NOT NULL,
    salary_min INT NULL,
    salary_max INT NULL,
    currency NVARCHAR(10) NOT NULL CONSTRAINT DF_job_curr DEFAULT 'VND',
    experience_level NVARCHAR(50) NOT NULL CONSTRAINT DF_job_exp DEFAULT 'mid',
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_job_status DEFAULT 'published',
    rejection_reason NVARCHAR(MAX) NULL,
    embedding NVARCHAR(MAX) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_job_created DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_job_updated DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_job_jobs PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_job_company FOREIGN KEY (company_id) REFERENCES auth.companies(id) ON DELETE CASCADE,
    CONSTRAINT FK_job_creator FOREIGN KEY (creator_id) REFERENCES auth.users(id) ON DELETE SET NULL
);

CREATE TABLE job.job_skills (
    id NVARCHAR(36) NOT NULL,
    job_id NVARCHAR(36) NOT NULL,
    skill_id NVARCHAR(36) NOT NULL,
    is_required BIT NOT NULL CONSTRAINT DF_job_sk_req DEFAULT 1,
    importance_weight FLOAT NOT NULL CONSTRAINT DF_job_sk_weight DEFAULT 1.0,
    CONSTRAINT PK_job_job_skills PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_job_sk_job FOREIGN KEY (job_id) REFERENCES job.jobs(id) ON DELETE CASCADE,
    CONSTRAINT FK_job_sk_skill FOREIGN KEY (skill_id) REFERENCES cv.skills(id) ON DELETE CASCADE
);

CREATE TABLE job.job_reports (
    id NVARCHAR(36) NOT NULL,
    job_id NVARCHAR(36) NOT NULL,
    reporter_id NVARCHAR(36) NULL,
    reason NVARCHAR(100) NOT NULL,
    details NVARCHAR(MAX) NULL,
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_job_rep_status DEFAULT 'pending',
    action_taken NVARCHAR(100) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_job_rep_created DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_job_rep_updated DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_job_job_reports PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_rep_job FOREIGN KEY (job_id) REFERENCES job.jobs(id) ON DELETE CASCADE,
    CONSTRAINT FK_rep_user FOREIGN KEY (reporter_id) REFERENCES auth.users(id) ON DELETE NO ACTION
);
GO

-- =====================================================================================
-- MODULE 4 & 5: ATS APPLICATION & AI HYBRID MATCHING (ats & matching schemas)
-- =====================================================================================
CREATE TABLE ats.applications (
    id NVARCHAR(36) NOT NULL,
    job_id NVARCHAR(36) NOT NULL,
    candidate_id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_app_status DEFAULT 'submitted',
    cover_letter NVARCHAR(MAX) NULL,
    internal_notes NVARCHAR(MAX) NULL,
    interview_time DATETIME2(7) NULL,
    interview_location NVARCHAR(255) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_app_created DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2(7) NOT NULL CONSTRAINT DF_app_updated DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_ats_applications PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_app_job FOREIGN KEY (job_id) REFERENCES job.jobs(id) ON DELETE CASCADE,
    CONSTRAINT FK_app_candidate FOREIGN KEY (candidate_id) REFERENCES auth.users(id) ON DELETE NO ACTION,
    CONSTRAINT FK_app_cv FOREIGN KEY (cv_id) REFERENCES cv.cvs(id) ON DELETE NO ACTION
);

CREATE TABLE matching.match_results (
    id NVARCHAR(36) NOT NULL,
    job_id NVARCHAR(36) NOT NULL,
    cv_id NVARCHAR(36) NOT NULL,
    application_id NVARCHAR(36) NULL,
    overall_score FLOAT NOT NULL,
    hard_skills_score FLOAT NOT NULL CONSTRAINT DF_match_hs DEFAULT 0.0,
    semantic_score FLOAT NOT NULL CONSTRAINT DF_match_ss DEFAULT 0.0,
    experience_score FLOAT NOT NULL CONSTRAINT DF_match_es DEFAULT 0.0,
    matched_skills NVARCHAR(MAX) NULL,
    missing_required_skills NVARCHAR(MAX) NULL,
    missing_preferred_skills NVARCHAR(MAX) NULL,
    ai_explanation NVARCHAR(MAX) NULL,
    recommendations NVARCHAR(MAX) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_match_created DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_matching_match_results PRIMARY KEY CLUSTERED (id),
    CONSTRAINT UQ_match_app_id UNIQUE (application_id),
    CONSTRAINT FK_match_job FOREIGN KEY (job_id) REFERENCES job.jobs(id) ON DELETE CASCADE,
    CONSTRAINT FK_match_cv FOREIGN KEY (cv_id) REFERENCES cv.cvs(id) ON DELETE NO ACTION,
    CONSTRAINT FK_match_app FOREIGN KEY (application_id) REFERENCES ats.applications(id) ON DELETE NO ACTION
);

CREATE TABLE ats.notifications (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    title NVARCHAR(255) NOT NULL,
    message NVARCHAR(MAX) NOT NULL,
    type NVARCHAR(50) NOT NULL CONSTRAINT DF_notif_type DEFAULT 'system',
    link NVARCHAR(255) NULL,
    is_read BIT NOT NULL CONSTRAINT DF_notif_read DEFAULT 0,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_notif_created DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_ats_notifications PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_notif_user FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);
GO

-- =====================================================================================
-- MODULE 6: SECURITY & DATA PRIVACY (sec schema)
-- =====================================================================================
CREATE TABLE sec.audit_logs (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NULL,
    action NVARCHAR(100) NOT NULL,
    target_type NVARCHAR(100) NULL,
    target_id NVARCHAR(100) NULL,
    details NVARCHAR(MAX) NULL,
    ip_address NVARCHAR(50) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_audit_created DEFAULT SYSUTCDATETIME(),
    CONSTRAINT PK_sec_audit_logs PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_audit_user FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE SET NULL
);

CREATE TABLE sec.data_consents (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    consent_type NVARCHAR(100) NOT NULL,
    granted BIT NOT NULL CONSTRAINT DF_consent_granted DEFAULT 1,
    ip_address NVARCHAR(50) NULL,
    granted_at DATETIME2(7) NOT NULL CONSTRAINT DF_consent_granted_at DEFAULT SYSUTCDATETIME(),
    revoked_at DATETIME2(7) NULL,
    CONSTRAINT PK_sec_data_consents PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_consent_user FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

CREATE TABLE sec.data_requests (
    id NVARCHAR(36) NOT NULL,
    user_id NVARCHAR(36) NOT NULL,
    request_type NVARCHAR(50) NOT NULL,
    status NVARCHAR(50) NOT NULL CONSTRAINT DF_req_status DEFAULT 'pending',
    details NVARCHAR(MAX) NULL,
    created_at DATETIME2(7) NOT NULL CONSTRAINT DF_req_created DEFAULT SYSUTCDATETIME(),
    completed_at DATETIME2(7) NULL,
    CONSTRAINT PK_sec_data_requests PRIMARY KEY CLUSTERED (id),
    CONSTRAINT FK_req_user FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);
GO

PRINT N'====================================================================='
PRINT N' HOAN TAT KHOI TAO CSDL THEO 6 SCHEMAS MODULAR (auth, cv, job, matching, ats, sec)!'
PRINT N'====================================================================='
GO


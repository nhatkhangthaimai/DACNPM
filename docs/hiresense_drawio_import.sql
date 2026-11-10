-- =====================================================================================
-- FILE DDL SQL TOI UU CHO TINH NANG: "Arrange -> Insert -> Advanced -> SQL..." TREN DRAW.IO
-- Huong dan tren draw.io: Vao menu Arrange -> Insert -> Advanced -> SQL... -> Dan toan bo code nay vao -> Bam Insert
-- =====================================================================================

CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    role VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL,
    is_verified BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE candidate_profiles (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) UNIQUE NOT NULL,
    title VARCHAR(255),
    bio TEXT,
    location VARCHAR(255),
    years_of_experience FLOAT,
    expected_salary INT,
    github_url VARCHAR(255),
    linkedin_url VARCHAR(255),
    portfolio_url VARCHAR(255),
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE companies (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    logo_url VARCHAR(500),
    website VARCHAR(255),
    industry VARCHAR(100),
    company_size VARCHAR(50),
    address VARCHAR(500),
    description TEXT,
    status VARCHAR(50) NOT NULL,
    tax_id VARCHAR(50),
    verification_status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP
);

CREATE TABLE company_members (
    id VARCHAR(36) PRIMARY KEY,
    company_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE skills (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),
    normalized_name VARCHAR(100) NOT NULL
);

CREATE TABLE cvs (
    id VARCHAR(36) PRIMARY KEY,
    candidate_id VARCHAR(36) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    file_size INT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    raw_text TEXT,
    is_primary BOOLEAN,
    extraction_status VARCHAR(50) NOT NULL,
    extraction_error TEXT,
    content_validated BOOLEAN,
    parsed_data JSON,
    embedding TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidate_profiles(id)
);

CREATE TABLE education_records (
    id VARCHAR(36) PRIMARY KEY,
    cv_id VARCHAR(36) NOT NULL,
    institution VARCHAR(255) NOT NULL,
    degree VARCHAR(100),
    field_of_study VARCHAR(255),
    start_date VARCHAR(50),
    end_date VARCHAR(50),
    gpa VARCHAR(50),
    description TEXT,
    FOREIGN KEY (cv_id) REFERENCES cvs(id)
);

CREATE TABLE experience_records (
    id VARCHAR(36) PRIMARY KEY,
    cv_id VARCHAR(36) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    start_date VARCHAR(50),
    end_date VARCHAR(50),
    is_current BOOLEAN,
    description TEXT,
    FOREIGN KEY (cv_id) REFERENCES cvs(id)
);

CREATE TABLE cv_skills (
    id VARCHAR(36) PRIMARY KEY,
    cv_id VARCHAR(36) NOT NULL,
    skill_id VARCHAR(36) NOT NULL,
    proficiency_level VARCHAR(50),
    years_of_experience FLOAT,
    FOREIGN KEY (cv_id) REFERENCES cvs(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
);

CREATE TABLE jobs (
    id VARCHAR(36) PRIMARY KEY,
    company_id VARCHAR(36) NOT NULL,
    creator_id VARCHAR(36),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT NOT NULL,
    benefits TEXT,
    job_type VARCHAR(50),
    location VARCHAR(255) NOT NULL,
    salary_min INT,
    salary_max INT,
    currency VARCHAR(10),
    experience_level VARCHAR(50),
    status VARCHAR(50) NOT NULL,
    rejection_reason TEXT,
    embedding TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (creator_id) REFERENCES users(id)
);

CREATE TABLE job_skills (
    id VARCHAR(36) PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL,
    skill_id VARCHAR(36) NOT NULL,
    is_required BOOLEAN,
    importance_weight FLOAT,
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
);

CREATE TABLE applications (
    id VARCHAR(36) PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL,
    candidate_id VARCHAR(36) NOT NULL,
    cv_id VARCHAR(36) NOT NULL,
    status VARCHAR(50) NOT NULL,
    cover_letter TEXT,
    internal_notes TEXT,
    interview_time TIMESTAMP,
    interview_location VARCHAR(255),
    created_at TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (candidate_id) REFERENCES users(id),
    FOREIGN KEY (cv_id) REFERENCES cvs(id)
);

CREATE TABLE match_results (
    id VARCHAR(36) PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL,
    cv_id VARCHAR(36) NOT NULL,
    application_id VARCHAR(36) UNIQUE,
    overall_score FLOAT NOT NULL,
    hard_skills_score FLOAT,
    semantic_score FLOAT,
    experience_score FLOAT,
    matched_skills JSON,
    missing_required_skills JSON,
    missing_preferred_skills JSON,
    ai_explanation TEXT,
    recommendations JSON,
    created_at TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (cv_id) REFERENCES cvs(id),
    FOREIGN KEY (application_id) REFERENCES applications(id)
);

CREATE TABLE notifications (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50),
    link VARCHAR(255),
    is_read BOOLEAN,
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE audit_logs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(100),
    target_id VARCHAR(100),
    details JSON,
    ip_address VARCHAR(50),
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE data_consents (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    consent_type VARCHAR(100) NOT NULL,
    granted BOOLEAN,
    ip_address VARCHAR(50),
    granted_at TIMESTAMP,
    revoked_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE data_requests (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    request_type VARCHAR(50) NOT NULL,
    status VARCHAR(50),
    details JSON,
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE job_reports (
    id VARCHAR(36) PRIMARY KEY,
    job_id VARCHAR(36) NOT NULL,
    reporter_id VARCHAR(36),
    reason VARCHAR(100) NOT NULL,
    details TEXT,
    status VARCHAR(50),
    action_taken VARCHAR(100),
    created_at TIMESTAMP,
    FOREIGN KEY (job_id) REFERENCES jobs(id),
    FOREIGN KEY (reporter_id) REFERENCES users(id)
);

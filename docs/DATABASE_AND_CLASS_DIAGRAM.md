# TÀI LIỆU THIẾT KẾ CƠ SỞ DỮ LIỆU VÀ BIỂU ĐỒ LỚP UML THEO MODULE
**Đề tài:** HireSense AI – Smart Recruitment Platform (SIGNAL Edition)  
**Công nghệ:** PostgreSQL 16 + pgvector, Python FastAPI, SQLAlchemy 2.0 Async, Google Gemini API, ReactJS + TypeScript

---

## 1. SƠ ĐỒ THỰC THỂ LIÊN KẾT CƠ SỞ DỮ LIỆU (DATABASE ERD DIAGRAM)

Cơ sở dữ liệu của HireSense AI gồm **18 bảng thực thể**, hỗ trợ đầy đủ các phân hệ: Xác thực & Phân quyền, Hồ sơ Ứng viên & CV, Tin Tuyển dụng đa ngành, Thuật toán So khớp AI Hybrid Matching, Phễu tuyển dụng, Bảo mật kiểm toán (Audit Logs) và Quyền riêng tư dữ liệu (Data Privacy / GDPR).

```mermaid
erDiagram
    USERS ||--o| CANDIDATE_PROFILES : "owns"
    USERS ||--o{ COMPANY_MEMBERS : "joins"
    USERS ||--o{ JOBS : "creates"
    USERS ||--o{ APPLICATIONS : "submits"
    USERS ||--o{ NOTIFICATIONS : "receives"
    USERS ||--o{ AUDIT_LOGS : "logs"
    USERS ||--o{ DATA_CONSENTS : "grants"
    USERS ||--o{ DATA_REQUESTS : "initiates"
    USERS ||--o{ JOB_REPORTS : "submits"

    COMPANIES ||--o{ COMPANY_MEMBERS : "employs"
    COMPANIES ||--o{ JOBS : "publishes"

    CANDIDATE_PROFILES ||--o{ CVS : "manages"

    CVS ||--o{ EDUCATION_RECORDS : "details"
    CVS ||--o{ EXPERIENCE_RECORDS : "details"
    CVS ||--o{ CV_SKILLS : "contains"
    CVS ||--o{ APPLICATIONS : "attached_to"
    CVS ||--o{ MATCH_RESULTS : "evaluated_in"

    SKILLS ||--o{ CV_SKILLS : "categorizes"
    SKILLS ||--o{ JOB_SKILLS : "categorizes"

    JOBS ||--o{ JOB_SKILLS : "requires"
    JOBS ||--o{ APPLICATIONS : "receives"
    JOBS ||--o{ MATCH_RESULTS : "target_of"
    JOBS ||--o{ JOB_REPORTS : "flagged_by"

    APPLICATIONS ||--o| MATCH_RESULTS : "evaluated_as"

    USERS {
        string id PK "UUID"
        string email "Unique, Index"
        string hashed_password "Argon2 / Bcrypt"
        string full_name "Họ và tên"
        string phone "Số điện thoại"
        string role "candidate | recruiter | admin"
        boolean is_active "Trạng thái kích hoạt"
        boolean is_verified "Đã xác thực email"
        datetime created_at "Thời gian tạo"
        datetime updated_at "Thời gian cập nhật"
    }

    CANDIDATE_PROFILES {
        string id PK "UUID"
        string user_id FK "users.id (Cascade)"
        string title "Chức danh mục tiêu"
        string bio "Giới thiệu bản thân"
        string location "Địa điểm làm việc"
        float years_of_experience "Số năm kinh nghiệm"
        int expected_salary "Mức lương mong muốn"
        string github_url "Link GitHub"
        string linkedin_url "Link LinkedIn"
        string portfolio_url "Website Portfolio"
        datetime created_at "Thời gian tạo"
    }

    COMPANIES {
        string id PK "UUID"
        string name "Tên công ty"
        string slug "Unique, URL slug"
        string logo_url "Đường dẫn logo"
        string website "Website doanh nghiệp"
        string industry "Ngành nghề kinh doanh"
        string company_size "Quy mô nhân sự"
        string address "Địa chỉ trụ sở"
        string description "Mô tả công ty"
        string status "pending | approved | rejected"
        string tax_id "Mã số thuế"
        string verification_status "unverified | verified"
        datetime created_at "Thời gian tạo"
    }

    COMPANY_MEMBERS {
        string id PK "UUID"
        string company_id FK "companies.id"
        string user_id FK "users.id"
        string role "owner | recruiter | interviewer"
        datetime created_at "Thời gian gia nhập"
    }

    CVS {
        string id PK "UUID"
        string candidate_id FK "candidate_profiles.id"
        string file_name "Tên tệp gốc"
        string file_url "Đường dẫn lưu trữ an toàn"
        int file_size "Kích thước tệp (bytes)"
        string mime_type "application/pdf, docx, image"
        text raw_text "Nội dung văn bản trích xuất"
        boolean is_primary "CV chính dùng so khớp"
        string extraction_status "pending | processing | completed | failed"
        text extraction_error "Lỗi trích xuất nếu có"
        boolean content_validated "Đã kiểm duyệt chất lượng"
        json parsed_data "Dữ liệu JSON chuẩn hoá LLM"
        vector_768 embedding "pgvector 768 dimensions"
        datetime created_at "Thời gian tải lên"
    }

    EDUCATION_RECORDS {
        string id PK "UUID"
        string cv_id FK "cvs.id"
        string institution "Tên trường / Học viện"
        string degree "Bằng cấp / Học vị"
        string field_of_study "Chuyên ngành đào tạo"
        string start_date "Thời gian bắt đầu"
        string end_date "Thời gian tốt nghiệp"
        string gpa "Điểm trung bình tích luỹ"
    }

    EXPERIENCE_RECORDS {
        string id PK "UUID"
        string cv_id FK "cvs.id"
        string company_name "Tên công ty"
        string job_title "Chức vụ đảm nhiệm"
        string start_date "Ngày bắt đầu"
        string end_date "Ngày kết thúc"
        boolean is_current "Đang làm việc tại đây"
        text description "Mô tả trách nhiệm & thành tích"
    }

    SKILLS {
        string id PK "UUID"
        string name "Tên kỹ năng (Python, React...)"
        string category "hard | soft | tool | lang"
        string normalized_name "Tên chuẩn hoá NFC"
    }

    CV_SKILLS {
        string id PK "UUID"
        string cv_id FK "cvs.id"
        string skill_id FK "skills.id"
        string proficiency_level "beginner | intermediate | senior | expert"
        float years_of_experience "Số năm áp dụng thực tế"
    }

    JOBS {
        string id PK "UUID"
        string company_id FK "companies.id"
        string creator_id FK "users.id"
        string title "Tiêu đề vị trí tuyển dụng"
        text description "Mô tả công việc"
        text requirements "Yêu cầu ứng viên"
        text benefits "Chế độ đãi ngộ"
        string job_type "full_time | remote | hybrid | part_time"
        string location "Địa điểm tuyển dụng"
        int salary_min "Lương tối thiểu"
        int salary_max "Lương tối đa"
        string currency "VND | USD"
        string experience_level "entry | junior | mid | senior | lead"
        string status "draft | pending_approval | published | closed"
        text rejection_reason "Lý do từ chối kiểm duyệt"
        vector_768 embedding "pgvector 768 dimensions"
        datetime created_at "Thời gian đăng"
    }

    JOB_SKILLS {
        string id PK "UUID"
        string job_id FK "jobs.id"
        string skill_id FK "skills.id"
        boolean is_required "Bắt buộc hay ưu tiên"
        float importance_weight "Trọng số kỹ năng (0.5 - 2.0)"
    }

    APPLICATIONS {
        string id PK "UUID"
        string job_id FK "jobs.id"
        string candidate_id FK "users.id"
        string cv_id FK "cvs.id"
        string status "submitted | reviewing | shortlisted | interviewed | offered | rejected"
        text cover_letter "Thư giới thiệu ứng tuyển"
        text internal_notes "Ghi chú nội bộ của Recruiter"
        datetime interview_time "Lịch hẹn phỏng vấn"
        string interview_location "Phòng phỏng vấn / Link Online"
        datetime created_at "Thời gian nộp đơn"
    }

    MATCH_RESULTS {
        string id PK "UUID"
        string job_id FK "jobs.id"
        string cv_id FK "cvs.id"
        string application_id FK "applications.id (Unique, Nullable)"
        float overall_score "Điểm tổng hợp (0 - 100)"
        float hard_skills_score "Điểm kỹ năng cứng (50%)"
        float semantic_score "Điểm ngữ nghĩa pgvector (30%)"
        float experience_score "Điểm số năm kinh nghiệm (20%)"
        json matched_skills "Danh sách kỹ năng đáp ứng"
        json missing_required_skills "Kỹ năng bắt buộc còn thiếu"
        json missing_preferred_skills "Kỹ năng ưu tiên gợi ý học thêm"
        text ai_explanation "Giải thích lý do chấm điểm của Gemini"
        json recommendations "Lộ trình học tập cá nhân hóa"
        datetime created_at "Thời gian tính toán"
    }

    NOTIFICATIONS {
        string id PK "UUID"
        string user_id FK "users.id"
        string title "Tiêu đề thông báo"
        text message "Nội dung chi tiết"
        string type "application | interview | system"
        string link "Đường dẫn điều hướng"
        boolean is_read "Đã xem thông báo"
        datetime created_at "Thời gian gửi"
    }

    AUDIT_LOGS {
        string id PK "UUID"
        string user_id FK "users.id (Nullable)"
        string action "Hành động thực thi"
        string target_type "Đối tượng chịu tác động"
        string target_id "ID đối tượng"
        json details "Dữ liệu chi tiết thay đổi"
        string ip_address "Địa chỉ IP người thao tác"
        datetime created_at "Thời gian ghi nhật ký"
    }

    DATA_CONSENTS {
        string id PK "UUID"
        string user_id FK "users.id"
        string consent_type "cv_ai_processing | recruiter_sharing"
        boolean granted "Đồng ý xử lý dữ liệu"
        string ip_address "IP khi người dùng xác nhận"
        datetime granted_at "Thời gian chấp thuận"
        datetime revoked_at "Thời gian rút lại chấp thuận"
    }

    DATA_REQUESTS {
        string id PK "UUID"
        string user_id FK "users.id"
        string request_type "export_data | delete_all_data"
        string status "pending | completed | rejected"
        json details "Chi tiết yêu cầu người dùng"
        datetime created_at "Thời gian tạo yêu cầu"
        datetime completed_at "Thời gian xử lý xong"
    }

    JOB_REPORTS {
        string id PK "UUID"
        string job_id FK "jobs.id"
        string reporter_id FK "users.id"
        string reason "scam | fake_company | illegal_fee"
        text details "Chi tiết báo cáo vi phạm"
        string status "pending | reviewed | action_taken"
        string action_taken "Khóa tin / Cảnh cáo"
        datetime created_at "Thời gian báo cáo"
    }
```

---

## 2. BIỂU ĐỒ LỚP UML THEO TỪNG MODULE (MODULAR CLASS DIAGRAMS)

Hệ thống HireSense AI được kiến trúc thành **6 Module chức năng độc lập, lỏng lẻo (loose coupling) và có tính gắn kết cao (high cohesion)**:
1. **Module 1:** Xác thực & Quản lý Danh tính (Auth & Identity Management)
2. **Module 2:** Xử lý & Trích xuất CV Đa phương thức (CV Ingestion & Multi-modal Processing)
3. **Module 3:** Quản lý Tin Tuyển dụng & Kiểm duyệt (Job Management & Moderation)
4. **Module 4:** So khớp Thông minh & Phân tích Kỹ năng (AI Hybrid Matching & Skill Gap Analysis)
5. **Module 5:** Phễu Tuyển dụng & Theo dõi Ứng tuyển (ATS Funnel & Application Tracking)
6. **Module 6:** Bảo mật, Quyền riêng tư & Kiểm toán (Security, Privacy & Audit Logging)

---

### 2.1. Sơ đồ Kiến trúc Phụ thuộc giữa các Module (Package Dependency Diagram)

```mermaid
graph TD
    classDef moduleStyle fill:#0C1A2D,stroke:#C9F16A,stroke-width:2px,color:#fff;
    classDef aiStyle fill:#2A1B4E,stroke:#B8A8FA,stroke-width:2px,color:#fff;
    classDef coreStyle fill:#1E293B,stroke:#68DCC5,stroke-width:2px,color:#fff;

    M1["<b>Module 1: Auth & Identity</b><br>User, Profile, Company, RBAC"]:::coreStyle
    M2["<b>Module 2: CV & Vision OCR</b><br>CV, Experience, Education, Storage"]:::coreStyle
    M3["<b>Module 3: Job & Moderation</b><br>Job, JobSkill, Moderation"]:::coreStyle
    M4["<b>Module 4: AI Hybrid Matching</b><br>Gemini LLM, pgvector, Skill Gap Engine"]:::aiStyle
    M5["<b>Module 5: ATS & Application</b><br>Application, Funnel, Notification"]:::moduleStyle
    M6["<b>Module 6: Security & Privacy</b><br>AuditLog, DataConsent, GDPR Compliance"]:::coreStyle

    M1 -->|cung cấp User/Profile| M2
    M1 -->|cung cấp Company/Recruiter| M3
    M1 -->|xác thực ứng viên| M5
    M2 -->|cung cấp dữ liệu CV & Vector| M4
    M3 -->|cung cấp dữ liệu JD & Vector| M4
    M4 -->|tính điểm xếp hạng| M5
    M2 -->|đính kèm hồ sơ| M5
    M3 -->|tiếp nhận đơn ứng tuyển| M5
    M1 -.->|ghi nhận nhật ký| M6
    M5 -.->|ghi nhận nhật ký| M6
```

---

### 2.2. Module 1: Phân hệ Xác thực & Quản lý Danh tính (Auth & Identity Management)

Quản lý đăng ký, đăng nhập JWT, phân quyền 3 vai trò (`Candidate`, `Recruiter`, `Admin`) và thông tin hồ sơ doanh nghiệp.

```mermaid
classDiagram
    class UserRole {
        <<enumeration>>
        CANDIDATE
        RECRUITER
        ADMIN
    }

    class CompanyStatus {
        <<enumeration>>
        PENDING
        APPROVED
        REJECTED
    }

    class User {
        +String id
        +String email
        +String hashed_password
        +String full_name
        +String phone
        +UserRole role
        +Boolean is_active
        +Boolean is_verified
        +DateTime created_at
        +DateTime updated_at
        +verify_password(plain_password) Boolean
        +has_role(required_role) Boolean
    }

    class CandidateProfile {
        +String id
        +String user_id
        +String title
        +String bio
        +String location
        +Float years_of_experience
        +Integer expected_salary
        +String github_url
        +String linkedin_url
        +String portfolio_url
        +update_profile(data)
    }

    class Company {
        +String id
        +String name
        +String slug
        +String logo_url
        +String website
        +String industry
        +String company_size
        +String address
        +String description
        +CompanyStatus status
        +String tax_id
        +String verification_status
        +is_verified() Boolean
        +verify_company()
    }

    class CompanyMember {
        +String id
        +String company_id
        +String user_id
        +String role
        +DateTime created_at
    }

    class AuthController {
        +login(credentials) TokenResponse
        +register_candidate(data) UserResponse
        +register_recruiter(data) UserResponse
        +get_current_user() User
        +switch_demo_role(role) TokenResponse
    }

    class SecurityService {
        +hash_password(password) String
        +verify_password(plain, hashed) Boolean
        +create_access_token(payload, expires_delta) String
        +decode_access_token(token) Dict
    }

    User "1" *-- "0..1" CandidateProfile : owns
    User "1" o-- "0..*" CompanyMember : joins
    Company "1" *-- "0..*" CompanyMember : employs
    AuthController ..> User : authenticates
    AuthController ..> SecurityService : delegates
    User --> UserRole : typed_by
    Company --> CompanyStatus : has_status
```

---

### 2.3. Module 2: Phân hệ Xử lý & Trích xuất CV Đa phương thức (CV Ingestion & Multi-modal Processing)

Tiếp nhận tệp PDF, DOCX hoặc ảnh chụp điện thoại (JPG/PNG/WEBP), giải mã EXIF xoay ảnh, OCR bằng Gemini Vision và trích xuất cấu trúc thực thể. Đồng thời áp dụng **Adapter Pattern** cho việc lưu trữ an toàn.

```mermaid
classDiagram
    class ExtractionStatus {
        <<enumeration>>
        PENDING
        PROCESSING
        COMPLETED
        FAILED
        EXTRACTION_FAILED
    }

    class CV {
        +String id
        +String candidate_id
        +String file_name
        +String file_url
        +Integer file_size
        +String mime_type
        +String raw_text
        +Boolean is_primary
        +ExtractionStatus extraction_status
        +String extraction_error
        +Boolean content_validated
        +Dict parsed_data
        +List~Float~ embedding
        +DateTime created_at
        +set_as_primary()
        +is_valid_for_matching() Boolean
    }

    class EducationRecord {
        +String id
        +String cv_id
        +String institution
        +String degree
        +String field_of_study
        +String start_date
        +String end_date
        +String gpa
    }

    class ExperienceRecord {
        +String id
        +String cv_id
        +String company_name
        +String job_title
        +String start_date
        +String end_date
        +Boolean is_current
        +String description
    }

    class Skill {
        +String id
        +String name
        +String category
        +String normalized_name
    }

    class CVSkill {
        +String id
        +String cv_id
        +String skill_id
        +String proficiency_level
        +Float years_of_experience
    }

    class CVController {
        +upload_cv(file, candidate_id) CVResponse
        +get_cv_detail(cv_id) CVDetailResponse
        +delete_cv(cv_id) Boolean
        +set_primary(cv_id) CVResponse
        +download_cv_signed(cv_id) FileStream
    }

    class CVPipelineService {
        +validate_cv_file(filename, bytes, mime) Tuple
        +extract_pdf_text(bytes) Tuple
        +extract_docx_text(bytes) Tuple
        +extract_image_cv(bytes, filename) Tuple
        +clean_and_normalize_text(text) String
        +gemini_extract_structured_cv(raw_text) Dict
        +heuristic_cv_extraction(text) Dict
    }

    class StorageService {
        <<interface>>
        +save_file(file_bytes, filename, folder) String
        +read_file(storage_key) bytes
        +delete_file(storage_key) Boolean
        +generate_signed_url(storage_key, expiry) String
    }

    class LocalStorageService {
        -String upload_dir
        -String secret_key
        +save_file(file_bytes, filename, folder) String
        +read_file(storage_key) bytes
        +delete_file(storage_key) Boolean
        +generate_signed_url(storage_key, expiry) String
    }

    class S3CompatibleStorageService {
        -String bucket_name
        -String endpoint_url
        +save_file(file_bytes, filename, folder) String
        +read_file(storage_key) bytes
        +delete_file(storage_key) Boolean
        +generate_signed_url(storage_key, expiry) String
    }

    StorageService <|.. LocalStorageService : implements
    StorageService <|.. S3CompatibleStorageService : implements

    CV "1" *-- "0..*" EducationRecord : contains
    CV "1" *-- "0..*" ExperienceRecord : contains
    CV "1" *-- "0..*" CVSkill : has
    Skill "1" -- "0..*" CVSkill : categorizes
    CV --> ExtractionStatus : has_status

    CVController ..> CV : manages
    CVController ..> CVPipelineService : processes
    CVController ..> StorageService : uses
```

---

### 2.4. Module 3: Phân hệ Quản lý Tin Tuyển dụng & Kiểm duyệt (Job Management & Moderation)

Quản lý đăng tin 14 lĩnh vực trọng điểm, tự động phân tích từ khóa kỹ năng bằng Regex biên dịch sẵn + LRU Cache, kiểm duyệt tin của Quản trị viên (Admin Moderation).

```mermaid
classDiagram
    class JobStatus {
        <<enumeration>>
        DRAFT
        PENDING_APPROVAL
        PUBLISHED
        CLOSED
        REJECTED
    }

    class JobType {
        <<enumeration>>
        FULL_TIME
        PART_TIME
        REMOTE
        HYBRID
        INTERNSHIP
    }

    class Job {
        +String id
        +String company_id
        +String creator_id
        +String title
        +String description
        +String requirements
        +String benefits
        +JobType job_type
        +String location
        +Integer salary_min
        +Integer salary_max
        +String currency
        +String experience_level
        +JobStatus status
        +String rejection_reason
        +List~Float~ embedding
        +DateTime created_at
        +publish()
        +close()
        +reject(reason)
    }

    class JobSkill {
        +String id
        +String job_id
        +String skill_id
        +Boolean is_required
        +Float importance_weight
    }

    class JobReport {
        +String id
        +String job_id
        +String reporter_id
        +String reason
        +String details
        +String status
        +String action_taken
        +resolve(action)
    }

    class JobsController {
        +get_jobs(filters) List~Job~
        +get_job_detail(job_id) JobResponse
        +create_job(data) JobResponse
        +update_job(job_id, data) JobResponse
        +seed_multi_industry() List~Job~
    }

    class AdminModerationController {
        +get_pending_jobs() List~Job~
        +approve_job(job_id) JobResponse
        +reject_job(job_id, reason) JobResponse
        +get_job_reports() List~JobReport~
    }

    class JobSkillExtractor {
        -List _COMPILED_SKILLS
        -Dict _JOBS_CACHE
        +extract_job_skills(job_id, requirements, description) Tuple
        +invalidate_jobs_cache()
    }

    Job "1" *-- "0..*" JobSkill : requires
    Job "1" o-- "0..*" JobReport : flagged_by
    Job --> JobStatus : status_is
    Job --> JobType : type_is

    JobsController ..> Job : manages
    JobsController ..> JobSkillExtractor : optimizes
    AdminModerationController ..> Job : moderates
```

---

### 2.5. Module 4: Phân hệ So khớp Thông minh & Phân tích Kỹ năng (AI Hybrid Matching & Skill Gap Analysis)

Trái tim trí tuệ nhân tạo của hệ thống: Tính toán điểm tương thích đa tiêu chí kết hợp Trọng số Kỹ năng bắt buộc (50%) + Tương đồng ngữ nghĩa pgvector (30%) + Số năm kinh nghiệm (20%), đồng thời chỉ ra Skill Gap và lộ trình học tập do Gemini sinh ra.

```mermaid
classDiagram
    class MatchResult {
        +String id
        +String job_id
        +String cv_id
        +String application_id
        +Float overall_score
        +Float hard_skills_score
        +Float semantic_score
        +Float experience_score
        +List matched_skills
        +List missing_required_skills
        +List missing_preferred_skills
        +String ai_explanation
        +List recommendations
        +DateTime created_at
        +get_verdict() String
    }

    class MatchingController {
        +calculate_match(cv_id, job_id) MatchScoreBreakdown
        +get_match_result(job_id, cv_id) MatchScoreBreakdown
        +get_all_cv_match_results(cv_id) List~MatchResult~
    }

    class HybridMatchingEngine {
        +calculate_hybrid_match(cv_data, job_data) Dict
        +calculate_hard_skills_score(cv_skills, req_skills, pref_skills) Float
        +compute_cosine_similarity(text1, text2) Float
        +calculate_experience_score(cv_exp, job_req_exp) Float
        +generate_ai_explanation(breakdown, cv_data, job_data) String
        +generate_skill_roadmap(missing_skills) List~Dict~
    }

    class VectorEmbeddingService {
        -String model_name
        +generate_embedding(text) List~Float~
        +cosine_distance(vec_a, vec_b) Float
    }

    MatchingController ..> MatchResult : persists_and_returns
    MatchingController ..> HybridMatchingEngine : orchestrates
    HybridMatchingEngine ..> VectorEmbeddingService : relies_on
```

---

### 2.6. Module 5: Phân hệ Tuyển dụng & Quản lý Đơn ứng tuyển (ATS Funnel & Application Tracking)

Quản lý phễu ứng tuyển khép kín: Nộp hồ sơ -> Sàng lọc -> Phỏng vấn -> Nhận việc/Từ chối, kèm theo hệ thống thông báo đẩy (Notification system).

```mermaid
classDiagram
    class ApplicationStatus {
        <<enumeration>>
        SUBMITTED
        REVIEWING
        SHORTLISTED
        INTERVIEWED
        OFFERED
        REJECTED
        WITHDRAWN
    }

    class Application {
        +String id
        +String job_id
        +String candidate_id
        +String cv_id
        +ApplicationStatus status
        +String cover_letter
        +String internal_notes
        +DateTime interview_time
        +String interview_location
        +DateTime created_at
        +DateTime updated_at
        +update_status(new_status)
        +schedule_interview(time, location)
        +add_recruiter_note(note)
    }

    class Notification {
        +String id
        +String user_id
        +String title
        +String message
        +String type
        +String link
        +Boolean is_read
        +DateTime created_at
        +mark_as_read()
    }

    class ApplicationController {
        +apply_job(job_id, cv_id, cover_letter) ApplicationResponse
        +get_my_applications() List~ApplicationResponse~
        +get_job_applications(job_id) List~ApplicationResponse~
        +update_status(app_id, status) ApplicationResponse
        +schedule_interview(app_id, time, location) ApplicationResponse
    }

    class NotificationService {
        +send_notification(user_id, title, msg, type, link) Notification
        +get_user_notifications(user_id) List~Notification~
        +mark_all_read(user_id) Boolean
    }

    Application --> ApplicationStatus : status_is
    Application "1" o-- "0..1" MatchResult : scored_by

    ApplicationController ..> Application : manages
    ApplicationController ..> NotificationService : triggers
    NotificationService ..> Notification : delivers
```

---

### 2.7. Module 6: Phân hệ Bảo mật, Quyền riêng tư & Nhật ký Kiểm toán (Security, Privacy & Audit Logging)

Tuân thủ Nghị định 13/2023/NĐ-CP và GDPR: Ghi vết kiểm toán (Audit Trail), quản lý sự đồng thuận xử lý AI (Data Consent) và quyền yêu cầu xuất/xóa dữ liệu cá nhân (Right to be Forgotten).

```mermaid
classDiagram
    class ConsentType {
        <<enumeration>>
        CV_AI_PROCESSING
        RECRUITER_SHARING
        PRIVACY_POLICY
    }

    class DataRequestType {
        <<enumeration>>
        EXPORT_DATA
        DELETE_ALL_DATA
        RECTIFY_DATA
    }

    class AuditLog {
        +String id
        +String user_id
        +String action
        +String target_type
        +String target_id
        +Dict details
        +String ip_address
        +DateTime created_at
    }

    class DataConsent {
        +String id
        +String user_id
        +ConsentType consent_type
        +Boolean granted
        +String ip_address
        +DateTime granted_at
        +DateTime revoked_at
        +revoke()
    }

    class DataRequest {
        +String id
        +String user_id
        +DataRequestType request_type
        +String status
        +Dict details
        +DateTime created_at
        +DateTime completed_at
        +mark_completed()
    }

    class PrivacyController {
        +grant_consent(type) DataConsent
        +revoke_consent(type) DataConsent
        +request_data_export() DataRequest
        +request_account_deletion() DataRequest
    }

    class AuditService {
        +log_event(user_id, action, target_type, target_id, details, ip) AuditLog
        +get_user_audit_logs(user_id) List~AuditLog~
    }

    DataConsent --> ConsentType : type_is
    DataRequest --> DataRequestType : type_is

    PrivacyController ..> DataConsent : manages
    PrivacyController ..> DataRequest : manages
    PrivacyController ..> AuditService : logs
```

---

## 3. BẢNG TỔNG HỢP CÁC MODULE VÀ ÁNH XẠ MÃ NGUỒN THỰC TẾ

| STT | Module | Các Thực thể (Entity Classes) | Services / Pipelines cốt lõi | File mã nguồn Backend chính |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Auth & Identity** | `User`, `CandidateProfile`, `Company`, `CompanyMember` | `SecurityService`, `AuthService` | [`app/api/v1/endpoints/auth.py`](file:///d:/DACNPM/backend/app/api/v1/endpoints/auth.py), [`app/core/security.py`](file:///d:/DACNPM/backend/app/core/security.py) |
| **2** | **CV & Vision OCR** | `CV`, `EducationRecord`, `ExperienceRecord`, `CVSkill`, `Skill` | `CVPipelineService`, `LocalStorageService`, `S3StorageService` | [`app/api/v1/endpoints/cvs.py`](file:///d:/DACNPM/backend/app/api/v1/endpoints/cvs.py), [`app/ai/pipeline.py`](file:///d:/DACNPM/backend/app/ai/pipeline.py), [`app/core/storage.py`](file:///d:/DACNPM/backend/app/core/storage.py) |
| **3** | **Job & Moderation**| `Job`, `JobSkill`, `JobReport` | `JobSkillExtractor` (LRU + Precompiled Regex) | [`app/api/v1/endpoints/jobs.py`](file:///d:/DACNPM/backend/app/api/v1/endpoints/jobs.py), [`app/api/v1/endpoints/admin.py`](file:///d:/DACNPM/backend/app/api/v1/endpoints/admin.py) |
| **4** | **AI Hybrid Match** | `MatchResult` | `HybridMatchingEngine`, `VectorEmbeddingService` | [`app/api/v1/endpoints/matching.py`](file:///d:/DACNPM/backend/app/api/v1/endpoints/matching.py), [`app/ai/pipeline.py`](file:///d:/DACNPM/backend/app/ai/pipeline.py) |
| **5** | **ATS & Application**| `Application`, `Notification` | `ApplicationService`, `NotificationService` | [`app/api/v1/endpoints/applications.py`](file:///d:/DACNPM/backend/app/api/v1/endpoints/applications.py) |
| **6** | **Security & Privacy**| `AuditLog`, `DataConsent`, `DataRequest` | `AuditService`, `PrivacyService` | [`app/api/v1/endpoints/admin.py`](file:///d:/DACNPM/backend/app/api/v1/endpoints/admin.py), [`app/core/database.py`](file:///d:/DACNPM/backend/app/core/database.py) |


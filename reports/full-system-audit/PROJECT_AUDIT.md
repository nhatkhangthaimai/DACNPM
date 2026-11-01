# BÁO CÁO KIỂM TOÁN DỰ ÁN TOÀN DIỆN (DEEP PROJECT AUDIT)
**Hệ thống:** HireSense AI – Smart Recruitment Platform  
**Phiên bản:** SIGNAL Edition v2.0  
**Ngày kiểm toán:** 27/10/2026  
**Chuyên gia thực hiện:** Nhóm Kiểm định Kiến trúc & QA Automation cấp cao  

---

## 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

HireSense AI là nền tảng tuyển dụng thông minh ứng dụng Mô hình Ngôn ngữ Lớn (LLMs), Embeddings đa chiều và Vector Database nhằm tự động hóa quy trình phân tích CV, so khớp ứng viên (Hybrid Job Matching) và phân tích khoảng cách kỹ năng (Skill Gap Analysis).

```
+-------------------------------------------------------------------------------+
|                       REACTJS FRONTEND (SIGNAL EDITION)                       |
|   - Vite + React 18 + TypeScript + Tailwind CSS                               |
|   - Port: 5173 (Host) -> 80 (Docker Container Nginx)                          |
|   - Quản lý trạng thái: React Context API + LocalStorage Cache                 |
|   - Personas: Candidate Portal | Recruiter Portal | Admin Moderation Portal   |
+---------------------------------------+---------------------------------------+
                                        | (REST JSON API / JWT Bearer)
                                        v
+-------------------------------------------------------------------------------+
|                        FASTAPI BACKEND CORE ENGINE                             |
|   - Python 3.11 + FastAPI + AsyncIO + SQLAlchemy 2.0 Async                    |
|   - Port: 8000 (Host/Container)                                               |
|   - Middleware: CORS, Security Bearer, Exception Handlers                     |
|   - Modules: Auth, Users, Candidates, Companies, Jobs, CVs, Applications,     |
|              Hybrid Matching Engine, AI Pipeline                              |
+-------------------+-------------------+-------------------+-------------------+
                    |                   |                   |
                    v                   v                   v
+-----------------------+ +-----------------------+ +-----------------------+
|  POSTGRESQL + PGVECTOR| |    GOOGLE GEMINI AI   | |    PARSING & NLP      |
|  - Postgres 16        | |  - Model:             | |  - PyMuPDF (fitz)     |
|  - pgvector 0.8.7     | |    gemini-2.5-flash   | |  - pdfplumber         |
|  - 14 Database Tables | |  - Embeddings:        | |  - python-docx        |
|  - 768-dim Vector Col | |    gemini-embedding-  | |  - NFC Unicode Norm   |
|  - Port: 5432         | |    001 (REST transp)  | |  - Anti-Corrupt Gate  |
+-----------------------+ +-----------------------+ +-----------------------+
```

---

## 2. MÔI TRƯỜNG THỰC THI & CONTAINER STATUS

Kiểm toán trạng thái thực tế của các containers Docker đang vận hành trên host Windows:

| Container Name | Service | Image | Cổng ánh xạ | Trạng thái | Ghi chú |
|---|---|---|---|---|---|
| `hiresense_backend` | FastAPI REST API | `dacnpm-backend:latest` | `0.0.0.0:8000->8000/tcp` | Up (healthy) | Python 3.11, PyMuPDF, SQLAlchemy 2.0 |
| `hiresense_frontend` | Nginx React Web | `dacnpm-frontend:latest` | `0.0.0.0:5173->80/tcp` | Up | Nginx serving production bundle (dist/) |
| `hiresense_postgres` | Database + pgvector | `pgvector/pgvector:pg16` | `0.0.0.0:5432->5432/tcp` | Up (healthy) | PostgreSQL 16.4, extension vector 0.8.7 |

---

## 3. KIỂM TOÁN THƯ VIỆN & PHỤ THUỘC (DEPENDENCY AUDIT)

### 3.1. Backend Python Dependencies (`backend/requirements.txt`)

Qua rà soát chi tiết mã nguồn và lịch sử lỗi của dự án, các thư viện từng bị thiếu hoặc xung đột phiên bản đã được chuẩn hóa và kiểm tra đầy đủ:

1. **`greenlet` (v3.1.1):** Đã cài đặt trong container backend. Ngăn ngừa triệt để lỗi thiếu runtime cho SQLAlchemy AsyncIO.
2. **`email-validator` (v2.2.0):** Đã cài đặt, phục vụ xác thực schema EmailStr của Pydantic V2.
3. **`sqlalchemy` (v2.0.36) & `asyncpg` (v0.30.0):** Cấu hình chuẩn kết nối bất đồng bộ pool kết nối PostgreSQL.
4. **`pymupdf` (v1.24.14) & `pdfplumber` (v0.11.4):** Kết hợp trích xuất văn bản PDF 2 cột, bảng biểu và ký tự tiếng Việt.
5. **`python-docx` (v1.1.2):** Xử lý định dạng CV Microsoft Word .docx qua paragraphs và tables.
6. **`google-generativeai` (v0.8.3):** Cấu hình chế độ giao tiếp `transport="rest"` để tránh tình trạng gRPC handshake timeout trong Docker network.
7. **`bcrypt` (v4.0.1) & `python-jose` (v3.3.0):** Băm mật khẩu một chiều an toàn và sinh JWT access token.

### 3.2. Frontend Dependencies (`frontend/package.json`)

1. **`react` & `react-dom`:** v18.3.1.
2. **`vite`:** v5.4.21 – Build bundle sản xuất đạt 0 lỗi biên dịch TypeScript.
3. **`axios`:** v1.7.9 – Tích hợp HTTP Client kèm interceptor gắn JWT Bearer token tự động.
4. **`lucide-react`:** Bộ icon chuẩn cho phong cách SIGNAL Edition.
5. **`canvas-confetti`:** Hiệu ứng chúc mừng khi ứng tuyển thành công.

---

## 4. BẢN ĐỒ SCHEMA DỮ LIỆU POSTGRESQL

Cơ sở dữ liệu gồm 14 bảng quan hệ với tính toàn vẹn khóa ngoại (Foreign Keys) nghiêm ngặt:

1. `users`: Quản lý tài khoản, mật khẩu băm bcrypt, vai trò (`candidate`, `recruiter`, `admin`), trạng thái khóa.
2. `candidate_profiles`: Hồ sơ ứng viên, tiêu đề nghề nghiệp, bio, vị trí mong muốn, liên kết 1-1 với `users`.
3. `companies`: Hồ sơ doanh nghiệp tuyển dụng, slug định danh, trạng thái duyệt (`pending`, `approved`, `rejected`).
4. `company_members`: Quan hệ n-n giữa `companies` và `users` (vai trò `owner`, `recruiter`).
5. `jobs`: Tin tuyển dụng JD, tiêu đề, mô tả, yêu cầu, mức lương, kinh nghiệm, trạng thái kiểm duyệt (`draft`, `pending`, `published`, `closed`).
6. `cvs`: Hồ sơ CV tải lên, dung lượng, đường dẫn file, trạng thái trích xuất (`pending`, `completed`, `extraction_failed`), trường `content_validated` (kiểm định chất lượng nội dung), `extraction_error`, và vector embedding 768 chiều.
7. `match_results`: Bản ghi điểm so khớp Hybrid Matching giữa CV và JD (điểm tổng, điểm hard skills, điểm semantic, điểm kinh nghiệm, kỹ năng thiếu, giải thích AI).
8. `applications`: Đơn ứng tuyển công việc kết nối `jobs`, `candidate_profiles`, `cvs` và `match_results`.
9. `audit_logs`: Nhật ký kiểm toán thao tác quản trị và kiểm duyệt tin.
10. `skills`, `job_skills`, `cv_skills`, `experience_records`, `education_records`: Lưu trữ kỹ năng và tiểu sử chuẩn hóa.

---

## 5. KẾT LUẬN KIỂM TOÁN DỰ ÁN

Hệ thống HireSense AI đã hoàn tất việc đồng bộ hạ tầng giữa Container và Host Code:
- Mã nguồn Backend không còn phụ thuộc vào các thư viện thiếu.
- Database Schema pgvector đã kích hoạt phiên bản vector 0.8.7.
- Frontend đã loại bỏ các tham chiếu `undefined.slice()` gây màn hình trắng.
- Các API endpoints đã được cấu hình CORS và bảo vệ xác thực Bearer token.

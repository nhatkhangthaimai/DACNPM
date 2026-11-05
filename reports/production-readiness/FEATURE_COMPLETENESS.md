# HireSense AI - Feature Completeness Matrix

**Ngày cập nhật:** 05/11/2026  
**Phiên bản hệ thống:** v2.0-production-candidate  
**Đánh giá tổng quan:** Toàn diện 3 vai trò (Candidate, Recruiter, Admin), Core AI Matching Engine, Privacy & Security Module.

---

## 1. Candidate Portal (Cổng Ứng Viên)

| Phân hệ / Chức năng | Hiện trạng | Minh chứng kỹ thuật & File liên quan | Đánh giá |
| :--- | :---: | :--- | :---: |
| **Đăng ký / Đăng nhập** | COMPLETE | `POST /api/v1/auth/register`, JWT Authentication, Bcrypt hash | 100% |
| **Quên / Đặt lại mật khẩu** | COMPLETE | `POST /forgot-password`, `POST /reset-password` (JWT 15p) | 100% |
| **Quản lý CV đa định dạng** | COMPLETE | Hỗ trợ PDF, DOCX, JPG, PNG, HEIC/HEIF với Auto-rotate & Cleanup | 100% |
| **Đặt CV chính (Primary CV)**| COMPLETE | `PUT /api/v1/cvs/{id}/primary`, tự động liên kết so khớp JD | 100% |
| **Xóa CV cá nhân** | COMPLETE | `DELETE /api/v1/cvs/{id}`, xóa file vật lý và embedding liên quan | 100% |
| **Khám phá Việc làm (Job Discovery)**| COMPLETE | Lọc 14 nhóm ngành, 3 thành phố lớn, phân trang, full-text search | 100% |
| **So khớp thông minh (Matching Center)** | COMPLETE | Hybrid Matching (50% Hard Skills + 30% Cosine + 20% Experience) | 100% |
| **Phân tích Khoảng cách Kỹ năng** | COMPLETE | Phân loại Kỹ năng đạt, Kỹ năng thiếu, Lộ trình học tập đề xuất | 100% |
| **Nộp đơn ứng tuyển** | COMPLETE | `POST /api/v1/applications`, đính kèm CV và Cover Letter | 100% |
| **Rút đơn ứng tuyển (Withdraw)** | COMPLETE | `DELETE /api/v1/applications/{id}` (khi ở trạng thái submitted) | 100% |
| **Theo dõi lịch phỏng vấn** | COMPLETE | Nhận thông báo in-app và email khi Recruiter xếp lịch phỏng vấn | 100% |
| **Báo cáo tin tuyển dụng lừa đảo** | COMPLETE | `POST /api/v1/jobs/{id}/report`, gắn cờ tin đáng ngờ | 100% |
| **Quản lý Quyền riêng tư & Dữ liệu** | COMPLETE | Luật 91/2025/QH15: Consent, Xuất dữ liệu JSON, Xóa tài khoản vĩnh viễn | 100% |

---

## 2. Recruiter Portal (Cổng Nhà Tuyển Dụng)

| Phân hệ / Chức năng | Hiện trạng | Minh chứng kỹ thuật & File liên quan | Đánh giá |
| :--- | :---: | :--- | :---: |
| **Đăng ký tài khoản Doanh nghiệp** | COMPLETE | `POST /api/v1/auth/register-recruiter`, liên kết `tax_id` | 100% |
| **Xác thực hồ sơ Công ty** | COMPLETE | Quy trình xác minh MST, trạng thái `pending_verification` / `verified` | 100% |
| **Tạo mới và Quản lý Tin JD** | COMPLETE | AI-assisted JD creation, kiểm duyệt tự động từ khóa lừa đảo (Anti-Scam) | 100% |
| **Bảng xếp hạng Ứng viên (Candidate Ranking)** | COMPLETE | Tự động xếp hạng ứng viên theo Hybrid Matching Score thực | 100% |
| **Xem chi tiết hồ sơ & CV ứng viên** | COMPLETE | Tải CV qua Signed HMAC URL bảo mật, phân tích khoảng cách kỹ năng | 100% |
| **Cập nhật trạng thái tuyển dụng** | COMPLETE | `PUT /api/v1/applications/{id}/status` (reviewing, interviewing, accepted, rejected) | 100% |
| **Xếp lịch phỏng vấn** | COMPLETE | `PUT /api/v1/applications/{id}/schedule-interview`, thời gian & địa điểm | 100% |
| **Hệ thống Thông báo Doanh nghiệp**| COMPLETE | In-app notifications khi có ứng viên mới nộp hoặc rút đơn | 100% |
| **Cách ly dữ liệu (Company Isolation)** | COMPLETE | Multi-tenant RBAC: Recruiter chỉ quản lý ứng viên nộp vào công ty mình | 100% |

---

## 3. Administrator Portal (Cổng Quản Trị Hệ Thống)

| Phân hệ / Chức năng | Hiện trạng | Minh chứng kỹ thuật & File liên quan | Đánh giá |
| :--- | :---: | :--- | :---: |
| **Bảng điều khiển Tổng quan (Admin Dashboard)** | COMPLETE | Thống kê số lượng user, công ty, tin tuyển dụng, lượt nộp hồ sơ | 100% |
| **Kiểm duyệt Tin tuyển dụng (Job Moderation)** | COMPLETE | `PUT /api/v1/admin/jobs/{id}/moderate`, duyệt hoặc từ chối kèm lý do | 100% |
| **Quản trị Người dùng (User Management)** | COMPLETE | Khóa/Mở khóa tài khoản `PUT /api/v1/admin/users/{id}/toggle-active` | 100% |
| **Xác thực Doanh nghiệp (Company Verification)**| COMPLETE | `PUT /api/v1/admin/companies/{id}/verify`, kiểm tra MST hợp pháp | 100% |
| **Xử lý Báo cáo Vi phạm (Trust & Safety)** | COMPLETE | `GET /api/v1/admin/reports`, `PUT /api/v1/admin/reports/{id}/action` | 100% |
| **Nhật ký Giám sát Bảo mật (Audit Logging)** | COMPLETE | Bảng `audit_logs`, ghi nhận mọi hành vi quản trị, đổi mật khẩu, xóa dữ liệu | 100% |

---

## 4. Hệ Thống Nền Tảng (Core Infrastructure & Platform)

| Phân hệ | Chi tiết triển khai | Trạng thái |
| :--- | :--- | :---: |
| **AI Parsing & Matching Engine** | Hỗ trợ Gemini 1.5 Flash, 2.5 Flash, 1.5 Pro với Fallback Chain & Cache SHA-256 | Hoạt động tối ưu |
| **Negative Skill Filtering** | Bóc tách ngữ cảnh phủ định tiếng Việt ("chưa từng làm", "chưa có kinh nghiệm") | Đã kiểm thử |
| **Bảo mật Xác thực (Security)** | Enforce 401 trên mọi endpoint cần đăng nhập, chặn Demo switching trên Prod | Chuẩn OWASP ASVS |
| **Rate Limiting** | Sliding window bảo vệ Auth, Register, CV Upload, AI Matching | Hoạt động |
| **Lưu trữ Tệp (Storage)** | Adapter Storage kép: Local Storage với HMAC-SHA256 Token & S3-compatible | Sẵn sàng production |
| **Sao lưu & Phục hồi CSDL** | Script tự động dump PostgreSQL, tính SHA-256 Checksum, khôi phục an toàn | Đã xác minh |
| **Tối ưu Hiệu năng Frontend** | Code-splitting React.lazy 18 routes, bundle size giảm 60% (390 KB chunk chính) | Hoàn thành |


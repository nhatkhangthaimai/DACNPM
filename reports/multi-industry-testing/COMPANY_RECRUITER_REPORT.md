# BÁO CÁO DOANH NGHIỆP VÀ TÀI KHOẢN RECRUITER (COMPANY & RECRUITER REPORT)
**Dự án:** HireSense AI – Smart Recruitment Platform  
**Phạm vi:** Kiểm tra liên kết nghiệp vụ, phân quyền RBAC và cách ly dữ liệu nhà tuyển dụng  
**Thời gian thực hiện:** 2026-11-02  

---

## 1. BẢNG ĐỐI CHIẾU DOANH NGHIỆP VÀ TÀI KHOẢN NHÀ TUYỂN DỤNG

| STT | Mã Công Ty | Tên Doanh Nghiệp Giả Lập | Lĩnh Vực | Recruiter ID | Email Đăng Nhập | Đại Diện | Quyền Hạn |
|---|---|---|---|---|---|---|---|
| 1 | `comp-seed-01` | NovaTech Solutions | Công nghệ phần mềm | `user-rec-seed-01` | `recruiter01@example.test` | Nguyễn Quốc Bảo | Owner |
| 2 | `comp-seed-02` | DataVision Analytics | AI và phân tích dữ liệu | `user-rec-seed-02` | `recruiter02@example.test` | Trần Thị Mai Phương | Owner |
| 3 | `comp-seed-03` | Finora Digital | Tài chính – Fintech | `user-rec-seed-03` | `recruiter03@example.test` | Lê Hoàng Nam | Owner |
| 4 | `comp-seed-04` | BrightWave Media | Marketing | `user-rec-seed-04` | `recruiter04@example.test` | Phạm Thảo Ly | Owner |
| 5 | `comp-seed-05` | PixelCraft Studio | Thiết kế đồ họa | `user-rec-seed-05` | `recruiter05@example.test` | Đỗ Minh Tuấn | Owner |
| 6 | `comp-seed-06` | Mekong Logistics | Logistics | `user-rec-seed-06` | `recruiter06@example.test` | Huỳnh Thanh Sang | Owner |
| 7 | `comp-seed-07` | GreenMart Retail | Bán lẻ | `user-rec-seed-07` | `recruiter07@example.test` | Vũ Bích Ngọc | Owner |
| 8 | `comp-seed-08` | SunPeak Hospitality | Du lịch – Khách sạn | `user-rec-seed-08` | `recruiter08@example.test` | Trịnh Văn Hùng | Owner |
| 9 | `comp-seed-09` | EduNext Academy | Giáo dục | `user-rec-seed-09` | `recruiter09@example.test` | Phan Thùy Trang | Owner |
| 10 | `comp-seed-10` | BuildCore Engineering | Xây dựng | `user-rec-seed-10` | `recruiter10@example.test` | Cao Đăng Khoa | Owner |
| 11 | `comp-seed-11` | HealthBridge Services | Chăm sóc sức khỏe | `user-rec-seed-11` | `recruiter11@example.test` | Bùi Thị Thanh Hà | Owner |
| 12 | `comp-seed-12` | TalentWorks HR | Nhân sự | `user-rec-seed-12` | `recruiter12@example.test` | Dương Công Danh | Owner |
| 13 | `comp-seed-13` | SmartFactory Vietnam | Sản xuất | `user-rec-seed-13` | `recruiter13@example.test` | Tạ Đức Anh | Owner |
| 14 | `comp-seed-14` | CloudNest Technology | Cloud – DevOps | `user-rec-seed-14` | `recruiter14@example.test` | Hà Quỳnh Chi | Owner |
| 15 | `comp-seed-15` | AgriFuture Solutions | Nông nghiệp công nghệ | `user-rec-seed-15` | `recruiter15@example.test` | Lương Hải Đăng | Owner |

---

## 2. KẾT QUẢ KIỂM TRA ĐĂNG NHẬP LOCALHOST

### 2.1. Kiểm thử xác thực bằng API `/api/v1/auth/login`
- **Tài khoản kiểm tra:** `recruiter01@example.test` (password: `password123`).
- **Kết quả HTTP:** `200 OK`.
- **Payload trả về:**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "role": "recruiter",
    "user_id": "user-rec-seed-01",
    "full_name": "Nguyễn Quốc Bảo",
    "email": "recruiter01@example.test"
  }
  ```
- **Xác minh Hash:** Kiểm tra trong PostgreSQL bảng `users` cột `hashed_password` lưu chuỗi hash `$2b$12$...`. Xác nhận mật khẩu được bảo vệ đúng tiêu chuẩn OWASP.

---

## 3. KIỂM THỬ PHÂN QUYỀN VÀ CÁCH LY DỮ LIỆU (DATA ISOLATION & RBAC)

### 3.1. Truy vấn thông tin người dùng hiện tại (`GET /api/v1/auth/me`)
- Gửi kèm Bearer Token của `recruiter01`.
- Kết quả phản hồi chính xác thông tin doanh nghiệp được liên kết:
  - `company_id`: `comp-seed-01`
  - `company_name`: `NovaTech Solutions`
  - `role`: `recruiter`

### 3.2. Ngăn chặn Recruiter truy cập trái phép trang Quản trị viên (Admin)
- Gửi request `GET /api/v1/admin/users` với Bearer Token của Recruiter.
- **Kết quả:** `HTTP 403 Forbidden`.
- **Thông điệp:** `"Quyền truy cập bị từ chối: vai trò 'recruiter' không có quyền truy cập tài nguyên này."`
- **Kết luận:** Hệ thống RBAC chặn truy cập cấp backend một cách nghiêm ngặt, không thể bị qua mặt bằng việc chỉnh sửa State ở Frontend.

### 3.3. Tự động gán quyền sở hữu khi Recruiter tạo tin tuyển dụng (`POST /api/v1/jobs`)
- Thực hiện request tạo tin JD mới mà **không truyền trường `company_id`**.
- Backend tự động trích xuất `sub` (User ID) từ JWT Token, truy vấn bảng `company_members` và gán tự động `company_id = comp-seed-01`.
- **Kết quả:** JD mới tạo thuộc về đúng doanh nghiệp quản lý của Recruiter đó, không bị lẫn lộn dữ liệu giữa các công ty khác nhau.


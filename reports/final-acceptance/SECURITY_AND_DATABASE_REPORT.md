# HIRESENSE AI – BÁO CÁO BẢO MẬT VÀ CƠ SỞ DỮ LIỆU (SECURITY & DATABASE AUDIT REPORT)

**Dự án:** HireSense AI – Smart Recruitment Platform (SIGNAL Edition)  
**Phân hệ:** Database Architecture, Encryption, RBAC & API Security  
**Ngày thực hiện:** 01/11/2026  
**Chuyên gia đánh giá:** Software Security Engineer & Principal Database Architect  

---

## 1. KIỂM ĐỊNH CƠ SỞ DỮ LIỆU POSTGRESQL & PGVECTOR

### A. Trạng thái kết nối và Extension:
- **Cơ sở dữ liệu:** PostgreSQL 16 (Container `hiresense_postgres`).
- **Phần mở rộng pgvector:** Đã cài đặt và kích hoạt thành công phiên bản **`vector 0.8.7`**:
  ```sql
  SELECT extname, extversion, schema, description FROM pg_extension WHERE extname = 'vector';
  -- Kết quả: vector | 0.8.7 | public | vector data type and ivfflat and hnsw access methods
  ```
- **Driver kết nối:** `asyncpg` qua SQLAlchemy 2.0 Async Engine.
- **Khả năng tương thích Cloud Database (Render PostgreSQL):** Đã cấu hình bóc tách tham số `?sslmode=...` khỏi chuỗi kết nối và truyền `ssl_context` chuẩn vào engine để ngăn chặn lỗi `TypeError: connect() got an unexpected keyword argument 'sslmode'`.

### B. Danh mục 14 bảng quan hệ (Relational Tables):
Toàn bộ 14 bảng dữ liệu đã được khởi tạo và kiểm tra tính toàn vẹn khóa ngoại (Foreign Keys & Constraints):
1. `users`: Tài khoản người dùng (id, email, hashed_password, full_name, role, is_active, is_verified).
2. `candidate_profiles`: Hồ sơ ứng viên chi tiết (user_id, title, bio, location, years_of_experience).
3. `companies`: Doanh nghiệp tuyển dụng (id, name, logo_url, website, size, description).
4. `company_members`: Thành viên doanh nghiệp và phân quyền nội bộ.
5. `jobs`: Tin tuyển dụng (id, company_id, title, description, status, location, salary_min, salary_max).
6. `skills`: Từ điển kỹ năng chuẩn hóa (id, name, category, normalized_name).
7. `job_skills`: Kỹ năng gắn với từng tin tuyển dụng (job_id, skill_id, is_required).
8. `cvs`: Quản lý tệp CV (id, candidate_id, file_name, file_url, parsed_data, extraction_status, embedding vector).
9. `cv_skills`: Quan hệ n-n kỹ năng bóc tách từ CV.
10. `education_records`: Lịch sử học vấn ứng viên.
11. `experience_records`: Lịch sử công tác và kinh nghiệm thực tế.
12. `match_results`: Bảng lưu kết quả so khớp AI (cv_id, job_id, overall_score, hard_skills_score, semantic_score, matched_skills, missing_skills).
13. `applications`: Hồ sơ nộp đơn ứng tuyển (id, job_id, candidate_id, cv_id, status, applied_at).
14. `audit_logs`: Bảng lưu vết hành động bảo mật và kiểm duyệt của hệ thống.

---

## 2. KIỂM ĐỊNH AN TOÀN THÔNG TIN VÀ PHÂN QUYỀN (RBAC & ACCESS CONTROL)

### A. Mã hóa mật khẩu (Password Hashing):
- Mật khẩu người dùng được băm bằng thuật toán **Bcrypt** với salt ngẫu nhiên (`passlib.context.CryptContext(schemes=["bcrypt"])`).
- Tuyệt đối không lưu trữ plaintext hoặc băm một chiều yếu (như MD5/SHA1).
- Bằng chứng kiểm thử: `test_password_hashing_bcrypt` **PASSED**.

### B. Xác thực phiên làm việc (JWT Authentication):
- Sử dụng chuẩn JWT với thuật toán `HS256`, thời hạn hết hạn token (`ACCESS_TOKEN_EXPIRE_MINUTES`) được cấu hình qua biến môi trường.
- Chặn 100% token giả mạo, chữ ký sai, hoặc token đã hết hạn (trả về `HTTP 401 Unauthorized`).
- Bằng chứng kiểm thử: `test_jwt_token_encode_decode` và `test_invalid_token_decode_fails` **PASSED**.

### C. Phân quyền theo vai trò (Role-Based Access Control - RBAC):
- Hệ thống áp dụng 3 vai trò nghiêm ngặt: `candidate`, `recruiter`, `admin`.
- **Thử nghiệm xâm nhập 1:** Tài khoản Ứng viên cố tình gọi API `/api/v1/admin/users` hoặc `/api/v1/admin/jobs/{id}/moderate` $\rightarrow$ Bị chặn ngay lập tức với mã lỗi **`HTTP 403 Forbidden`**.
- **Thử nghiệm xâm nhập 2:** Tài khoản Quản trị viên gọi các API quản trị $\rightarrow$ Trả về **`HTTP 200 OK`**.
- Bằng chứng kiểm thử: `test_candidate_forbidden_from_admin_endpoints` và `test_admin_authorized_for_admin_endpoints` **PASSED**.

### D. Bảo mật dữ liệu riêng tư CV (Object-Level Authorization):
- Ứng viên chỉ được xem, chỉnh sửa hoặc xóa các file CV thuộc sở hữu của chính mình (`WHERE candidate_id = current_user.id`).
- Nhà tuyển dụng chỉ được phép xem CV của những ứng viên đã chính thức nộp đơn (`applications`) vào các tin tuyển dụng thuộc sở hữu của công ty họ.
- Ngăn ngừa hoàn toàn lỗ hổng IDOR (Insecure Direct Object Reference).

---

## 3. KIỂM ĐỊNH BẢO MẬT TẢI LÊN TỆP TIN (FILE UPLOAD SECURITY)

| Lỗ hổng tiềm ẩn | Cơ chế phòng thủ của HireSense AI | Đánh giá |
|---|---|:---:|
| **Path Traversal (`../../etc/passwd`)** | Tên file được băm UUID và sanitize qua `secure_filename`, lưu trữ độc lập trong thư mục cố định. | **ĐẠT** |
| **Giả mạo định dạng file (File Spoofing)** | Đọc 16 bytes đầu tiên của tệp tin để kiểm tra Magic Bytes (JPEG: `\xff\xd8\xff`, PNG: `\x89PNG`, PDF: `%PDF`). | **ĐẠT** |
| **Tấn công từ chối dịch vụ bằng file lớn (DoS/Zip Bomb)** | Giới hạn dung lượng tối đa 15MB, kiểm tra kích thước `len(content)` trước khi ghi đĩa hoặc gửi AI. | **ĐẠT** |
| **Chèn mã độc trong ảnh (Steganography / WebShell)** | Thư viện Pillow tự động mở, giải mã, xoay hướng và xuất lại sang định dạng nén tối ưu (WebP/JPEG). | **ĐẠT** |
| **Rò rỉ API Keys và Secrets** | Không in API keys ra console log; tuân thủ Secret Scanning của GitHub. | **ĐẠT** |
| **SQL Injection** | Sử dụng 100% SQLAlchemy ORM Parameterized Statements, không cộng chuỗi SQL thô. | **ĐẠT** |

**Kết luận:** Phân hệ Cơ sở dữ liệu và Bảo mật đạt chuẩn an toàn cao, đáp ứng đầy đủ các yêu cầu cho việc demo và sẵn sàng vận hành thực tế.

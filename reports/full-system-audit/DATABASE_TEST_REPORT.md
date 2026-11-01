# BÁO CÁO KIỂM TOÁN CƠ SỞ DỮ LIỆU POSTGRESQL & PGVECTOR (DATABASE TEST REPORT)
**Hệ thống:** HireSense AI – Smart Recruitment Platform  
**Tài liệu:** `reports/full-system-audit/DATABASE_TEST_REPORT.md`  
**Ngày kiểm toán:** 27/10/2026  
**Động cơ CSDL:** PostgreSQL 16.4 (Debian 16.4-1.pgdg120+1) + Extension pgvector 0.8.7  

---

## 1. TRẠNG THÁI EXTENSION PGVECTOR & VECTOR DIMENSION

Kiểm tra extension pgvector được cài đặt trong database `hiresense_db`:
```sql
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
```
**Kết quả thực tế:**
```text
 extname | extversion 
---------+------------
 vector  | 0.8.7
(1 row)
```
- **Kích thước vector chuẩn:** `embedding vector(768)` tại bảng `cvs` và `jobs`.
- **Chỉ mục tìm kiếm lân cận (Vector Index):** Sử dụng hàm khoảng cách Cosine Distance (`<=>`) để truy vấn ứng viên có độ tương đồng ngữ nghĩa cao nhất.
- **Tương thích ORM:** Mô hình `CompatVector` được định nghĩa trong `backend/app/models/entities.py` đảm bảo tương thích hoàn hảo giữa môi trường SQLite kiểm thử và PostgreSQL pgvector trong môi trường sản xuất.

---

## 2. KIỂM TOÁN TÍNH TOÀN VẸN CỦA 14 BẢNG CƠ SỞ DỮ LIỆU

Kết quả truy vấn số lượng bản ghi thực tế từ database:

```text
     table_name     | row_count 
--------------------+-----------
 applications       |         0
 audit_logs         |         0
 candidate_profiles |         2
 companies          |         2
 company_members    |         1
 cv_skills          |         0
 cvs                |         4
 education_records  |         0
 experience_records |         0
 job_skills         |         0
 jobs               |         2
 match_results      |         1
 skills             |         0
 users              |         5
(14 rows)
```

### Chi tiết các ràng buộc toàn vẹn dữ liệu (Constraints & Foreign Keys):
1. **Bảng `users`:**
   - Khóa chính: `id` (VARCHAR(36)).
   - Ràng buộc duy nhất: `email` (UNIQUE, NOT NULL, có chỉ mục index).
   - Mật khẩu băm: `hashed_password` (VARCHAR(255)) không bao giờ lưu mật khẩu dạng văn bản thô.
2. **Bảng `candidate_profiles`:**
   - Khóa ngoại `user_id` tham chiếu `users(id)` kèm quy tắc `ON DELETE CASCADE`.
3. **Bảng `companies` & `company_members`:**
   - `slug` định danh công ty duy nhất (UNIQUE).
   - `company_members` quản lý mối quan hệ n-n giữa Nhà tuyển dụng và Doanh nghiệp với vai trò `owner` hoặc `recruiter`.
4. **Bảng `jobs`:**
   - Khóa ngoại `company_id` tham chiếu `companies(id)`.
   - Trạng thái tin tuyển dụng: `draft`, `pending`, `published`, `closed`, `rejected`.
5. **Bảng `cvs`:**
   - Khóa ngoại `candidate_id` tham chiếu `candidate_profiles(id)`.
   - Cột trạng thái: `extraction_status` (`pending`, `completed`, `extraction_failed`).
   - Cột kiểm định nội dung: `content_validated` (BOOLEAN).
   - Cột thông báo lỗi: `extraction_error` (TEXT).
6. **Bảng `match_results`:**
   - Khóa ngoại tham chiếu đồng thời `cv_id` và `job_id`.
   - Lưu trữ chi tiết: `overall_score`, `hard_skills_score`, `semantic_score`, `experience_score`, `matched_skills`, `missing_skills`, `ai_explanation`.

---

## 3. AN TOÀN VẬN HÀNH CƠ SỞ DỮ LIỆU (DATABASE SAFETY POLICY)

Trong suốt quá trình kiểm thử và tự động sửa lỗi, nhóm kỹ thuật đã tuân thủ nghiêm ngặt các nguyên tắc bảo tồn dữ liệu:
- **KHÔNG** chạy lệnh `docker compose down -v` làm mất volume dữ liệu.
- **KHÔNG** xóa hoặc reset dữ liệu bảng `users`, `jobs`, `companies` đã có sẵn.
- **KHÔNG** áp dụng các migration mang tính phá hủy dữ liệu (destructive migrations).
- Các bài kiểm thử đơn vị và API sử dụng cơ chế session giao dịch riêng biệt (`sqlite+aiosqlite:///:memory:`) để bảo vệ dữ liệu sản xuất trong PostgreSQL.

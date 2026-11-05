# HireSense AI - Comprehensive Security Audit Report

**Tiêu chuẩn đối chiếu:** OWASP Application Security Verification Standard (ASVS) Level 2 & OWASP Top 10  
**Ngày kiểm toán:** 05/11/2026  
**Chuyên gia thực hiện:** Principal Security & DevOps Engineer  
**Kết quả kiểm tra tự động:** 10/10 Test cases Passed (`test_production_readiness.py`, `test_security_rbac.py`)

---

## 1. Tóm tắt Phát hiện & Khắc phục Lỗ hổng Nguy cấp

### 1.1. Lỗ hổng Bỏ qua Xác thực (Authentication Bypass in `require_role`) - CRITICAL [FIXED]
- **Vấn đề trước đây:** Hàm phụ thuộc `require_role` trong `app/core/security.py` trả về `None` khi request không chứa Bearer Token (`payload is None`), dẫn đến một số router không chặn được request nặc danh nếu phụ thuộc chỉ kiểm tra điều kiện quyền.
- **Biện pháp xử lý:** Sửa đổi triệt để `require_role` để luôn luôn kích hoạt ngoại lệ `HTTPException(status_code=401, detail="Vui lòng đăng nhập...")` khi thiếu token hoặc token vô hiệu. Bổ sung `get_authenticated_user_payload` làm rào chắn tiền xác thực.
- **Kiểm chứng:** Test case `test_unauthenticated_request_blocked_401` xác nhận 100% endpoint được bảo vệ trả về HTTP 401 khi không có token.

### 1.2. Loại bỏ Demo Mode trên Môi trường Mạng ngoài (Production Hardening) - HIGH [FIXED]
- **Vấn đề trước đây:** Giao diện người dùng có dropdown chọn vai trò Demo Persona (Candidate, Recruiter, Admin) mà không cần nhập mật khẩu.
- **Biện pháp xử lý:** 
  - Khóa cơ chế chuyển đổi tại Frontend: `IS_DEMO_ALLOWED = Boolean(import.meta.env.DEV && import.meta.env.VITE_ENABLE_DEMO_MODE === 'true')`.
  - Trên môi trường Production (`import.meta.env.PROD`), Dropdown hoàn toàn bị ẩn khỏi DOM và thay thế bằng huy hiệu bảo mật `JWT RBAC`.
  - Hàm `switchDemoRole` trong `AuthContext.tsx` ném lỗi `Error` nếu bị gọi lén trên production.

---

## 2. Ma trận Đối chiếu OWASP Top 10

| Mục kiểm toán OWASP | Hiện trạng | Cơ chế bảo vệ đã triển khai trong mã nguồn |
| :--- | :---: | :--- |
| **A01: Broken Access Control** | **PASS** | `require_role(UserRole.ADMIN)` và `require_role(UserRole.RECRUITER)` kiểm tra chữ ký JWT và vai trò ở tầng ASGI middleware. Object-level authorization kiểm tra quyền sở hữu công ty của recruiter trước khi xem hồ sơ. |
| **A02: Cryptographic Failures** | **PASS** | Mật khẩu băm một chiều bằng chuẩn công nghiệp `bcrypt` với cost factor tiêu chuẩn. Token xác thực sử dụng thuật toán HMAC-SHA256 bí mật được lấy từ biến môi trường `SECRET_KEY`. |
| **A03: Injection** | **PASS** | 100% câu truy vấn dữ liệu sử dụng SQLAlchemy 2.0 ORM với Parameterized Queries, loại trừ hoàn toàn nguy cơ SQL Injection. File path được làm sạch bằng Regex `re.sub(r'[^a-zA-Z0-9_-]', '_')` để chống Directory Traversal. |
| **A04: Insecure Design** | **PASS** | Quota rate limiting được tích hợp ngay tại các cửa ngõ nhạy cảm. Bộ lọc Scam Detector nhận diện và cô lập tin tuyển dụng có dấu hiệu lừa đảo tài chính ngay từ bước tạo JD. |
| **A05: Security Misconfiguration** | **PASS** | CORS được giới hạn theo danh sách whitelist trong `settings.BACKEND_CORS_ORIGINS`. Debug mode tự động tắt trên production (`DEBUG=False`). |
| **A06: Vulnerable and Outdated Components** | **PASS** | Cập nhật các thư viện phụ thuộc; kiểm tra không có lỗ hổng CVE nghiêm trọng trong FastAPI, Pydantic v2, PyMuPDF, python-docx, Pillow, và SQLite. |
| **A07: Identification and Authentication Failures** | **PASS** | Cơ chế Password Reset sử dụng Signed Token độc lập có thời hạn 15 phút, liên kết trực tiếp với email người dùng, tự hủy sau khi sử dụng. Rate limiting chặn Brute Force (tối đa 5 lần đăng nhập sai/phút). |
| **A08: Software and Data Integrity Failures** | **PASS** | File CV tải lên được kiểm tra Magic Bytes (chữ ký nhị phân thực tế của file PDF, DOCX, PNG, JPG, HEIC), từ chối file giả mạo đuôi mở rộng. Tải file an toàn qua Signed HMAC URLs có thời hạn. |
| **A09: Security Logging and Monitoring Failures** | **PASS** | Phân hệ `app/core/audit.py` tự động ghi nhận mọi sự kiện trọng yếu vào bảng CSDL `audit_logs` (Đăng nhập, Thay đổi mật khẩu, Cập nhật quyền, Duyệt tin, Xóa dữ liệu). |
| **A10: Server-Side Request Forgery (SSRF)** | **PASS** | Hệ thống không thực hiện các HTTP fetch tới địa chỉ IP tùy biến từ người dùng bên ngoài. Toàn bộ API bên thứ ba (Google Gemini API) được gọi qua endpoint chính thống của Google. |

---

## 3. Kiến Trúc Rate Limiting (Sliding Window)

HireSense AI triển khai bộ giới hạn tần suất bộ nhớ đệm (In-memory Sliding Window Rate Limiter) tại `backend/app/core/rate_limiter.py` với cấu hình cụ thể:

```python
# Cấu hình giới hạn tần suất truy cập bảo vệ hệ thống:
auth_rate_limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=60)      # Chống Brute-force Login
register_rate_limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=300) # Chống Spam Đăng ký tài khoản
upload_rate_limiter = SlidingWindowRateLimiter(max_requests=10, window_seconds=60)   # Chống tràn ổ cứng qua Upload
ai_matching_rate_limiter = SlidingWindowRateLimiter(max_requests=10, window_seconds=60) # Chống lạm dụng chi phí Gemini API
```

Khi vượt ngưỡng, hệ thống trả về mã lỗi chuẩn `HTTP 429 Too Many Requests` kèm theo trường `Retry-After`.

---

## 4. Kiểm Soát Quyền Sở Hữu Đối Tượng (Object-Level Authorization)

1. **Ứng viên (Candidate):**
   - Chỉ có quyền tải xuống, xem, hoặc xóa CV thuộc tài khoản sở hữu (`CV.candidate_id == current_user.id`).
   - Chỉ có thể rút đơn ứng tuyển (`DELETE /applications/{id}`) của chính mình khi đơn còn ở trạng thái `submitted`.
2. **Nhà tuyển dụng (Recruiter):**
   - Chỉ có thể xem danh sách ứng viên nộp vào tin tuyển dụng thuộc quyền sở hữu của công ty mình (`Job.company_id == recruiter.company_id`).
   - Không được phép can thiệp vào đơn ứng tuyển của công ty khác.
3. **Quản trị viên (Admin):**
   - Duyệt hoặc từ chối tin tuyển dụng trên toàn hệ thống kèm văn bản giải trình lý do (`rejection_reason`).
   - Tạm ngừng tin tuyển dụng có nguy cơ lừa đảo sau khi tiếp nhận báo cáo của ứng viên.


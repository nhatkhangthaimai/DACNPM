# TẬP HỢP CÁC TRƯỜNG HỢP KIỂM THỬ CHI TIẾT (TEST CASES SPECIFICATION)
**Hệ thống:** HireSense AI – Smart Recruitment Platform  
**Tài liệu:** `reports/full-system-audit/TEST_CASES.md`  
**Ngày ban hành:** 27/10/2026  

---

## 1. PHÂN HỆ AUTHENTICATION & SECURITY RBAC

| Test Case ID | Tên kịch bản | Dữ liệu đầu vào | Thao tác thực hiện | Kết quả mong đợi (Expected) |
|---|---|---|---|---|
| **TC-AUTH-01** | Đăng nhập tài khoản hợp lệ | Email: `nguyenvanan.ai@gmail.com`, Pass: `password123` | Gửi POST tới `/api/v1/auth/login` | HTTP 200 OK, trả JWT access token, thông tin `user_id`, vai trò `candidate` |
| **TC-AUTH-02** | Đăng nhập sai mật khẩu | Email: `nguyenvanan.ai@gmail.com`, Pass: `wrong_pass` | Gửi POST tới `/api/v1/auth/login` | HTTP 401 Unauthorized, thông báo: "Email hoặc mật khẩu không chính xác." |
| **TC-AUTH-03** | Đăng nhập tài khoản không tồn tại | Email: `nonexistent@gmail.com`, Pass: `123456` | Gửi POST tới `/api/v1/auth/login` | HTTP 401 Unauthorized |
| **TC-AUTH-04** | Đăng ký tài khoản Ứng viên mới | Email: `new.candidate@ai.vn`, Họ tên, Mật khẩu | Gửi POST tới `/api/v1/auth/register/candidate` | HTTP 200 OK, tạo bản ghi `User` và `CandidateProfile` trong database |
| **TC-AUTH-05** | Đăng ký với Email đã tồn tại | Email đã có trong database | Gửi POST tới `/api/v1/auth/register/candidate` | HTTP 400 Bad Request, thông báo: "Email này đã được sử dụng." |
| **TC-AUTH-06** | Đăng ký Nhà tuyển dụng kèm Doanh nghiệp | Email, Họ tên, Tên công ty: "TechCorp" | Gửi POST tới `/api/v1/auth/register/recruiter` | HTTP 200 OK, tạo `User`, `Company` và `CompanyMember` vai trò owner |
| **TC-SEC-01** | Băm mật khẩu một chiều bcrypt | Mật khẩu thô bất kỳ | Gọi hàm `get_password_hash()` | Chuỗi băm bắt đầu bằng `$2b$`, không lưu bản rõ, `verify_password()` trả True |
| **TC-SEC-02** | Mã hóa và giải mã JWT token | `subject="user-1"`, `role="recruiter"` | Gọi `create_access_token` và `decode_access_token` | Token chứa `sub`, `role`, `exp` hợp lệ; chữ ký hợp lệ |
| **TC-SEC-03** | Token bị giả mạo hoặc sai chữ ký | Token có chữ ký bị thay đổi | Gọi `decode_access_token` | Hàm trả về `None`, không sinh ngoại lệ crash |
| **TC-SEC-04** | Candidate truy cập API Admin | Header Bearer Token của Candidate | Gửi GET tới `/api/v1/admin/users` | **HTTP 403 Forbidden**, thông báo: "vai trò 'candidate' không có quyền truy cập" |
| **TC-SEC-05** | Admin truy cập API Admin | Header Bearer Token của Admin | Gửi GET tới `/api/v1/admin/users` | **HTTP 200 OK**, trả danh sách người dùng đầy đủ |

---

## 2. PHÂN HỆ CV PARSING & QUALITY GATE (BỘ PHÂN TÍCH CV)

| Test Case ID | Tên kịch bản | Loại tệp tin | Kịch bản kiểm thử | Kết quả mong đợi |
|---|---|---|---|---|
| **TC-CV-01** | Trích xuất CV PDF tiêu chuẩn | PDF hợp lệ có text | PDF chứa thông tin kỹ sư phần mềm Python | Họ tên, email, kỹ năng được trích xuất đầy đủ, `content_validated = True` |
| **TC-CV-02** | Trích xuất CV DOCX Word | DOCX hợp lệ | Tệp .docx chứa bảng biểu và đoạn văn bản | Đọc toàn bộ nội dung trong paragraphs và tables, không mất dữ liệu |
| **TC-CV-03** | Phát hiện và từ chối file PDF hỏng | PDF bị corrupt byte | File PDF bị cắt ngắn, lỗi cấu trúc EOF | Hệ thống bắt ngoại lệ, trả thông báo lỗi rõ ràng, không crash container |
| **TC-CV-04** | Cổng kiểm định chất lượng (Quality Gate) | PDF chứa binary rác | File thô chứa chuỗi `%PDF-1.4`, `/Root` | **Quality Gate kích hoạt:** Đánh dấu `extraction_failed`, cấm đưa vào AI prompt |
| **TC-CV-05** | Từ chối tệp tin CV rỗng | Tệp 0 byte | File PDF hoặc DOCX rỗng không có chữ | Báo lỗi nội dung rỗng, không cấp phép tính điểm so khớp |
| **TC-CV-06** | Tải lên tệp tin không được hỗ trợ | Tệp .exe / .jpg | Đổi tên file exe thành CV.pdf | Kiểm tra MIME type và cấu trúc tệp, trả HTTP 400 Bad Request |
| **TC-CV-07** | Chuẩn hóa tiếng Việt có dấu (Unicode NFC) | PDF tiếng Việt | Văn bản chứa tổ hợp dấu (NFD) | Tự động chuyển đổi thành NFC, không bị lỗi font khi hiển thị trên giao diện |
| **TC-CV-08** | Hủy cache điểm khi tải lại CV mới | Reupload CV | Tải CV mới đè lên hồ sơ ứng viên cũ | Toàn bộ kết quả so khớp cũ bị hủy (`is_stale=True`), yêu cầu tính toán lại |

---

## 3. PHÂN HỆ HYBRID JOB MATCHING (THUẬT TOÁN SO KHỚP)

| Test Case ID | Kịch bản kiểm thử | Dữ liệu CV | Dữ liệu JD | Kết quả mong đợi |
|---|---|---|---|---|
| **TC-JM-01** | So khớp chuẩn xác năng lực | CV: Python, FastAPI, PostgreSQL, 4 năm KN | JD: Senior Python Developer (Python, FastAPI, 3 năm) | Điểm Hard Skills: 100%, Semantic: Cao, Điểm tổng: > 90% |
| **TC-JM-02** | So khớp ứng viên trái ngành | CV: Photoshop, Illustrator, Graphic Design | JD: Backend Engineer (Python, Go, PostgreSQL) | Hard Skills: 0%, Điểm tổng rất thấp (< 20%), không sinh điểm ảo |
| **TC-JM-03** | Khắc phục Bug 42% ảo trên CV hỏng | CV bị lỗi trích xuất (`extraction_failed`) | JD: Bất kỳ | **BỊ CHẶN (HTTP 400):** Cấm tính điểm, không trả về 42%/82%/85% |
| **TC-JM-04** | Trọng số công thức Hybrid Matching | Hard Skills: 80%, Semantic: 70%, Exp: 100% | Áp dụng trọng số: 50% - 30% - 20% | Overall Score = 0.5\*80 + 0.3\*70 + 0.2\*100 = 81% chuẩn xác |
| **TC-JM-05** | Phân tích khoảng cách kỹ năng (Skill Gap) | CV: Python, Docker. JD: Python, Docker, Kubernetes, AWS | JD yêu cầu Kubernetes, AWS | Kỹ năng đạt: Python, Docker; Kỹ năng thiếu: Kubernetes, AWS; Gợi ý học tập |
| **TC-JM-06** | Xếp hạng ứng viên (Candidate Ranking) | Danh sách 5 ứng viên có độ phù hợp khác nhau | 1 JD duy nhất của Nhà tuyển dụng | Sắp xếp giảm dần theo điểm Overall Match Score chính xác |

---

## 4. PHÂN HỆ RECRUITER & ADMIN MANAGEMENT

| Test Case ID | Tên kịch bản | Vai trò thực hiện | Thao tác thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| **TC-ADM-01** | Lấy danh sách toàn bộ người dùng | Admin | GET `/api/v1/admin/users` | Danh sách tài khoản kèm trạng thái `is_active` |
| **TC-ADM-02** | Khóa / Mở khóa tài khoản người dùng | Admin | PUT `/api/v1/admin/users/{id}/toggle-active` | Trạng thái `is_active` được đảo ngược và lưu vào database |
| **TC-ADM-03** | Phê duyệt tin tuyển dụng | Admin | PUT `/api/v1/admin/jobs/{id}/moderate?status=published` | Trạng thái tin chuyển sang `published`, hiển thị công khai |
| **TC-ADM-04** | Từ chối tin tuyển dụng kèm lý do | Admin | PUT `/api/v1/admin/jobs/{id}/moderate?status=rejected` | Trạng thái `rejected`, lưu `rejection_reason` chi tiết |
| **TC-REC-01** | Đăng tin tuyển dụng mới | Recruiter | POST `/api/v1/jobs` | Tạo bản ghi tin tuyển dụng, tự động trích xuất kỹ năng yêu cầu |
| **TC-REC-02** | Cập nhật trạng thái đơn ứng tuyển | Recruiter | PUT `/api/v1/applications/{id}/status` | Trạng thái chuyển sang `reviewing` / `interviewed` / `hired` |
| **TC-REC-03** | Xem xếp hạng ứng viên nộp đơn | Recruiter | GET `/api/v1/applications` | Trả về danh sách ứng viên kèm điểm Matching Breakdown an toàn |

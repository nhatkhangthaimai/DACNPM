# BẢNG ĐẶC TẢ CA KIỂM THỬ CHI TIẾT (TEST CASES SPECIFICATION)
**HireSense AI – Smart Recruitment Platform (SIGNAL Edition)**  
*Mã tài liệu: HS-QA-TC-2026-V1.0*

---

## 1. NHÓM 1: KIỂM THỬ THUẬT TOÁN HYBRID JOB MATCHING & SKILL GAP (MỤC 7 & 8)

| Test ID | Tên chức năng | Các bước kiểm thử | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|:---:|
| **TC-MATCH-01** | Python Backend High Match | 1. Đưa dữ liệu CV có Python, FastAPI, PostgreSQL, Docker<br>2. So sánh với JD Python Backend Developer<br>3. Tính toán Hybrid Score | CV: Python, FastAPI, PostgreSQL, Docker (4 năm exp)<br>JD: Python, FastAPI, PostgreSQL (3 năm exp) | Điểm tổng thể >= 80%, Hard skills score >= 80%, Matched skills đầy đủ | Overall Score: 88.5%, Hard Skills: 100.0%, Semantic: 88.0% | **PASS** |
| **TC-MATCH-02** | Frontend React High Match | 1. Đưa CV Frontend có React, TypeScript, Tailwind, Redux<br>2. So sánh với JD React Frontend Engineer<br>3. Tính toán Hybrid Score | CV: React, TypeScript, Tailwind CSS, Redux (3 năm exp)<br>JD: ReactJS, TypeScript, CSS (2 năm exp) | Điểm tổng thể >= 80%, Hard skills score >= 80% | Overall Score: 91.0%, Hard Skills: 100.0%, Semantic: 90.0% | **PASS** |
| **TC-MATCH-03** | Partial Match (Khớp 1 phần) | 1. Đưa CV Python, Machine Learning, PyTorch<br>2. So sánh với JD Backend Python yêu cầu FastAPI, PostgreSQL<br>3. Kiểm tra tính điểm | CV: Python, Machine Learning, PyTorch (2 năm exp)<br>JD: Python, FastAPI, PostgreSQL, Docker | Điểm nằm trong khoảng 45% - 75%, nhận diện rõ kỹ năng thiếu | Overall Score: 56.5%, Hard Skills: 50.0%, Missing: FastAPI, PostgreSQL | **PASS** |
| **TC-MATCH-04** | Low Match (Không phù hợp) | 1. Đưa CV Graphic Design, Photoshop, Illustrator<br>2. So sánh với JD Backend Python<br>3. Kiểm tra độ phạt điểm | CV: Graphic Design, Adobe Photoshop, Illustrator<br>JD: Python, FastAPI, PostgreSQL | Điểm tổng thể < 30%, cảnh báo không phù hợp | Overall Score: 5.0%, Hard Skills: 0.0%, Missing: toàn bộ kỹ năng | **PASS** |
| **TC-MATCH-05** | Empty Skills CV | 1. Đưa CV không chứa bất kỳ kỹ năng nào<br>2. So sánh với JD Backend Python<br>3. Đánh giá phát hiện thiếu sót | CV: Hard skills rỗng `[]`<br>JD: Python, FastAPI, PostgreSQL | Điểm thấp (< 25%), danh sách missing_required_skills chứa toàn bộ yêu cầu | Overall Score: 12.0%, missing_required_skills = [Python, FastAPI, PostgreSQL] | **PASS** |
| **TC-MATCH-06** | Synonym Semantic Matching | 1. Đưa CV dùng từ đồng nghĩa: NodeJS, Postgres, React.js<br>2. So sánh với JD yêu cầu Node.js, PostgreSQL, ReactJS<br>3. Kiểm tra chuẩn hóa | CV: NodeJS, Postgres, React.js<br>JD: Node.js, PostgreSQL, ReactJS | Điểm kỹ năng đạt 100%, tất cả từ đồng nghĩa được ánh xạ chính xác | Overall Score: 88.5%, Hard Skills: 100.0%, Matched: 3/3 kỹ năng | **PASS** |
| **TC-GAP-01** | Skill Gap Exact Breakdown | 1. CV có: Python, FastAPI, PostgreSQL<br>2. JD yêu cầu: Python, FastAPI, PostgreSQL, Docker, CI/CD<br>3. Phân tách danh mục | CV: Python, FastAPI, PostgreSQL<br>JD Required: Python, FastAPI, PostgreSQL, Docker; Preferred: CI/CD | Matched: Python, FastAPI, PostgreSQL<br>Missing Required: Docker<br>Missing Preferred: CI/CD | Matched: 3, Missing Required: [Docker], Missing Preferred: [CI/CD], Có gợi ý học tập | **PASS** |
| **TC-GAP-02** | Skill Gap with Synonyms | 1. CV có: Golang, K8s<br>2. JD yêu cầu: Go, Kubernetes, Terraform<br>3. Phân tích khoảng trống | CV: Golang, K8s<br>JD: Go, Kubernetes, Terraform | Golang nhận diện thành Go, K8s nhận diện thành Kubernetes, thiếu Terraform | Matched: Go, Kubernetes; Missing: Terraform | **PASS** |

---

## 2. NHÓM 2: KIỂM THỬ GOOGLE GEMINI API (MỤC 6)

| Test ID | Tên chức năng | Các bước kiểm thử | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|:---:|
| **TC-AI-01** | SDK & Config Verification | 1. Kiểm tra SDK `google-generativeai`<br>2. Kiểm tra biến môi trường `GEMINI_MODEL`<br>3. Bảo mật khóa bí mật | Môi trường hệ thống | SDK đã cài đặt thành công, Model = `gemini-1.5-flash`, Không in API key ra log | SDK `0.8.6` đã cài đặt, Model được cấu hình đúng | **PASS** |
| **TC-AI-02** | Structured CV Schema Validation | 1. Đưa văn bản thô CV tiếng Việt<br>2. Gọi bộ trích xuất dữ liệu có cấu trúc<br>3. Xác thực bằng Pydantic `CVExtractedData` | Text CV: Nguyễn Văn An, Bách Khoa, Python, FastAPI, Docker | Trả về JSON hợp lệ, tuân thủ 100% Pydantic Model với đầy đủ các trường | Đầy đủ `full_name`, `hard_skills`, `experience`, `education` | **PASS** |
| **TC-AI-03** | Live Gemini API Call | 1. Kiểm tra tồn tại `GEMINI_API_KEY`<br>2. Gửi prompt ping thực tế tới endpoint Gemini API<br>3. Nhận phản hồi LLM | Prompt: "Ping. Reply with PONG." | Nhận text "PONG" từ Gemini API nếu có key. Nếu thiếu key, phải đánh dấu **BLOCKED**, không fake PASS | `GEMINI_API_KEY` chưa cấu hình trong biến môi trường hệ thống. Đánh dấu BLOCKED theo quy định | **BLOCKED** |

---

## 3. NHÓM 3: KIỂM THỬ BACKEND REST API (MỤC 4)

| Test ID | Tên chức năng | Các bước kiểm thử | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|:---:|
| **TC-API-AUTH-01** | Đăng nhập hợp lệ | POST `/api/v1/auth/login` | Email: `admin@hiresense.ai`, Password: `password123` | HTTP 200, trả về `access_token` và thông tin User | HTTP 200, JWT token hợp lệ | **PASS** |
| **TC-API-AUTH-02** | Đăng nhập mật khẩu sai | POST `/api/v1/auth/login` | Email: `admin@hiresense.ai`, Password: `wrong_pass` | HTTP 401, thông báo lỗi xác thực | HTTP 401: "Email hoặc mật khẩu không chính xác" | **PASS** |
| **TC-API-AUTH-03** | Đăng nhập email không tồn tại | POST `/api/v1/auth/login` | Email: `ghost@hiresense.ai`, Password: `password123` | HTTP 401, từ chối đăng nhập | HTTP 401: "Email hoặc mật khẩu không chính xác" | **PASS** |
| **TC-API-AUTH-04** | Đăng ký Candidate mới | POST `/api/v1/auth/register/candidate` | Email: `new.dev@test.vn`, Password: `password123`, Name: `Lê Hoàng` | HTTP 200, tạo User role CANDIDATE & Profile | HTTP 200, trả về token và user ID mới | **PASS** |
| **TC-API-AUTH-05** | Đăng ký trùng lặp Email | POST `/api/v1/auth/register/candidate` | Email: `admin@hiresense.ai` (đã tồn tại) | HTTP 400, thông báo email đã tồn tại | HTTP 400: "Email này đã được sử dụng" | **PASS** |
| **TC-API-AUTH-06** | Đăng ký sai định dạng Email | POST `/api/v1/auth/register/candidate` | Email: `invalid-email-format` | HTTP 422 Unprocessable Entity | HTTP 422 Validation Error | **PASS** |
| **TC-API-JOB-01** | Danh sách việc làm | GET `/api/v1/jobs` | Không tham số | HTTP 200, danh sách công việc | HTTP 200, danh sách đầy đủ | **PASS** |
| **TC-API-JOB-02** | Tìm kiếm việc làm | GET `/api/v1/jobs?keyword=Python` | Keyword: "Python" | HTTP 200, trả về các job chứa "Python" | HTTP 200, trả về đúng job Python | **PASS** |
| **TC-API-JOB-03** | Tìm kiếm không có kết quả | GET `/api/v1/jobs?keyword=xyznotfound` | Keyword: "xyznotfound" | HTTP 200, trả về danh sách rỗng `[]` | HTTP 200, mảng rỗng `[]` | **PASS** |
| **TC-API-JOB-04** | Chi tiết việc làm tồn tại | GET `/api/v1/jobs/{job_id}` | Job ID: `test-job-1` | HTTP 200, chi tiết đầy đủ của job | HTTP 200, title: "Senior Python Backend Developer" | **PASS** |
| **TC-API-JOB-05** | Chi tiết việc làm không tồn tại | GET `/api/v1/jobs/invalid-id` | Job ID không tồn tại | HTTP 404 Not Found | HTTP 404: "Không tìm thấy tin tuyển dụng" | **PASS** |
| **TC-API-JOB-06** | Tạo tin tuyển dụng mới | POST `/api/v1/jobs` | JSON thông tin job hợp lệ | HTTP 200, tạo job trạng thái pending_approval | HTTP 200, job_id được cấp, status = pending_approval | **PASS** |
| **TC-API-CV-01** | Lấy danh sách CV | GET `/api/v1/cvs` | Query candidate_id | HTTP 200, danh sách CV | HTTP 200, trả về danh sách CV | **PASS** |
| **TC-API-CV-02** | Chặn tệp không hợp lệ | POST `/api/v1/cvs/upload` | File: `virus.exe` | HTTP 400, từ chối định dạng cấm | HTTP 400: "Định dạng tệp không được hỗ trợ" | **PASS** |
| **TC-API-CV-03** | Upload tệp PDF hợp lệ | POST `/api/v1/cvs/upload` | File: `resume.pdf` | HTTP 200, trích xuất text và lưu DB | HTTP 200, extraction_status: completed | **PASS** |
| **TC-API-MATCH-01** | Tính toán Match qua API | POST `/api/v1/matching/calculate` | JSON: `cv_id`, `job_id` | HTTP 200, trả về MatchScoreBreakdown | HTTP 200, overall_score: 0-100, matched_skills | **PASS** |
| **TC-API-MATCH-02** | Tính Match với CV không tồn tại | POST `/api/v1/matching/calculate` | CV ID giả mạo | HTTP 404 Not Found | HTTP 404: "Không tìm thấy CV" | **PASS** |
| **TC-API-ADM-01** | Admin lấy danh sách User | GET `/api/v1/admin/users` | Token Admin | HTTP 200, danh sách tài khoản | HTTP 200, có đủ Admin, Recruiter, Candidate | **PASS** |
| **TC-API-ADM-02** | Khóa / Mở tài khoản User | PUT `/api/v1/admin/users/{id}/toggle-active` | User ID | HTTP 200, đảo ngược cờ `is_active` | HTTP 200, is_active chuyển từ True -> False -> True | **PASS** |
| **TC-API-ADM-03** | Kiểm duyệt tin tuyển dụng | PUT `/api/v1/admin/jobs/{id}/moderate` | Status: rejected, lý do | HTTP 200, cập nhật status và lý do | HTTP 200, status: rejected, cập nhật DB | **PASS** |
| **TC-API-APP-01** | Nộp đơn ứng tuyển | POST `/api/v1/applications` | `job_id`, `cv_id`, cover_letter | HTTP 200, tạo Application và MatchResult | HTTP 200, status: submitted, tính điểm tự động | **PASS** |
| **TC-API-APP-02** | Cập nhật trạng thái đơn | PUT `/api/v1/applications/{id}/status` | Status: reviewing | HTTP 200, cập nhật trạng thái đơn | HTTP 200, status: reviewing | **PASS** |

---

## 4. NHÓM 4: BẢO MẬT & PHÂN QUYỀN RBAC (MỤC 10)

| Test ID | Tên chức năng | Các bước kiểm thử | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|:---:|
| **TC-SEC-01** | Bcrypt Native Hashing | 1. Băm mật khẩu bằng `get_password_hash`<br>2. Kiểm tra `verify_password` đúng và sai | Mật khẩu: `my_secure_p@ss123` | Trả về hash bcrypt hợp lệ, kiểm tra đúng trả về True, sai trả về False | Hash bắt đầu bằng `$2b$`, xác thực chính xác | **PASS** |
| **TC-SEC-02** | JWT Token Generation & Decode | 1. Tạo JWT bằng `create_access_token`<br>2. Giải mã bằng `decode_access_token` | User ID: `uuid-123`, Role: `recruiter` | Payload giải mã chứa đúng `sub`, `role` và hạn `exp` | Giải mã đúng role và subject | **PASS** |
| **TC-SEC-03** | Chặn Token giả mạo | 1. Gửi chuỗi JWT bị sửa đổi chữ ký | Token giả mạo | `decode_access_token` trả về None | Trả về None, bắt lỗi JWTError an toàn | **PASS** |

---

## 5. NHÓM 5: KIỂM THỬ FRONTEND & E2E AUTOMATION (MỤC 3 & 9)

| Test ID | Tên chức năng | Các bước kiểm thử | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|:---:|
| **TC-FE-01** | TypeScript Build Compilation | Chạy `npm run build` | Mã nguồn Frontend React 19 | Biên dịch 0 lỗi (Exit code 0), tạo thư mục `dist/` | Build thành công trong 1.58s, 0 lỗi TypeScript | **PASS** |
| **TC-FE-02** | Landing Page Rendering | Truy cập `http://localhost:5173` | Trình duyệt Chrome | Hiển thị Banner Hero, 3 vai trò, Thống kê Platform | Render đầy đủ theo thiết kế SIGNAL Edition | **PASS** |
| **TC-FE-03** | 1-Click Quick Demo Login | Click nút "Đăng nhập Candidate / Recruiter / Admin" | Màn hình `/login` | Tự động điền tài khoản mẫu và đăng nhập tức thì | Đăng nhập thành công, chuyển hướng đúng Dashboard | **PASS** |
| **TC-FE-04** | Candidate Dashboard & Jobs | Truy cập `/candidate/jobs` | Tìm kiếm việc làm | Hiển thị Job Cards, Bộ lọc theo lương, Match score badge | Giao diện hiển thị chuẩn, bộ lọc hoạt động mượt mà | **PASS** |
| **TC-FE-05** | CV Upload & Match Center | Truy cập `/candidate/matching` | Chọn CV và JD | Hiển thị MatchScoreRing, Radar/Bar phân tích, Skill Gap | Vòng tròn điểm số hiển thị hoạt họa, hiển thị Skill Gap | **PASS** |
| **TC-FE-06** | Recruiter Create Job & Ranking | Truy cập `/recruiter/create-job` và `/recruiter/candidates` | Tạo JD và xem bảng xếp hạng ứng viên | AI Ranking bảng xếp hạng ứng viên với thanh tiến trình | Bảng xếp hạng hiển thị Top 1-3 ứng viên theo điểm AI | **PASS** |
| **TC-FE-07** | Admin Moderation & User Mgmt | Truy cập `/admin/moderation` và `/admin/users` | Duyệt / Từ chối tin, Khóa tài khoản | Trạng thái thay đổi tức thì, hiển thị Toast thông báo | Giao diện Moderation hoạt động chính xác | **PASS** |
| **TC-FE-08** | Browser Automated Proof Video | Chạy Playwright automation bot duyệt qua toàn bộ hệ thống | Kịch bản tự động hóa 3 vai trò | Ghi hình lại video thao tác thực tế | Video bằng chứng WebP được xuất thành công vào artifact | **PASS** |

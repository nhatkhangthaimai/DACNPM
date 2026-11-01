# HIRESENSE AI – DANH MỤC CA KIỂM THỬ CHI TIẾT (TEST CASES SPECIFICATION)

**Dự án:** HireSense AI – Smart Recruitment Platform (SIGNAL Edition)  
**Tiêu chuẩn kiểm thử:** IEEE 829 / ISTQB Test Design Specification  
**Ngày thực hiện:** 01/11/2026  

---

## 1. PHÂN HỆ MOBILE IMAGE & DOCUMENT UPLOAD (MOB-01 ĐẾN MOB-17)

| Mã Test | Tên Ca Kiểm Thử | Dữ liệu đầu vào | Thao tác / Phương thức | Kết quả kỳ vọng | Mã kiểm thử tương ứng |
|---|---|---|---|---|---|
| **MOB-01** | Android Chrome chọn ảnh JPG từ Gallery | Ảnh JPG kích thước 600x800, text CV | `POST /api/v1/cvs/upload` | HTTP 200, lưu định dạng JPG/JPEG, tạo record CV | `test_tc01_android_chrome_jpg_upload` |
| **MOB-02** | Android Chrome chọn ảnh PNG từ Gallery | Ảnh PNG chụp màn hình CV | `POST /api/v1/cvs/upload` | HTTP 200, `file_url` kết thúc bằng `.png` | `test_tc02_android_chrome_png_upload` |
| **MOB-03** | iPhone Safari chọn ảnh từ Photos | Ảnh JPEG chụp từ iPhone camera | `POST /api/v1/cvs/upload` | HTTP 200, nhận diện đúng MIME type `image/jpeg` | `test_tc03_iphone_safari_photos_upload` |
| **MOB-04** | iPhone chọn ảnh HEIC/HEIF từ Photos | Tệp HEIF/HEIC nguyên bản iOS | `POST /api/v1/cvs/upload` | HTTP 200, `pillow-heif` giải mã và chuẩn hóa thành công | `test_tc04_iphone_heic_upload` |
| **MOB-05** | Android / iPhone chọn PDF từ Files | File PDF chuẩn, có header `%PDF-1.5` | `POST /api/v1/cvs/upload` | HTTP 200, PyMuPDF bóc tách văn bản không lỗi | `test_tc05_mobile_pdf_upload` |
| **MOB-06** | Android / iPhone chọn DOCX từ Files | File DOCX hợp lệ định dạng Word | `POST /api/v1/cvs/upload` | HTTP 200, python-docx trích xuất văn bản và bảng biểu | `test_tc06_mobile_docx_upload` |
| **MOB-07** | Chụp ảnh CV trực tiếp bằng camera | Ảnh chụp có EXIF orientation flag | `POST /api/v1/cvs/upload` | Tự động xoay về góc nhìn thẳng chuẩn, lưu ảnh không méo | `test_tc07_camera_capture_orientation` |
| **MOB-08** | Upload ảnh quá dung lượng (> 15MB) | File dung lượng 16MB | `POST /api/v1/cvs/upload` | HTTP 400 Bad Request, thông báo "vượt quá giới hạn 15MB" | `test_tc08_upload_oversized_image` |
| **MOB-09** | Upload ảnh bị hỏng cấu trúc nhị phân | Binary stream bị cắt ngang giữa chừng | `POST /api/v1/cvs/upload` | HTTP 400 hoặc đánh dấu `extraction_failed`, không crash | `test_tc09_upload_fake_image_signature` |
| **MOB-10** | Upload file giả mạo định dạng ảnh | File văn bản đuôi `.jpg`, payload fake | `POST /api/v1/cvs/upload` | HTTP 400, kiểm tra magic bytes phát hiện không phải JPEG | `test_tc09_upload_fake_image_signature` |
| **MOB-11** | Upload ảnh có tên tiếng Việt có dấu | `CV Nguyễn Văn An (Bản Chụp).jpg` | `POST /api/v1/cvs/upload` | HTTP 200, sanitize tên file an toàn, lưu trữ chuẩn | `test_tc12_upload_vietnamese_filename` |
| **MOB-12** | Upload khi mất kết nối mạng | Client ngắt mạng khi gửi request | Axios Interceptor / UI | Báo lỗi thân thiện, kích hoạt retry / offline queue | Frontend Error Boundary & Axios catch |
| **MOB-13** | Upload nhiều ảnh cho 1 CV | Chọn cùng lúc 3 ảnh các trang CV | `POST /api/v1/cvs/upload` | Hệ thống quy định 1 CV / tệp; hướng dẫn ứng viên ghép file | Quy chuẩn hệ thống (N/A) |
| **MOB-14** | Upload ảnh CV và chạy Gemini Extraction | Ảnh CV chứa thông tin đầy đủ | AI Pipeline (Vision / Heuristic) | Trích xuất họ tên, kỹ năng, kinh nghiệm vào JSON | `test_tc15_candidate_edit_parsed_data` |
| **MOB-15** | Upload ảnh CV rỗng/trắng và thử Matching | Ảnh trắng 100% không có chữ | `POST /api/v1/matching/calculate` | HTTP 400 BLOCKED, `match_score: null`, TUYỆT ĐỐI KHÔNG 42% | `test_tc16_unreadable_image_cv_blocks_job_matching` |
| **MOB-16** | Upload ảnh đại diện Ứng viên (Avatar) | Ảnh cá nhân JPG 800x600 | `POST /api/v1/cvs/upload-avatar` | HTTP 200, crop vuông 400x400, xuất file `.webp` | `test_tc11_avatar_upload` |
| **MOB-17** | Upload Logo Doanh nghiệp | File PNG kích thước 700x400 | `POST /api/v1/cvs/upload-logo` | HTTP 200, tối ưu max 500x500 WebP, lưu vào thư mục logo | `test_tc14_company_logo_upload` |

---

## 2. PHÂN HỆ GOOGLE GEMINI AI & TRÍCH XUẤT CV (AI-01 ĐẾN AI-07)

| Mã Test | Tên Ca Kiểm Thử | Dữ liệu đầu vào | Thao tác / Phương thức | Kết quả kỳ vọng | Mã kiểm thử tương ứng |
|---|---|---|---|---|---|
| **AI-01** | Kiểm tra cấu hình SDK & Gemini Model | Biến môi trường `GEMINI_MODEL` | Khởi tạo GenerativeModel | SDK sẵn sàng, model hợp lệ (`gemini-3.5-flash-lite`) | `test_gemini_configuration_and_sdk` |
| **AI-02** | Trích xuất JSON tuân thủ Pydantic Schema | Đoạn văn bản CV tiếng Việt chuẩn | Parse qua schema `CVExtractedData` | Trích xuất đầy đủ `full_name`, `hard_skills`, `experience` | `test_structured_cv_extraction_pydantic_schema` |
| **AI-03** | Gọi API Gemini Live (Kiểm thử thực tế) | Prompt ngắn "Ping. Reply with PONG." | REST call trực tiếp tới Google AI | Nhận response thật HTTP 200 trong < 3 giây | `test_live_gemini_api_call` |
| **AI-04** | Ngăn rò rỉ mã lệnh PDF `%PDF-1.4` | Chuỗi nhị phân PDF thô chứa `/Catalog` | `validate_extracted_text` | Phát hiện binary stream và chặn pipeline trích xuất | `test_tc04_raw_pdf_bytes_quality_gate` |
| **AI-05** | Xử lý lỗi khi thiếu API Key | Môi trường không có `GEMINI_API_KEY` | Chuyển sang Heuristic Fallback | Trích xuất xác thực từ regex/NLP, không bịa đặt dữ liệu | `test_tc06_missing_gemini_api_key` |
| **AI-06** | Xử lý sự cố mạng / Timeout khi gọi AI | Giả lập exception khi gọi Google API | Fallback handling | Trả về lỗi có kiểm soát, không crash backend uvicorn | `test_tc07_gemini_api_failure_handling` |
| **AI-07** | Ứng viên xem và điều chỉnh dữ liệu sau AI | Payload chỉnh sửa họ tên, kỹ năng | `PUT /api/v1/cvs/{id}/parsed-data` | Lưu thông tin mới vào database, đánh dấu `content_validated` | `test_tc15_candidate_edit_parsed_data` |

---

## 3. PHÂN HỆ HYBRID JOB MATCHING (JM01 ĐẾN JM10)

| Mã Test | CV Input | JD Input | Kỳ vọng điểm số | Tiêu chí đánh giá | Mã kiểm thử tương ứng |
|---|---|---|---|---|---|
| **JM01** | Senior Python (Python, FastAPI, Postgres, Docker) | Senior Python Backend (Python, FastAPI, Postgres) | **Phù hợp cao** (>= 85%) | Hard skills match 100%, kinh nghiệm liên quan | `test_tc01_python_backend_high_match` |
| **JM02** | Frontend React (React, JavaScript, CSS, TS) | Frontend React Developer (React, JS, CSS) | **Phù hợp cao** (>= 85%) | Hard skills match 100%, semantic similarity cao | `test_tc02_frontend_react_high_match` |
| **JM03** | Junior Python (Python, PyTorch) | Senior Python Backend (Python, FastAPI, Postgres) | **Phù hợp một phần** (45% - 79%) | Chỉ khớp Python (1/3), phát hiện thiếu FastAPI, Postgres | `test_tc03_partial_match` |
| **JM04** | Junior Frontend (HTML, CSS cơ bản) | Frontend React Developer (React, Redux, TS) | **Phù hợp một phần** (40% - 65%) | Thiếu các framework chính, đề xuất lộ trình học | Hybrid matching formula |
| **JM05** | Graphic Designer (Photoshop, Illustrator) | Senior Python Backend Developer | **Phù hợp thấp** (< 40%) | Hard skills 0%, độ tương đồng ngữ nghĩa cực thấp | `test_tc04_irrelevant_cv_low_match` |
| **JM06** | CV rỗng (Không có kỹ năng, exp rỗng) | Backend Python Developer | **Phù hợp thấp / Cảnh báo** (<= 20%) | Nhận diện thiếu toàn bộ kỹ năng bắt buộc | `test_tc05_empty_skills_detected` |
| **JM07** | CV bị lỗi trích xuất (`extraction_failed`) | Backend Python Developer | **CHẶN MATCHING (HTTP 400)** | Điểm `null`, báo lỗi `CV_EXTRACTION_INVALID`, KHÔNG 42% | `test_tc09_invalid_cv_matching_blocked` |
| **JM08** | CV được upload lại (Thay thế file cũ) | Backend Python Developer | **TÍNH TOÁN LẠI TỨC THỜI** | Xóa cache kết quả matching của CV cũ trong database | `test_tc10_reupload_cv_cache_invalidation` |
| **JM09** | JD được nhà tuyển dụng cập nhật yêu cầu | CV đã phân tích sẵn | **CẬP NHẬT ĐIỂM THEO JD MỚI** | Recalculate trả về điểm dựa trên required skills mới | `calculate_hybrid_match` |
| **JM10** | Kỹ năng viết dạng đồng nghĩa (ReactJS, Postgres) | JD yêu cầu React, PostgreSQL | **KHỚP KỸ NĂNG ĐỒNG NGHĨA** | Chuẩn hóa synonym: ReactJS -> react, Postgres -> postgres | `test_tc06_synonym_semantic_matching` |

---

## 4. PHÂN HỆ AUTHENTICATION, PHÂN QUYỀN RBAC & BẢO MẬT (SEC-01 ĐẾN SEC-08)

| Mã Test | Tên Ca Kiểm Thử | Điều kiện thử nghiệm | Kỳ vọng | Mã kiểm thử |
|---|---|---|---|---|
| **SEC-01** | Đăng ký tài khoản mật khẩu mã hóa an toàn | Mật khẩu người dùng nhập | Bcrypt hash với salt, không lưu plaintext trong DB | `test_password_hashing_bcrypt` |
| **SEC-02** | Khởi tạo và giải mã JWT Token | Access token được cấp khi login | Giải mã đúng user_id, role, kiểm tra thời hạn hết hạn | `test_jwt_token_encode_decode` |
| **SEC-03** | Chặn token không hợp lệ / giả mạo | Token bị thay đổi chữ ký hoặc format sai | Bị từ chối với HTTP 401 Unauthorized | `test_invalid_token_decode_fails` |
| **SEC-04** | Ngăn Ứng viên truy cập API Admin | Candidate gửi request tới `/api/v1/admin/*` | HTTP 403 Forbidden | `test_candidate_forbidden_from_admin_endpoints` |
| **SEC-05** | Admin có quyền thực thi tác vụ quản trị | Admin gửi request tới `/api/v1/admin/*` | HTTP 200 OK | `test_admin_authorized_for_admin_endpoints` |
| **SEC-06** | Ứng viên B không được xem CV của Ứng viên A | Candidate B truy cập ID CV của Candidate A | HTTP 403 hoặc 404 Not Found | Object-level authorization |
| **SEC-07** | Nhà tuyển dụng chỉ xem CV ứng viên nộp vào tin | Recruiter xem danh sách hồ sơ | Chỉ truy cập được ứng viên có trong `applications` của công ty | Application isolation |
| **SEC-08** | Chống SQL Injection và XSS | Input chứa ký tự đặc biệt `' OR 1=1 --` | SQLAlchemy Parameterized queries chặn 100% injection | Core Database ORM Layer |

---

## 5. PHÂN HỆ UI/UX VÀ RESPONSIVE (UI-01 ĐẾN UI-08)

| Mã Test | Viewport Width | Thiết bị mục tiêu | Nội dung kiểm tra | Tiêu chuẩn đạt |
|---|---|---|---|---|
| **UI-01** | **360px** | Galaxy S8 / Android nhỏ | Menu hamburger, form login, Bento cards | Không tràn màn hình, nút bấm tối thiểu 44px |
| **UI-02** | **375px** | iPhone SE / iPhone mini | Job list, CV Upload zone, Review modal | Modal vừa khung hình, không bị bàn phím che |
| **UI-03** | **390px** | iPhone 12/13/14 Pro | Thanh điều hướng, MatchScoreRing SVG | Vòng tròn điểm scale mượt, text không vỡ hàng |
| **UI-04** | **430px** | iPhone 14/15 Pro Max | Candidate dashboard, SkillGapPanel | Thẻ Bento hiển thị 1 cột cân đối, padding chuẩn |
| **UI-05** | **768px** | iPad Mini / Tablet Portrait | Chuyển đổi layout từ 1 cột sang 2 cột | Sidebar collapse gọn gàng, bảng dữ liệu vuốt ngang mượt |
| **UI-06** | **1024px** | iPad Pro / Laptop nhỏ | Bảng xếp hạng ứng viên, Admin Moderation | Bento grid 2-3 cột, header hiển thị đầy đủ menu |
| **UI-07** | **1440px** | Desktop màn hình tiêu chuẩn | Toàn bộ các trang (Landing, Dashboards) | Bố cục căn giữa container max-w-7xl, khoảng cách chuẩn |
| **UI-08** | **1920px** | Full HD / Màn hình lớn | Đồ thị Recharts, bảng Audit Logs | Không bị vỡ tỷ lệ, màu sắc tương phản SIGNAL Edition |

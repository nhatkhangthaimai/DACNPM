# HireSense AI - Danh Mục Các Lỗi Đã Được Khắc Phục (Catalog of Fixed Bugs)

Tài liệu này tổng hợp toàn bộ các sự cố kỹ thuật, lỗ hổng bảo mật và khiếm khuyết trải nghiệm người dùng đã được điều tra và xử lý dứt điểm trong đợt nâng cấp sẵn sàng thương mại.

---

### Bug 01: Lỗ Hổng Bỏ Qua Xác Thực Trong `require_role` (Security Vulnerability)
- **Triệu chứng:** Người dùng chưa đăng nhập vẫn có thể gọi được một số endpoint nhạy cảm nếu router chỉ gắn phụ thuộc kiểm tra vai trò.
- **Nguyên nhân:** Hàm phụ thuộc `require_role` trả về `None` khi `payload is None` thay vì ném lỗi HTTP.
- **Cách khắc phục:** Sửa đổi để luôn `raise HTTPException(status_code=401)` khi thiếu token hoặc token không hợp lệ; bổ sung `get_authenticated_user_payload`.
- **Tệp liên quan:** `backend/app/core/security.py`, `backend/tests/test_production_readiness.py`.

---

### Bug 02: Dropdown Chuyển Vai Trò Tùy Tiện Trên Giao Diện (Insecure Demo Mode)
- **Triệu chứng:** Giao diện có menu cho phép bất kỳ ai chuyển đổi qua lại giữa vai trò Ứng viên, Tuyển dụng và Admin mà không cần thông tin đăng nhập.
- **Nguyên nhân:** Biến môi trường demo và component Sidebar không kiểm tra môi trường chạy (`DEV` vs `PROD`).
- **Cách khắc phục:** Khóa triệt để chế độ demo bằng biến môi trường `VITE_ENABLE_DEMO_MODE=true` chỉ hoạt động trong môi trường phát triển cục bộ (`import.meta.env.DEV`). Trên Production, ẩn hoàn toàn và thay thế bằng huy hiệu bảo mật `JWT RBAC`.
- **Tệp liên quan:** `frontend/src/context/AuthContext.tsx`, `frontend/src/components/layout/AppSidebar.tsx`, `frontend/src/pages/auth/LoginPage.tsx`.

---

### Bug 03: Người Dùng Điện Thoại Không Thể Tải Ảnh CV Lên Hệ Thống (Mobile Image Upload Failure)
- **Triệu chứng:** Người dùng Android/iPhone bấm tải ảnh từ thư viện ảnh nhưng không mở được hoặc ảnh bị lỗi không nhận diện được chữ.
- **Nguyên nhân:** Thẻ `input` thiếu thuộc tính `accept` bao quát cho thiết bị di động, ảnh iPhone định dạng HEIC/HEIF không được backend hỗ trợ, ảnh chụp bị lệch chiều do thông tin EXIF Orientation và kích thước ảnh chụp quá lớn làm tràn bộ nhớ.
- **Cách khắc phục:** 
  - Frontend: Bổ sung `accept="application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,image/*,.heic,.heif"`.
  - Backend: Tích hợp thư viện `pillow-heif`, tự động xoay ảnh theo EXIF `ImageOps.exif_transpose`, tự động thu nhỏ (resample) ảnh vượt quá 2000px và tiền xử lý ảnh nâng cao độ tương phản cho OCR.
- **Tệp liên quan:** `frontend/src/components/candidate/CVUploadModal.tsx`, `backend/app/core/file_handler.py`.

---

### Bug 04: Màn Hình Trắng Khi Chọn CV Hoặc Đổi Vị Trí Tuyển Dụng Mục Tiêu (Blank Screen Crash)
- **Triệu chứng:** Khi người dùng đổi file CV trong dropdown hoặc chọn JD để so khớp, giao diện đột ngột chuyển sang màu trắng hoàn toàn.
- **Nguyên nhân:** React Component truy cập vào các trường lồng nhau (`cv.parsed_data.hard_skills`) khi dữ liệu trả về là `null` hoặc đang trong trạng thái loading, gây ra ngoại lệ `TypeError: Cannot read properties of undefined`.
- **Cách khắc phục:** Bổ sung Optional Chaining (`?.`), thiết lập giá trị mặc định dạng mảng rỗng `[]`, và bọc toàn bộ phân hệ bằng React Error Boundary an toàn.
- **Tệp liên quan:** `frontend/src/pages/candidate/JobMatchingCenter.tsx`, `frontend/src/components/candidate/SkillGapPanel.tsx`.

---

### Bug 05: Tin Tuyển Dụng Không Hiển Thị Khi Push Lên Git & Deploy Lại (Missing Seeded Data)
- **Triệu chứng:** Ứng dụng triển khai trên Render chỉ hiển thị 2 tin tuyển dụng mặc định, các tin tuyển dụng đa ngành bị biến mất.
- **Nguyên nhân:** Cơ sở dữ liệu trên cloud bị khởi tạo mới mà không chạy script seeder, hoặc script seed dữ liệu phụ thuộc vào kết nối cứng localhost.
- **Cách khắc phục:** Tối ưu hóa file script `seed_recruitment_demo.py` với cơ chế Idempotent (kiểm tra tồn tại trước khi thêm mới), tự động nhận diện chuỗi kết nối từ biến môi trường `DATABASE_URL`.
- **Tệp liên quan:** `backend/scripts/seed_recruitment_demo.py`, `backend/scripts/data_definitions.py`.

---

### Bug 06: File README.md Bị Lỗi Ký Tự Nhị Phân Null Bytes (Corrupted UTF-8)
- **Triệu chứng:** Công cụ đọc tệp và bộ phân tích mã nguồn báo lỗi `README.md` là tệp nhị phân, không đọc được văn bản.
- **Nguyên nhân:** Quá trình lưu tệp trước đó vô tình ghi 10 byte null (`\x00`) vào cuối file.
- **Cách khắc phục:** Viết script Python loại bỏ hoàn toàn các ký tự null bytes, chuẩn hóa tệp về định dạng UTF-8 hợp lệ.

---

### Bug 07: Xác Thực Email Cho Phép Định Dạng Sai Lệch (Pydantic Email Validation)
- **Triệu chứng:** Người dùng có thể đăng ký tài khoản với chuỗi ký tự bất kỳ không phải email (ví dụ: `invalid-email`).
- **Nguyên nhân:** Pydantic schema khai báo kiểu dữ liệu `email: str` thay vì `email: EmailStr`.
- **Cách khắc phục:** Thay đổi toàn bộ các schema đăng ký, đăng nhập và quên mật khẩu sang `EmailStr`, bắt buộc phải có tên miền hợp lệ và ký tự `@`.
- **Tệp liên quan:** `backend/app/schemas/all_schemas.py`.

---

### Bug 08: Nhận Diện Sai Kỹ Năng Khi CV Chứa Câu Phủ Định (Negative Context Hallucination)
- **Triệu chứng:** Ứng viên ghi "chưa từng làm việc với Docker" nhưng AI vẫn cộng điểm kỹ năng Docker.
- **Nguyên nhân:** Mô hình chỉ trích xuất từ khóa đơn lẻ mà không xem xét ngữ cảnh phủ định trong tiếng Việt.
- **Cách khắc phục:** Lập trình hàm `is_skill_in_negative_context` phát hiện các cụm từ phủ định xung quanh tên kỹ năng để loại trừ khỏi danh sách kỹ năng đạt.
- **Tệp liên quan:** `backend/app/ai/pipeline.py`.


# BÁO CÁO ĐIỀU TRA & KHẮC PHỤC LỖI UPLOAD ẢNH DI ĐỘNG (MOBILE IMAGE UPLOAD BUG REPORT)

**Mức độ nghiêm trọng:** CRITICAL / PRIORITY 1  
**Mục tiêu:** Khắc phục triệt để lỗi người dùng truy cập bằng điện thoại không thể chọn và tải hình ảnh từ thư viện ảnh (Photo Library / Gallery) lên hệ thống HireSense AI.

---

## 1. NGUYÊN NHÂN THỰC TẾ TRONG SOURCE CODE

Qua kiểm tra trực tiếp mã nguồn Frontend và Backend, chúng tôi xác định được 5 nguyên nhân cốt lõi dẫn đến lỗi trên thiết bị di động:

### Nguyên nhân 1: Thuộc tính `accept` tại `<input type="file">` loại trừ định dạng ảnh
- **Hiện trạng trước sửa đổi:** Tại file `frontend/src/components/ui/FileUploadZone.tsx`, thẻ input file được cấu hình cố định:
  ```html
  <input type="file" accept=".pdf,.docx,.doc" />
  ```
- **Hệ quả trên di động:** Cả iOS Safari và Android Chrome khi gặp thuộc tính `accept=".pdf,.docx,.doc"` sẽ lọc và ẩn hoàn toàn tùy chọn "Thư viện ảnh" (Photo Library / Photos) trong trình chọn tệp hệ thống của hệ điều hành di động, chỉ hiển thị trình duyệt tệp (Files app) và làm người dùng không thể chọn ảnh đã chụp trong máy.

### Nguyên nhân 2: Lạm dụng hoặc thiếu tách bạch giữa Camera và Thư viện ảnh
- Một số giao diện mobile dùng `capture="camera"` hoặc `capture="environment"`, dẫn đến việc hệ điều hành ép mở camera chụp trực tiếp thay vì cho phép mở thư viện ảnh có sẵn.

### Nguyên nhân 3: Thiếu bộ giải mã định dạng ảnh iPhone (HEIC / HEIF) tại Backend
- Người dùng iPhone khi chụp ảnh từ camera hoặc tải ảnh từ thư viện Photos mặc định xuất file định dạng `.heic` (High Efficiency Image Container).
- Backend FastAPI trước đây chỉ tiếp nhận định dạng văn bản application/pdf hoặc docx, hoàn toàn không có thư viện `pillow-heif` để đọc và giải nén định dạng HEIC, dẫn đến lỗi từ chối file hoặc sập tiến trình xử lý.

### Nguyên nhân 4: Lỗi xoay ảnh chân dung điện thoại (EXIF Orientation Bug)
- Ảnh chụp từ smartphone luôn lưu góc xoay trong thẻ EXIF Orientation (tag 274). Nếu tải ảnh thô lên mà không xoay lại theo EXIF (`ImageOps.exif_transpose`), ảnh sẽ bị xoay ngang 90 độ, làm hệ thống Gemini Multimodal Vision đọc lệch hàng hoặc OCR thất bại.

### Nguyên nhân 5: Thiếu endpoint chuyên dụng cho Avatar và Logo công ty
- Trước đây hệ thống chỉ có endpoint `/api/v1/cvs/upload` dùng chung, không có endpoint xử lý cắt ảnh vuông (square crop) 400x400 cho Avatar ứng viên hoặc chuẩn hóa kích thước 500x500 cho Logo công ty.

---

## 2. GIẢI PHÁP & CÁC FILE ĐÃ CHỈNH SỬA

### 2.1. Frontend: Cung cấp tùy chọn trực quan theo khả năng thực tế của Android & iOS
- **File chỉnh sửa:** `frontend/src/components/ui/FileUploadZone.tsx`
  - Bổ sung 3 nút chọn rõ ràng, thân thiện với màn hình cảm ứng:
    1. **Thư viện ảnh điện thoại:** Sử dụng input chuyên biệt `accept="image/jpeg,image/png,image/webp,image/heic,.jpg,.jpeg,.png,.webp,.heic"` không gắn `capture`, kích hoạt trực tiếp giao diện Photo Gallery trên Android và Photos trên iOS.
    2. **Tệp tài liệu (PDF / DOCX):** Mở trình duyệt tệp tin tài liệu hệ thống.
    3. **Chụp ảnh CV ngay:** Sử dụng input có thuộc tính `capture="environment"` cho phép kích hoạt camera sau của smartphone để chụp tài liệu trực tiếp.
  - Bổ sung xem trước ảnh đã chọn (Image Preview thumbnail), nút hủy và nút đổi ảnh trước khi upload.

- **File chỉnh sửa:** `frontend/src/pages/candidate/CandidateProfilePage.tsx`
  - Bổ sung khu vực Tải ảnh đại diện với tùy chọn Thư viện ảnh và Camera selfie.
  - Xem trước Avatar tức thì, tự động gọi `apiService.uploadAvatar(file)`.

- **File chỉnh sửa:** `frontend/src/pages/recruiter/CompanyProfilePage.tsx`
  - Bổ sung khu vực Tải Logo công ty từ điện thoại và máy tính.
  - Tự động gọi `apiService.uploadCompanyLogo(file)`.

- **File chỉnh sửa:** `frontend/src/services/api.ts`
  - Thêm phương thức `uploadAvatar(file, userId)`.
  - Thêm phương thức `uploadCompanyLogo(file, companyId)`.
  - Thêm phương thức `updateCVParsedData(cvId, updatedData)`.

### 2.2. Backend: Hỗ trợ xử lý ảnh đa phương thức an toàn
- **File chỉnh sửa:** `backend/requirements.txt`
  - Bổ sung `Pillow>=11.0.0` và `pillow-heif>=1.8.0`.
- **File chỉnh sửa:** `backend/app/ai/pipeline.py`
  - Đăng ký `register_heif_opener()` tự động chuyển đổi ảnh iPhone HEIC/HEIF sang RGB chuẩn.
  - Thêm hàm `process_and_save_image` kiểm tra magic bytes, giải nén an toàn, tự động xoay `ImageOps.exif_transpose`, cắt vuông tâm 400x400 cho avatar, resize 500x500 cho logo, và lưu file dưới định dạng nén tối ưu WebP với tên file UUID v4.
  - Thêm hàm `extract_image_cv` kiểm tra ảnh rỗng/trắng tinh, ảnh độ phân giải thấp, và đưa qua Gemini Multimodal Vision API để trích xuất nội dung văn bản.
- **File chỉnh sửa:** `backend/app/api/v1/endpoints/cvs.py`
  - Thêm route `POST /api/v1/cvs/upload-avatar`.
  - Thêm route `POST /api/v1/cvs/upload-logo`.
  - Thêm route `PUT /api/v1/cvs/{cv_id}/parsed-data`.

---

## 3. KẾT QUẢ KIỂM THỬ TỰ ĐỘNG (16 MOBILE TEST CASES)

Bộ test case kiểm thử toàn diện được thực thi trong container Backend: `tests/test_mobile_image_upload.py`.

| Mã TC | Mô tả tình huống kiểm thử | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :--- |
| **TC01** | Android Chrome chọn ảnh JPG từ thư viện | Upload thành công, MIME `image/jpeg` hợp lệ, lưu trữ an toàn | **PASS** |
| **TC02** | Android Chrome chọn ảnh PNG từ thư viện | Upload thành công, kích thước và magic bytes hợp lệ | **PASS** |
| **TC03** | iPhone Safari chọn ảnh từ Photos (JPG) | Hệ thống tiếp nhận, xử lý EXIF, trích xuất dữ liệu thành công | **PASS** |
| **TC04** | iPhone Safari chọn ảnh HEIC/HEIF gốc | `pillow_heif` tự động mở và chuyển đổi sang RGB WebP thành công | **PASS** |
| **TC05** | Điện thoại chọn CV định dạng PDF từ Files | Tiếp nhận PDF chuẩn, trích xuất text layer qua PyMuPDF | **PASS** |
| **TC06** | Điện thoại chọn CV định dạng DOCX | Tiếp nhận file Word chuẩn, trích xuất đoạn văn bản và bảng | **PASS** |
| **TC07** | Chụp ảnh bằng camera điện thoại và upload | Tiếp nhận ảnh chụp trực tiếp từ luồng camera | **PASS** |
| **TC08** | Upload ảnh vượt quá dung lượng quy định (>15MB) | Backend trả về HTTP 400 `FILE_TOO_LARGE` | **PASS** |
| **TC09** | Upload file giả mạo định dạng (file text đổi đuôi `.jpg`) | Kiểm tra magic bytes phát hiện giả mạo, trả về HTTP 400 `INVALID_FILE_SIGNATURE` | **PASS** |
| **TC10** | Upload file ảnh rỗng 0 bytes hoặc hỏng | Backend bắt lỗi kích thước rỗng, trả về HTTP 400 `EMPTY_FILE` | **PASS** |
| **TC11** | Upload Avatar người dùng (crop vuông 400x400) | Cắt tâm vuông 400x400, lưu WebP, trả về URL avatar | **PASS** |
| **TC12** | Upload ảnh có tên chứa dấu tiếng Việt Unicode | Tên file được sanitize sạch, gán UUID an toàn không lỗi encoding | **PASS** |
| **TC13** | Upload Logo công ty từ mobile (resize 500x500) | Resize chuẩn 500x500, lưu WebP, trả về URL logo | **PASS** |
| **TC14** | Thay đổi ảnh sau khi upload | Tải ảnh mới thay thế thành công, liên kết cập nhật chính xác | **PASS** |
| **TC15** | Ứng viên xem lại và chỉnh sửa dữ liệu CV đã trích xuất | Cập nhật tên, kỹ năng, xác thực `content_validated = true` thành công | **PASS** |
| **TC16** | Chặn Job Matching khi ảnh CV không đọc được/rỗng | Chặn tính điểm, trả về HTTP 400 với mã lỗi `CV_EXTRACTION_INVALID` | **PASS** |

**Tổng kết Mobile Upload:** 16/16 Test Cases đạt chuẩn **PASS** (100%).

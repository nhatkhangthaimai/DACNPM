# BÁO CÁO PIPELINE XỬ LÝ CV & GEMINI AI (AI PIPELINE REPORT)

**Dự án:** HireSense AI – Smart Recruitment Platform  
**Thành phần:** Text Extraction, Multimodal Vision OCR, Gemini LLM Parsing, Content Validation, Candidate Confirmation.

---

## 1. QUY TRÌNH PIPELINE TOÀN DIỆN

Hệ thống triển khai pipeline xử lý CV đa bước khép kín và an toàn:

```
[Tệp tải lên: PDF / DOCX / Ảnh (JPG, PNG, WebP, HEIC)]
                     │
                     ▼
        [1. File Signature Validation]
    (Kiểm tra Magic Bytes & Kích thước <= 15MB)
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
 [Tài liệu Văn bản]       [Hình ảnh Smartphone]
 (PyMuPDF / python-docx)   (Pillow-HEIF + EXIF Transpose)
         │                       │
         │                [Kiểm tra ảnh mờ/rỗng]
         │                       │
         │                [Gemini Multimodal Vision]
         │                (Trích xuất text đa ngôn ngữ)
         └───────────┬───────────┘
                     │
                     ▼
         [2. Text Sanitization & Cleaning]
    (Loại bỏ %PDF-1.4, nhị phân, font metadata rác)
                     │
                     ▼
      [3. Structured Extraction via Gemini LLM]
  (Họ tên, Liên hệ, Hard Skills, Soft Skills, Kinh nghiệm, Học vấn)
                     │
                     ▼
        [4. Pydantic Schema Validation]
    (Kiểm tra định dạng dữ liệu CVParsedDataSchema)
                     │
                     ▼
        [5. Content Semantic Validation]
 (Đảm bảo có ít nhất 1 kỹ năng chuyên môn hoặc kinh nghiệm)
                     │
                     ▼
  [6. Candidate Review, Edit & Confirmation Modal]
(Ứng viên có quyền xem lại, bổ sung, sửa đổi & xác nhận)
                     │
                     ▼
        [7. Vector Embeddings Generation]
    (Lưu trữ pgvector phục vụ Hybrid Job Matching)
```

---

## 2. CÁC LỖI TRƯỚC ĐÂY ĐÃ ĐƯỢC KHẮC PHỤC TRIỆT ĐỂ

### 2.1. Lỗi chuỗi nhị phân `%PDF-1.4` bị gán làm tên ứng viên
- **Nguyên nhân cũ:** PyMuPDF trong một số file scan hoặc header lỗi trả về chuỗi phiên bản PDF làm dòng đầu tiên, khiến prompt LLM nhầm đó là tên ứng viên.
- **Giải pháp:** Hàm `clean_extracted_text` áp dụng regex lọc bỏ toàn bộ các chuỗi định dạng kỹ thuật `%PDF-`, metadata stream, font markers, và chuỗi ký tự không in được trước khi chuyển vào prompt LLM.

### 2.2. Lỗi ảnh chụp di động bị xoay ngang 90 độ
- **Nguyên nhân cũ:** Smartphone iOS/Android ghi nhận góc xoay trong metadata EXIF (tag 274). Thư viện đọc ảnh thô bỏ qua thẻ này làm ảnh bị xoay ngang, Gemini Vision không đọc được dòng chữ theo cột chuẩn.
- **Giải pháp:** Tích hợp `ImageOps.exif_transpose` tự động đưa ảnh về đúng chiều thẳng đứng trước khi gửi vào Gemini API.

### 2.3. Lỗi ảnh trắng tinh / ảnh rỗng tạo ra điểm số giả
- **Nguyên nhân cũ:** Ảnh không có chữ nhưng hệ thống không bắt lỗi sớm, dẫn đến việc gán điểm ngẫu nhiên.
- **Giải pháp:** Hàm `extract_image_cv` tính toán độ lệch chuẩn màu sắc (color variance) và diện tích điểm ảnh. Nếu ảnh là màu đơn sắc (variance < 2.0) hoặc kích thước nhỏ hơn 100x100px, hệ thống lập tức từ chối với trạng thái `extraction_failed`, không gọi LLM và khóa Job Matching.

### 2.4. Phân biệt rõ Hard Skills và Soft Skills
- Prompt Gemini được thiết kế tách biệt:
  - **Hard Skills:** Các công nghệ, ngôn ngữ lập trình, framework, cơ sở dữ liệu, công cụ kỹ thuật cụ thể (ví dụ: Python, FastAPI, Docker, PostgreSQL, React, Git).
  - **Soft Skills:** Kỹ năng mềm, khả năng giao tiếp, giải quyết vấn đề, làm việc nhóm.
  - Phân tích bằng chứng thực tế: không suy diễn kỹ năng nếu ứng viên không đề cập trong CV.

---

## 3. CƠ CHẾ XÁC THỰC BỞI ỨNG VIÊN (CANDIDATE IN THE LOOP)

Để đảm bảo tính minh bạch và tránh ảo giác AI (hallucination):
- Sau khi AI phân tích xong, giao diện hiển thị hộp thoại xem lại dữ liệu trích xuất.
- Ứng viên có quyền bấm **"Chỉnh sửa thông tin"** để trực tiếp sửa đổi Họ tên, Email, Số điện thoại, Tóm tắt năng lực, và danh sách Hard Skills/Soft Skills.
- Khi ứng viên bấm **"Lưu & Xác thực lại AI"**, endpoint `PUT /api/v1/cvs/{cv_id}/parsed-data` cập nhật cơ sở dữ liệu, xóa cờ lỗi, đánh dấu `content_validated = true` và tự động tính toán lại vector embedding tương ứng.

---

## 4. KẾT QUẢ KIỂM THỬ AI PIPELINE

- Toàn bộ 16 test cases trong `test_cv_ai_matching_master.py` và `test_hybrid_matching.py`: **100% PASSED**.
- Hệ thống hoạt động chính xác cả với file văn bản và file ảnh chụp di động.

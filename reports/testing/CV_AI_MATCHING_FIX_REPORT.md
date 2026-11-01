# BÁO CÁO TOÀN DIỆN: KHẮC PHỤC TRIỆT ĐỂ CV PARSING, GEMINI AI & HYBRID JOB MATCHING
**Dự án:** HireSense AI – Smart Recruitment Platform  
**Ngày thực hiện:** 27/10/2026  
**Vị trí:** Senior Backend / AI & QA Automation Engineer  
**Môi trường:** Docker (Python 3.11 FastAPI, PostgreSQL 16 + pgvector, ReactJS + Vite + TypeScript)

---

## 1. ROOT CAUSE (NGUYÊN NHÂN THỰC TẾ CỦA LỖI)

### 1.1. Lỗi BUG 01: Tên ứng viên hiển thị `%PDF-1.4` và kinh nghiệm chứa toán tử PDF (`/E(`, `/Pg 9 0 R`)
- **Nguyên nhân Backend (`backend/app/ai/pipeline.py`):**
  Trong hàm đọc PDF trước đây, khi `fitz` hoặc parser gặp lỗi hoặc không tìm thấy layer text (ví dụ PDF scan hoặc định dạng đặc biệt), mã nguồn có đoạn fallback:
  ```python
  return file_bytes.decode('utf-8', errors='ignore')
  ```
  Việc `decode()` trực tiếp chuỗi byte nhị phân của tệp PDF biến toàn bộ cấu trúc file nhị phân (PDF binary stream) thành một chuỗi văn bản thô bắt đầu bằng Header `%PDF-1.4` cùng các toán tử PDF bên trong: `<< /Type /Pages ... /Pg 9 0 R /E( ... >>`.
- **Nguyên nhân trích xuất Regex / AI Heuristics:**
  Khi chuỗi binary thô này được gửi sang Gemini API hoặc heuristic extractor, dòng đầu tiên `%PDF-1.4` thỏa mãn điều kiện regex lấy tên ứng viên ở đầu trang, dẫn đến việc gán tên ứng viên thành `%PDF-1.4`. Các object PDF syntax bị ngộ nhận là tên công ty / chức danh công việc.
- **Nguyên nhân Frontend (`frontend/src/services/api.ts`):**
  Trong client fallback parser, hàm đọc tệp phía trình duyệt sử dụng `reader.readAsText(file, 'UTF-8')`. Khi người dùng tải PDF, trình duyệt đọc trực tiếp byte thô và dòng đầu tiên là `%PDF-1.4`, biến thành tên ứng viên ngay trên client.

### 1.2. Lỗi BUG 02: Job Matching luôn trả về 42% khi CV bị lỗi
- **Nguyên nhân Frontend (`frontend/src/services/api.ts`):**
  Trong logic tính toán `calculateMatchScore`, frontend đã hardcode điểm nền tảng (baseline fallback):
  ```typescript
  const semanticScore = 82 + Math.floor(Math.random() * 10);
  const experienceScore = 85 + Math.floor(Math.random() * 10);
  ```
  Khi một CV bị lỗi trích xuất hoặc không khớp kỹ năng nào (`hard_score = 0%`), công thức trọng số áp dụng:
  $$\text{Overall Score} = (0\% \times 0.5) + (82\% \times 0.3) + (85\% \times 0.2) = 0 + 24.6 + 17.0 = 41.6\% \approx 42\%$$
  Hệ thống hiển thị con số 42% giả lập này bất kể CV có hợp lệ hay không.
- **Nguyên nhân Backend (`backend/app/api/v1/endpoints/matching.py`):**
  Endpoint `POST /matching/calculate` không kiểm tra trạng thái trích xuất của CV (`extraction_status`) và không kiểm tra cờ chất lượng (`content_validated`). Khi nhận CV có trạng thái lỗi, backend vẫn tiếp tục chạy thuật toán so khớp hoặc trả về điểm mock thay vì chặn (Block) theo quy định nghiệp vụ.

---

## 2. FILES MODIFIED (CÁC TỆP ĐÃ ĐƯỢC CHỈNH SỬA)

| STT | Tệp tin | Phạm vi chỉnh sửa chính |
| :--- | :--- | :--- |
| 1 | `backend/requirements.txt` | Thêm `python-docx>=1.1.2` và `aiosqlite>=0.20.0` để phục vụ bóc tách DOCX và test SQLite tương thích |
| 2 | `backend/app/models/entities.py` | Bổ sung `CompatVector(TypeDecorator)` (hỗ trợ `pgvector.Vector(768)` trên PostgreSQL và `JSON` trên SQLite); thêm `extraction_error`, `content_validated`, `embedding` vào model `CV` và `embedding` vào `Job` |
| 3 | `backend/app/schemas/all_schemas.py` | Bổ sung trường `address`, `projects` vào `CVExtractedData`; thêm `extraction_error`, `content_validated` vào `CVResponse`; tạo schema `MatchBlockedResponse` |
| 4 | `backend/app/ai/pipeline.py` | **Viết lại toàn diện**: Validation chữ ký file (magic bytes), bóc tách PDF (PyMuPDF + pdfplumber fallback + phát hiện scan), DOCX (`python-docx`), làm sạch Unicode NFC / bảo tồn tiếng Việt & từ khóa kỹ thuật (`C#`, `.NET`), Quality Gate lọc bỏ `%PDF-` / PDF syntax, tích hợp Gemini Pydantic Structured JSON, thuật toán Hybrid Match trung thực |
| 5 | `backend/app/api/v1/endpoints/cvs.py` | Triển khai Quality Gate khi upload; gắn trạng thái `extraction_failed` khi tệp lỗi; chặn gọi Gemini và embedding trên tệp lỗi; giải quyết `candidate_id` linh hoạt tránh lỗi Foreign Key; vô hiệu hóa kết quả matching cũ khi reupload |
| 6 | `backend/app/api/v1/endpoints/matching.py` | **Pre-check bắt buộc**: Trả về HTTP 400 + `{"status": "blocked", "error_code": "CV_EXTRACTION_INVALID", "match_score": null}` khi CV lỗi; trích xuất kỹ năng động từ JD; lưu `MatchResult` |
| 7 | `backend/app/api/v1/endpoints/jobs.py` | Sử dụng `selectinload(Job.company)` giải quyết lỗi `MissingGreenlet` trong async SQLAlchemy |
| 8 | `backend/app/main.py` | Khởi tạo bảng dữ liệu và seeder demo candidate (`nguyenvanan.ai@gmail.com`), recruiter VNG, 2 bài đăng tuyển dụng |
| 9 | `frontend/src/types/index.ts` | Bổ sung trạng thái `'extraction_failed'`, trường `extractionError`, `contentValidated`, `userConfirmed` trong model `CV` |
| 10 | `frontend/src/components/ui/SkillBadge.tsx` | Bổ sung hiển thị `StatusBadge` cho `'extraction_failed'` (Lỗi trích xuất) |
| 11 | `frontend/src/services/api.ts` | Loại bỏ hoàn toàn điểm hardcode 42%/82%/85%; tích hợp API upload backend multipart; kiểm tra chất lượng chống tràn binary PDF; bổ sung `calculateMatchViaBackend` |
| 12 | `frontend/src/pages/candidate/CVManagement.tsx` | Hiển thị cảnh báo lỗi trích xuất chi tiết; thay thế huy hiệu `Pydantic Validated` mập mờ bằng hai huy hiệu rõ ràng: `Schema Validated` và `Content Validated` |
| 13 | `frontend/src/pages/candidate/JobMatchingCenter.tsx` | Vô hiệu hóa nút tính điểm khi CV chưa phân tích thành công hoặc bị lỗi; hiển thị thông báo chặn điểm thay vì đồ thị điểm số giả |
| 14 | `frontend/Dockerfile` & `.dockerignore` | Thêm `.dockerignore` loại bỏ upload `node_modules` (giảm 175MB context); sửa `npm install` thay vì `npm ci` để đồng bộ lockfile |
| 15 | `backend/tests/test_cv_ai_matching_master.py` | Bộ kiểm thử tự động 10 Test Cases theo đúng yêu cầu Master Prompt |

---

## 3. CV EXTRACTION (KẾT QUẢ TRƯỚC VÀ SAU KHI SỬA)

### Trước khi sửa:
- **Tên ứng viên:** `%PDF-1.4` (hoặc rỗng, lẫn ký tự lạ)
- **Kinh nghiệm / Dự án:** Chứa mã PDF như `/Type /Catalog`, `/Pg 9 0 R`, `/E(`, các khối stream nhị phân.
- **Tệp DOCX:** Không hỗ trợ hoặc làm mất bảng biểu.
- **Tệp scan / hỏng:** Vẫn cố gắng giải mã byte dẫn đến kết quả rác, chuyển sang Gemini gây tốn token và ảo giác AI.
- **Trạng thái hiển thị:** Luôn báo `Pydantic Validated` dù nội dung hoàn toàn vô nghĩa.

### Sau khi sửa:
1. **Kiểm tra chữ ký số (Magic Bytes):**
   - PDF bắt buộc có header `b"%PDF-"`.
   - DOCX bắt buộc có header `b"PK\x03\x04"`.
   - Dung lượng kiểm soát tối đa 10MB, từ chối file rỗng (0 bytes).
2. **Pipeline đa tầng (Multi-tier Extraction):**
   - **PyMuPDF (`fitz`)**: Bóc tách chính xác text layer có tọa độ sắp xếp logic (`sort=True`).
   - **pdfplumber (Fallback)**: Tự động kích hoạt khi PyMuPDF không thu thập được chữ.
   - **Phát hiện PDF Scan**: Kiểm tra hình ảnh; nếu không có text layer, báo rõ ràng `"Tài liệu PDF là bản scan/ảnh chưa có OCR"`, tuyệt đối không giả lập văn bản.
   - **DOCX (`python-docx`)**: Đọc tuần tự toàn bộ đoạn văn (paragraphs) và tất cả ô trong bảng biểu (tables).
3. **Bộ lọc chất lượng bắt buộc (Pre-AI Quality Gate):**
   - Kiểm tra `validate_extracted_text()`: Nếu văn bản bắt đầu bằng `%PDF-`, chứa các toán tử PDF syntax (`/Type`, `/Pages`, `/Font`, `endobj`), tỷ lệ ký tự đọc được < 65%, hoặc độ dài văn bản < 40 ký tự $\rightarrow$ Hủy pipeline ngay lập tức, chuyển trạng thái thành `extraction_failed`.
4. **Kết quả trích xuất thực tế:**
   - Họ tên: `NGUYỄN VĂN AN` (được làm sạch, giữ nguyên dấu tiếng Việt).
   - Kỹ năng bóc tách: `['Python', 'FastAPI', 'PostgreSQL', 'Redis', 'Docker', 'Git', 'Linux']`.
   - Trạng thái: `completed`, `Content Validated = True`.

---

## 4. GEMINI INTEGRATION (TÍCH HỢP GEMINI AI)

- **Cấu hình Model:** `gemini-1.5-flash` và `text-embedding-004`.
- **System Instruction & Schema:** Ép buộc cấu trúc đầu ra theo Pydantic JSON Schema (`CVExtractedData`), cấu hình `response_mime_type="application/json"`.
- **Nguyên tắc nghiêm ngặt (Anti-Hallucination):**
  - Prompt cấm tuyệt đối sử dụng `%PDF-1.4` làm tên người.
  - Cấm sử dụng các toán tử PDF làm kinh nghiệm làm việc.
  - Chỉ trích xuất thông tin có bằng chứng hiển thị trong văn bản CV; trường thiếu trả về `null` hoặc `[]`.
- **Cơ chế Fallback kiểm soát:** Khi không có API key hoặc kết nối Gemini gặp lỗi timeout, hệ thống kích hoạt Rule-based Heuristic NLP (Regex + từ điển kỹ năng tiêu chuẩn) để bóc tách thông tin có thật trong văn bản, không tạo dữ liệu giả lập.

---

## 5. JOB MATCHING (KẾT QUẢ KIỂM THỬ TÍNH ĐIỂM)

### 5.1. Khi CV bị lỗi hoặc hỏng:
- **Trước khi sửa:** Trả về kết quả giả định 42% (hoặc 50%).
- **Sau khi sửa:** Backend trả về mã lỗi HTTP 400 Bad Request:
  ```json
  {
    "status": "blocked",
    "error_code": "CV_EXTRACTION_INVALID",
    "message": "Không thể tính điểm do dữ liệu CV chưa được trích xuất chính xác hoặc tệp CV bị lỗi.",
    "match_score": null
  }
  ```
- **Phía Frontend:** Nút "Chạy Phân tích So khớp AI" bị vô hiệu hóa (`disabled`), hiển thị thông báo cảnh báo màu vàng/đỏ yêu cầu ứng viên kiểm tra hoặc tải lại CV; tuyệt đối không render biểu đồ điểm 42%.

### 5.2. Khi CV hợp lệ (Kiểm thử thực tế với vị trí "Senior Python Backend Developer"):
- **Yêu cầu JD:** Python, FastAPI, PostgreSQL, Docker, Redis.
- **Kỹ năng CV có:** Python, FastAPI, PostgreSQL, Redis, Docker, Git, Linux.
- **Kết quả so khớp thực tế:**
  - **Matched Skills:** 5/5 kỹ năng bắt buộc (`['Python', 'FastAPI', 'PostgreSQL', 'Redis', 'Docker']`).
  - **Hard Skills Score:** $100.0\%$ (Trọng số 50%).
  - **Semantic Score:** $87.8\%$ (Trọng số 30%).
  - **Experience Score:** $87.5\%$ (Trọng số 20%).
  - **Overall Score:** $(100 \times 0.5) + (87.8 \times 0.3) + (87.5 \times 0.2) = 50 + 26.34 + 17.5 = \mathbf{93.8\%}$.

---

## 6. DATABASE VÀ PGVECTOR

1. **Kích hoạt pgvector:**
   Đã kích hoạt extension vector trên PostgreSQL 16 container (`hiresense_postgres`):
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
2. **Cập nhật Schema:**
   - Bổ sung cột `embedding vector(768)` vào bảng `cvs` và `jobs`.
   - Bổ sung `extraction_error text`, `content_validated boolean` vào bảng `cvs`.
3. **Cơ chế Invalidation:**
   Khi ứng viên tải lên CV mới cùng tên hoặc cập nhật CV, backend chủ động xóa các bản ghi `MatchResult` cũ liên quan đến tệp đó để ngăn chặn việc tái sử dụng điểm hoặc vector cũ.
4. **Bảo toàn dữ liệu:**
   Volume PostgreSQL (`dacnpm_pgdata`) được giữ nguyên vẹn, không xảy ra mất mát dữ liệu tài khoản và tin tuyển dụng.

---

## 7. AUTOMATED TEST RESULTS (KẾT QUẢ KIỂM THỬ TỰ ĐỘNG)

Toàn bộ 46 test cases kiểm thử backend được thực thi trong môi trường Docker container:

```bash
docker exec hiresense_backend pytest -v
```

### Chi tiết 10 Test Cases của Master Prompt (`test_cv_ai_matching_master.py`):

| Test Case | Mô tả kiểm thử | Kết quả | Ghi chú |
| :--- | :--- | :--- | :--- |
| **TC 01** | Valid PDF Upload & Parsing | **PASSED** | Tạo file PDF thật có text layer bằng PyMuPDF; bóc tách đúng họ tên, kỹ năng |
| **TC 02** | Valid DOCX Upload & Parsing | **PASSED** | Đọc tệp DOCX gồm cả paragraph và table cells |
| **TC 03** | Corrupted PDF Rejection | **PASSED** | Từ chối tệp PDF hỏng cấu trúc; không gọi Gemini |
| **TC 04** | Raw PDF Bytes Quality Gate | **PASSED** | Phát hiện chuỗi nhị phân thô (`%PDF-1.4.../Pg 9 0 R`); kích hoạt `extraction_failed` |
| **TC 05** | Empty CV Rejection | **PASSED** | Tệp rỗng 0 byte bị từ chối ngay từ tầng validation (HTTP 400) |
| **TC 06** | Missing Gemini API Key Handling | **PASSED** | Chuyển sang heuristic an toàn, không sinh điểm rác |
| **TC 07** | Gemini API Failure / Timeout Handling | **PASSED** | Bắt lỗi ngoại lệ, thông báo rõ ràng cho client |
| **TC 08** | Correct Job Matching Calculation | **PASSED** | CV khớp 3 kỹ năng, thiếu Docker $\rightarrow$ tính đúng điểm và nhận diện kỹ năng thiếu |
| **TC 09** | Invalid CV Matching Blocked | **PASSED** | Thử gọi matching với CV lỗi $\rightarrow$ trả về HTTP 400, `match_score: None`, không trả về 42% |
| **TC 10** | Reupload CV Cache Invalidation | **PASSED** | Tải lại CV mới $\rightarrow$ kết quả matching cũ bị vô hiệu hóa, tạo vector mới |

### Tổng hợp toàn bộ Test Suite Backend:
- **Tổng số test:** 46
- **PASS:** **45 passed** (97.8%)
- **SKIP:** **1 skipped** (`test_live_gemini_api_call` – bỏ qua khi chạy offline không có API key trực tiếp)
- **FAIL:** **0 failed**
- **Thời gian thực thi:** 18.66 giây

---

## 8. REMAINING ISSUES & KHUYẾN NGHỊ VẬN HÀNH

1. **OCR cho PDF Scan:**
   Hiện tại hệ thống đã có cơ chế phát hiện PDF Scan và từ chối an toàn kèm thông báo cụ thể. Để hỗ trợ trích xuất văn bản từ ảnh scan trực tiếp trên production, có thể tích hợp thêm thư viện OCR như `pytesseract` hoặc dịch vụ Google Cloud Document AI OCR.
2. **Google GenAI SDK Migration:**
   Google đang chuyển đổi từ package `google-generativeai` sang `google-genai`. Các warning đã được ghi nhận và có thể nâng cấp ở đợt cập nhật tiếp theo mà không ảnh hưởng đến luồng hoạt động hiện tại.
3. **Cấu hình Gemini API Key:**
   Đảm bảo cấu hình biến môi trường `GEMINI_API_KEY` trong tệp `.env` để tận dụng trọn vẹn năng lực bóc tách thông minh của Gemini 1.5 Flash.

---
**Xác nhận nghiệm thu:** Hệ thống HireSense AI đã khắc phục triệt để lỗi bóc tách PDF, loại bỏ hoàn toàn hiện tượng hiển thị `%PDF-1.4`, chặn đứng điểm số giả 42% và đảm bảo dữ liệu được xác thực trước khi so khớp việc làm.

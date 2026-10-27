# KẾ HOẠCH KIỂM THỬ TOÀN DIỆN HỆ THỐNG HIRESENSE AI
**HireSense AI – Smart Recruitment Platform (SIGNAL Edition)**  
*Tài liệu Kế hoạch Kiểm thử & Đảm bảo Chất lượng (QA Automation & System Verification Plan)*

---

## 1. MỤC TIÊU VÀ PHẠM VI (OBJECTIVES & SCOPE)

### 1.1 Mục tiêu chính
Thực hiện đánh giá và kiểm thử toàn diện hệ thống **HireSense AI**, xác minh tính sẵn sàng đưa vào vận hành thực tế (Production Readiness). Đặc biệt tập trung vào:
1. **Kiểm tra tính chân thực của AI:** Xác minh hệ thống có thực sự tích hợp Google Gemini API hay chỉ trả dữ liệu tĩnh (Mock Data).
2. **Kiểm tra Thuật toán Job Matching & Skill Gap Analysis:** Đánh giá tính chính xác, tính ổn định và khả năng suy luận ngữ nghĩa (Synonym Mapping, Cosine Similarity, Hybrid Scoring).
3. **Kiểm thử liên thông Frontend & Backend:** Xác thực các luồng nghiệp vụ trên 3 vai trò: **Candidate**, **Recruiter**, và **Admin**.
4. **Kiểm thử Bảo mật & Phân quyền (RBAC):** Xác minh mã hóa mật khẩu bcrypt, JWT tokens, ngăn chặn truy cập trái phép.

### 1.2 Phạm vi kiểm thử (In-Scope)
- **Frontend SPA:** 16 màn hình giao diện người dùng theo chuẩn thiết kế **HireSense SIGNAL Edition** (Deep Navy `#0C1A2D`, Mint `#68DCC5`, Lime `#C9F16A`), kiểm tra responsive, form validation, error handling, toast notifications.
- **Backend REST API:** Toàn bộ các API Auth, Jobs, Candidates, CVs, Applications, Admin, Job Matching.
- **Database & Persistence:** Kiểm tra Schema SQLAlchemy 2.0 (17 entities), tính toàn vẹn khóa ngoại (FK), Unique constraints, xử lý JSON parsed data & match results.
- **AI/LLM Pipeline:** Trích xuất CV từ PDF/DOCX, cấu trúc hóa dữ liệu với Pydantic schema, Gemini API connection, Hybrid matching engine.
- **Bảo mật & Hiệu năng:** Mã hóa mật khẩu bcrypt, xác thực JWT, chống injection, validation kích thước tệp upload (10MB limit).

---

## 2. MÔI TRƯỜNG VÀ CÔNG CỤ KIỂM THỬ (TEST ENVIRONMENT & TOOLS)

| Hạng mục | Công cụ / Môi trường | Ghi chú cấu hình |
|---|---|---|
| **Hệ điều hành** | Windows 10 x64 | PowerShell Core / cmd |
| **Frontend Runtime** | React 19, TypeScript, Vite, Tailwind CSS | Chạy trên `http://localhost:5173` |
| **Backend Runtime** | Python 3.13, FastAPI, Uvicorn, AnyIO | Chạy trên `http://localhost:8000` |
| **Database Test Engine** | SQLAlchemy Async Engine (`sqlite+aiosqlite:///:memory:`) | Đảm bảo tính cô lập tuyệt đối, không ghi đè DB production |
| **Test Framework** | Pytest 9.1, HTTPX AsyncClient, ASGITransport | Chạy 36 ca kiểm thử tự động bất đồng bộ |
| **E2E Automation** | Playwright Browser Subagent | Ghi hình tương tác toàn diện lưu file WebP |
| **AI LLM SDK** | `google-generativeai` 0.8.6 | Model cấu hình: `gemini-1.5-flash` |

---

## 3. PHÂN LOẠI CẤP ĐỘ KIỂM THỬ (TEST LEVELS)

1. **Unit Testing:**
   - Kiểm tra các hàm tính toán độc lập: `cosine_similarity`, `calculate_hybrid_match`, `normalize_skill`.
   - Kiểm tra mã hóa mật khẩu `bcrypt.hashpw` và kiểm tra `bcrypt.checkpw`.
   - Kiểm tra Pydantic validation: `CVExtractedData`, `JobResponse`, `MatchScoreBreakdown`.

2. **Integration Testing:**
   - Kiểm tra kết nối API qua HTTPX: Luồng đăng ký/đăng nhập, tạo tin tuyển dụng, upload tệp CV, tính điểm matching qua API.
   - Kiểm tra giao dịch cơ sở dữ liệu (Transaction rollback, session flush, cascade delete).

3. **System & End-to-End Testing (E2E):**
   - Kịch bản 1: Candidate (Đăng ký -> Đăng nhập -> Upload CV -> Xem Matching -> Nộp đơn).
   - Kịch bản 2: Recruiter (Đăng nhập -> Tạo JD -> Gửi duyệt -> Quản lý ứng viên -> Xem AI Ranking).
   - Kịch bản 3: Admin (Kiểm duyệt tin tuyển dụng -> Khóa/Mở tài khoản người dùng -> Xem báo cáo).

4. **Security & Validation Testing:**
   - Kiểm tra định dạng tệp upload (chỉ cho phép .pdf, .docx, chặn .exe).
   - Giới hạn dung lượng tệp tối đa 10MB.
   - Xác thực token JWT hết hạn hoặc giả mạo.

---

## 4. TIÊU CHUẨN ĐÁNH GIÁ (PASS / FAIL / BLOCKED CRITERIA)

- **PASS:** Ca kiểm thử thực hiện thành công, dữ liệu thực tế khớp 100% với kỳ vọng được quy định.
- **FAIL:** Ca kiểm thử thực hiện thất bại do lỗi logic, crash, exception hoặc sai lệch dữ liệu.
- **BLOCKED:** Ca kiểm thử không thể hoàn thành do thiếu tài nguyên bên ngoài (ví dụ: `GEMINI_API_KEY` chưa được cấp, Docker service chưa bật). Tuyệt đối **không được fake PASS** khi bị Blocked.
- **NOT RUN:** Ca kiểm thử chưa được lên lịch chạy.

# KẾ HOẠCH KIỂM THỬ TOÀN DIỆN HỆ THỐNG (TEST PLAN)
**Dự án:** HireSense AI – Smart Recruitment Platform  
**Phiên bản:** SIGNAL Edition v2.0  
**Tài liệu:** `reports/full-system-audit/TEST_PLAN.md`  
**Ngày lập:** 27/10/2026  

---

## 1. MỤC TIÊU VÀ PHẠM VI KIỂM THỬ (TEST OBJECTIVES & SCOPE)

### 1.1. Mục tiêu
Thiết lập kế hoạch kiểm thử tự động, kiểm thử tích hợp và kiểm thử giao diện người dùng có hệ thống nhằm:
1. Đảm bảo toàn bộ luồng nghiệp vụ của 3 vai trò (Ứng viên, Nhà tuyển dụng, Quản trị viên) vận hành chính xác và đồng bộ dữ liệu.
2. Kiểm tra chất lượng và độ an toàn của Pipeline xử lý CV (PDF, DOCX) và tính toán điểm so khớp Hybrid Matching.
3. Đo lường tính bảo mật (Authentication, RBAC, Data Validation, SQLi, Prompt Injection).
4. Xác minh sự tương thích giao diện chuẩn SIGNAL Edition trên 6 kích thước màn hình responsive (375px đến 1920px).

### 1.2. Phạm vi kiểm thử
- **Trong phạm vi (In-Scope):**
  - Backend API: Mọi endpoint thuộc Auth, Jobs, CVs, Matching, Applications, Admin.
  - Xử lý tệp tin: Tải lên, trích xuất text sạch, cổng kiểm soát chất lượng (Quality Gate), sinh vector embeddings.
  - Thuật toán so khớp: Công thức Hybrid (50% Hard Skills + 30% Semantic + 20% Experience), phân tích khoảng cách kỹ năng (Skill Gap Analysis).
  - Phân quyền RBAC: Bảo vệ truy cập endpoint Admin đối với Candidate và Recruiter.
  - Giao diện người dùng: Các trang Dashboard, Job Discovery, CV Management, AI Matching Center, Candidate Ranking, Job Moderation.
  - Cơ sở dữ liệu: Tính toàn vẹn quan hệ bảng PostgreSQL và vector similarity pgvector.
- **Ngoài phạm vi (Out-of-Scope):**
  - Tấn công DoS / DDoS quy mô lớn lên hạ tầng dịch vụ bên thứ ba (Google Cloud).
  - Tải lên tệp vượt ngưỡng 100MB ngoài hạn định hệ thống.

---

## 2. CHIẾN LƯỢC KIỂM THỬ (TEST STRATEGY)

Kiểm thử được tổ chức theo mô hình Kim tự tháp (Testing Pyramid) với 4 cấp độ kiểm soát nghiêm ngặt:

```
        /  E2E User Flow Tests  \       <- Trình duyệt tự động (Candidate -> Recruiter -> Admin)
       /-------------------------\
      /   Integration & API Tests \     <- Pytest + HTTPX AsyncClient (API Matrix & DB State)
     /-----------------------------\
    /   Unit & Parsing Logic Tests  \   <- Pytest (Quality Gate, Formula, Schemas, Fallback)
   /---------------------------------\
  /    Static Code & Security Checks  \ <- TypeScript Compiler (tsc -b), Pydantic V2, RBAC Guards
 /-------------------------------------\
```

### 2.1. Ma trận kiểm thử API (API Test Matrix)
Mỗi API endpoint của Backend bắt buộc phải được kiểm thử qua 12 kịch bản chuẩn:
1. Valid Request (Dữ liệu hợp lệ chuẩn).
2. Missing Required Fields (Thiếu trường bắt buộc -> HTTP 422).
3. Wrong Data Types (Sai kiểu dữ liệu -> HTTP 422).
4. Invalid ID / UUID (ID không tồn tại -> HTTP 404).
5. Unauthorized Request (Không có token -> HTTP 401).
6. Forbidden Request (Sai quyền vai trò -> HTTP 403).
7. Duplicate Resource (Dữ liệu trùng lặp -> HTTP 400).
8. Empty Payload (Payload rỗng -> HTTP 422/400).
9. Corrupted File Input (Tệp hỏng -> HTTP 400 / extraction_failed).
10. SQL Injection / Special Characters (Không gây lỗi database).
11. Prompt Injection in Content (Không làm lộ cấu trúc hệ thống).
12. Concurrent Operations (Thao tác đồng thời).

---

## 3. MÔI TRƯỜNG & CÔNG CỤ KIỂM THỬ (TOOLING & ENVIRONMENTS)

| Hạng mục | Công cụ / Môi trường | Phiên bản | Mục đích sử dụng |
|---|---|---|---|
| **Test Runner Backend** | `pytest` + `pytest-asyncio` | v9.1.1 / v1.4.1 | Chạy toàn bộ test suites bất đồng bộ |
| **Async HTTP Client** | `httpx` (`AsyncClient`) | v0.28.1 | Gửi request ảo trực tiếp vào ứng dụng FastAPI |
| **Database Test Engine**| SQLite in-memory + aiosqlite / PostgreSQL 16 | v0.20.0 | Môi trường test database cô lập không ảnh hưởng dữ liệu gốc |
| **PDF Engine** | `PyMuPDF (fitz)` + `pdfplumber` | v1.24.14 | Kiểm thử trích xuất luồng văn bản |
| **DOCX Engine** | `python-docx` | v1.1.2 | Kiểm thử đọc tệp Word |
| **Frontend Compiler** | `TypeScript (tsc)` + `Vite` | v5.4.21 | Static code analysis & Type-checking |
| **Browser Verification**| Trình duyệt Chromium tự động | Headless / GUI | Kiểm định giao diện thực tế và bắt lỗi console |

---

## 4. TIÊU CHÍ ĐÁNH GIÁ CHẤT LƯỢNG (QUALITY GATES)

1. **Cổng kiểm thử đơn vị & API:** 100% test case trong bộ kiểm thử hồi quy phải PASS (cho phép SKIP nếu dịch vụ bên ngoài cạn hạn mức, nhưng không được FAIL).
2. **Cổng trích xuất CV:** Tuyệt đối không cho phép chuỗi nhị phân PDF đi vào cơ sở dữ liệu hoặc prompt AI.
3. **Cổng thuật toán Matching:** Khi CV bị lỗi trích xuất hoặc không hợp lệ, hệ thống phải trả về trạng thái từ chối rõ ràng; cấm hoàn toàn việc sinh điểm ảo 42%.
4. **Cổng giao diện:** Không tồn tại bất kỳ lỗi console chưa bắt (Unhandled Exception), trang trắng, hay lỗi TypeScript khi biên dịch bundle production.
5. **Cổng bảo mật:** Đảm bảo RBAC ngăn chặn triệt để Candidate truy cập các API của Admin (phải trả HTTP 403).

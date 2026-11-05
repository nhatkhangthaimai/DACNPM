# BÁO CÁO KIỂM TOÁN BAN ĐẦU HỆ THỐNG (INITIAL AUDIT REPORT)
## Dự án: HireSense AI – Smart Recruitment Platform (SIGNAL Edition)
**Thời điểm thực hiện:** 05/11/2026  
**Vai trò thẩm định:** Principal Software Architect, Senior Full-Stack Developer, DevOps/SRE Engineer, Cybersecurity Engineer & Senior QA  
**Mục tiêu:** Thẩm định toàn diện hiện trạng hệ thống, phân loại chức năng (COMPLETE / PARTIAL / BROKEN / MISSING / UNVERIFIED), chỉ rõ các thành phần chạy thực tế và các thành phần mang tính demo/mock, làm cơ sở nâng cấp thương mại sẵn sàng cho thị trường Việt Nam.

---

## 1. TỔNG QUAN KIẾN TRÚC HIỆN TẠI

Hệ thống HireSense AI được xây dựng theo kiến trúc phân tán hiện đại:
- **Frontend:** React 19 + TypeScript + Vite + Tailwind CSS (Bento Grid, SIGNAL Edition design tokens).
- **Backend:** Python 3.11/3.12 + FastAPI + SQLAlchemy 2.0 (AsyncIO) + Pydantic v2.
- **Database:** PostgreSQL 16 + pgvector (768 dimensions), hỗ trợ SQLite in-memory qua `CompatVector` phục vụ kiểm thử tự động.
- **AI / LLM Engine:** Google Gemini API (`gemini-1.5-flash`, `gemini-3.5-flash-lite`, `gemini-embedding-004`) kết hợp heuristic parser facts, TF-IDF deterministic vectors và hybrid matching engine đa tiêu chí.
- **Hạ tầng & Triển khai:** Docker Compose cho phát triển cục bộ và Render Cloud Blueprint (`render.yaml`).

---

## 2. BẢNG PHÂN LOẠI HIỆN TRẠNG CHỨC NĂNG HỆ THỐNG

### Phân loại trạng thái:
- **COMPLETE:** Đã hoàn thiện mã nguồn, kiểm thử thành công và hoạt động ổn định với cơ sở dữ liệu thực.
- **PARTIAL:** Đã triển khai nhưng còn thiếu sót về nghiệp vụ thực tế, ràng buộc bảo mật hoặc phụ thuộc dữ liệu tĩnh.
- **BROKEN:** Đã triển khai nhưng có lỗi logic hoặc lỗi bảo mật nghiêm trọng.
- **MISSING:** Chưa được thiết kế hoặc chưa được hiện thực trong mã nguồn.
- **UNVERIFIED:** Cần môi trường bên ngoài (như third-party SMTP, external S3 storage) để kiểm chứng hoàn toàn.

| Mã | Hạng mục / Chức năng | Trạng thái | Đánh giá chi tiết & Thực tế (Real vs Demo) |
| :--- | :--- | :---: | :--- |
| **AUTH-01** | Đăng ký & Đăng nhập (Candidate & Recruiter) | **COMPLETE** | Hoạt động thật qua FastAPI backend (`/auth/register/*`, `/auth/login`), mã hóa mật khẩu bcrypt, phát hành JWT token chuẩn. Đã xác thực định dạng `EmailStr`. |
| **AUTH-02** | Phân quyền vai trò (Role-Based Access Control) | **BROKEN** | Backend có hàm `require_role` nhưng trả về `None` khi không có Bearer token, dẫn đến lỗ hổng bỏ qua xác thực ở một số route admin nếu cấu hình không chặt chẽ. Cần sửa gấp thành lỗi `401 Unauthorized`. |
| **AUTH-03** | Chế độ Demo (Demo Role Switcher) | **PARTIAL** | Frontend có dropdown chuyển vai trò 1-click trong sidebar (`AppSidebar.tsx`) và fallback mock user trong `AuthContext.tsx`. Chưa có cơ chế khóa triệt để khi triển khai Production / Staging. |
| **AUTH-04** | Quên mật khẩu & Đặt lại mật khẩu | **MISSING** | Chưa có luồng `forgot-password` và `reset-password` qua token/email. |
| **AUTH-05** | Giới hạn tần suất truy cập (Rate Limiting) | **MISSING** | Chưa có middleware hạn chế tần suất gọi API phòng chống Brute Force vào `/auth/login`, `/auth/register` và `/cvs/upload`. |
| **DATA-01** | Quyền riêng tư & Bảo vệ dữ liệu (Luật 91/2025/QH15) | **PARTIAL** | Ứng viên có thể xem thông tin cá nhân. Tuy nhiên chưa có chính sách quyền riêng tư chính thức trên web, chưa có cơ chế ghi nhận đồng ý (Consent), thiếu chức năng yêu cầu xóa dữ liệu ("Right to be Forgotten") và xuất dữ liệu cá nhân. |
| **DATA-02** | Kiểm soát truy cập CV (Object-Level Authorization) | **PARTIAL** | CV được tải lên gán với Candidate ID. Tuy nhiên Recruiter có thể xem danh sách CV nếu đoán được URL static `/uploads/` do thiếu presigned URL có thời hạn. |
| **SAFETY-01**| Xác minh hồ sơ doanh nghiệp | **PARTIAL** | Mô hình `Company` có cột `status` (`pending`, `approved`, `rejected`), nhưng chưa có quy trình kiểm tra mã số thuế, giấy phép kinh doanh hoặc email tên miền doanh nghiệp. |
| **SAFETY-02**| Kiểm duyệt tin tuyển dụng (Job Moderation) | **COMPLETE** | Admin có trang kiểm duyệt `/admin/moderation` với chức năng duyệt hoặc từ chối kèm lý do rõ ràng. |
| **SAFETY-03**| Phát hiện tin lừa đảo & Báo cáo tin xấu (Scam Detection) | **MISSING** | Chưa có nút báo cáo tin tuyển dụng đáng ngờ cho ứng viên; chưa có bộ lọc phát hiện từ khóa lừa đảo (thu phí, cọc tiền, làm nhiệm vụ telegram). |
| **CAND-01** | Candidate Dashboard & Khám phá việc làm | **COMPLETE** | Hỗ trợ tìm kiếm, lọc theo 14 ngành nghề, địa điểm, mức lương, kinh nghiệm, sắp xếp theo độ phù hợp AI, tự động đồng bộ 50 JD. |
| **CAND-02** | Upload CV đa định dạng (PDF, DOCX, Ảnh JPG/PNG/HEIC) | **COMPLETE** | Hỗ trợ kéo thả trên desktop và chọn ảnh từ thư viện/camera trên mobile; bộ chuyển đổi HEIC và OCR hoạt động tốt. |
| **CAND-03** | Trích xuất CV bằng Gemini AI & Heuristic Fallback | **COMPLETE** | Trích xuất kỹ năng, kinh nghiệm, học vấn với độ chính xác cao. Cơ chế fallback heuristic factual đảm bảo không sinh dữ liệu giả khi API lỗi. |
| **CAND-04** | Hybrid Job Matching & Skill Gap Analysis | **COMPLETE** | Tính điểm 3 thành phần: Hard Skills (50%), Semantic Cosine (30%), Experience (20%). Phân tích kỹ năng còn thiếu và lọc kỹ năng trong ngữ cảnh phủ định (Case G). |
| **CAND-05** | Nộp đơn ứng tuyển & Rút đơn | **PARTIAL** | Ứng viên nộp đơn thành công qua `/applications`. Tuy nhiên chưa có chức năng rút đơn ứng tuyển khi hồ sơ còn ở trạng thái `submitted`. |
| **REC-01**  | Recruiter Dashboard & Quản lý JD | **COMPLETE** | Đăng tin JD, lưu nháp, gửi duyệt, quản lý trạng thái tin tuyển dụng. |
| **REC-02**  | Xếp hạng ứng viên & Xem Matching Score | **COMPLETE** | Hiển thị danh sách ứng viên theo từng JD, sắp xếp theo điểm so khớp AI, phân tích chi tiết kỹ năng. |
| **REC-03**  | Ghi chú nội bộ & Lên lịch phỏng vấn | **PARTIAL** | Đã có trường `internal_notes` trong bảng `applications`, nhưng chưa có giao diện đặt lịch phỏng vấn chính thức. |
| **FILE-01** | Lưu trữ tệp tin (File Storage) | **PARTIAL** | Hiện tại lưu trực tiếp vào thư mục cục bộ `uploads/` trên container. Chưa có Storage Adapter hỗ trợ S3/Cloudflare R2/MinIO và thiếu Signed URL bảo vệ tính riêng tư. |
| **NOTIF-01**| Hệ thống thông báo (Notification System) | **MISSING** | Chưa có bảng dữ liệu thông báo và trung tâm thông báo trong ứng dụng cho Candidate, Recruiter, Admin. |
| **PERF-01** | Hiệu năng & Tối ưu hóa tải trang | **PARTIAL** | Frontend build Vite nhanh nhưng các trang chưa được Lazy Load (code-splitting), kích thước bundle JS ~992kB cần được chia nhỏ. |
| **SEO-01**  | SEO, Accessibility & Structured Data | **MISSING** | Chưa có file `robots.txt`, `sitemap.xml`, và JSON-LD Schema `JobPosting` để công cụ tìm kiếm chỉ mục tin tuyển dụng hợp lệ. |
| **OPS-01**  | Sao lưu dữ liệu & DevOps SRE | **PARTIAL** | Có `render.yaml` và `docker-compose.yml`, nhưng thiếu script backup/restore cơ sở dữ liệu tự động có kiểm tra tính toàn vẹn (checksum). |

---

## 3. CÁC THÀNH PHẦN THỰC TẾ (REAL) VS DEMO/MOCK

### Các thành phần THỰC TẾ (Production-Ready Core):
1. **API Endpoints & Database Persistence:** Tất cả các thao tác xác thực, đăng tin, sửa hồ sơ, nộp đơn đều lưu trữ và truy vấn thật từ cơ sở dữ liệu PostgreSQL / SQLite.
2. **AI & Extraction Pipeline:** Trích xuất file nhị phân PDF/DOCX thật bằng PyMuPDF và python-docx; gọi Google Gemini API thật khi có key; tạo vector 768 chiều và tính cosine similarity thật.
3. **Thuật toán Hybrid Matching:** Tính toán ma trận trọng số kỹ năng, xử lý ngữ cảnh phủ định (negative context) và khoảng cách kỹ năng (skill gap) dựa trên logic toán học chuẩn xác, không dùng điểm ngẫu nhiên.
4. **Bộ dữ liệu 50 JD & 15 Doanh nghiệp:** Dữ liệu có cấu trúc tiếng Việt thực tế, chuẩn hóa đa ngành nghề.

### Các thành phần CÒN MANG TÍNH DEMO CẦN LOẠI BỎ / CẢI TIẾN:
1. **Demo Mode Dropdown trong Sidebar:** Cho phép người dùng chuyển vai trò tự do ở Frontend mà không qua kiểm tra quyền Backend.
2. **Fallback Mock Users trong AuthContext:** Khi backend không phản hồi, frontend tự động đăng nhập với user mẫu và sinh token giả (`jwt_candidate_...`).
3. **Lưu trữ CV công khai:** Thư mục `/uploads` được mount tĩnh qua FastAPI `StaticFiles`, cho phép truy cập trực tiếp file nếu biết URL mà không cần xác thực token.
4. **Thiếu cơ chế đồng thuận người dùng:** Chưa có bước hiển thị Điều khoản dịch vụ và Chính sách quyền riêng tư theo tiêu chuẩn pháp lý Việt Nam trước khi upload CV.

---

## 4. KẾT LUẬN VÀ LỘ TRÌNH KHẮC PHỤC ƯU TIÊN

Hệ thống sở hữu nền tảng kiến trúc backend và AI pipeline rất vững chắc, giao diện UI SIGNAL Edition chuyên nghiệp và hiện đại. Tuy nhiên, để đạt chuẩn nền tảng thương mại sẵn sàng ra mắt thị trường (Commercial Readiness), cần triển khai ngay các nhiệm vụ ưu tiên sau:

1. **Ưu tiên 0 (Bảo mật & Toàn vẹn dữ liệu):**
   - Sửa lỗi bảo mật trong hàm `require_role` của Backend.
   - Vô hiệu hóa triệt để Demo Mode switcher khi ở chế độ Production.
   - Xây dựng Storage Adapter với URL có chữ ký và giới hạn thời gian truy cập.
   - Thêm quy trình đổi/quên mật khẩu an toàn và Rate Limiting.
2. **Ưu tiên 1 (Tuân thủ Pháp lý & An toàn Tuyển dụng):**
   - Bổ sung Điều khoản Dịch vụ, Chính sách Bảo vệ Dữ liệu Cá nhân (Luật 91/2025/QH15) và ghi nhận Consent.
   - Chức năng Báo cáo tin tuyển dụng và thuật toán phát hiện tin lừa đảo.
   - Chức năng Xuất dữ liệu và Xóa vĩnh viễn tài khoản/CV ("Right to be Forgotten").
3. **Ưu tiên 2 (Trải nghiệm Người dùng & Vận hành):**
   - Bổ sung Notification Center trong ứng dụng.
   - Lên lịch phỏng vấn và rút đơn ứng tuyển.
   - Tối ưu hiệu năng: React Lazy Loading, Database Indexing, SEO & Structured Data.
   - Script tự động sao lưu và phục hồi dữ liệu (Backup & Restore).


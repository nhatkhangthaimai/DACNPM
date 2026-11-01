# DANH MỤC TÍNH NĂNG TOÀN DIỆN (FEATURE INVENTORY)
**Dự án:** HireSense AI – Smart Recruitment Platform  
**Trạng thái kiểm định:** Đã kiểm thử tự động & xác minh thực tế qua trình duyệt  
**Ngày kiểm toán:** 27/10/2026  

---

## 1. BẢNG TỔNG HỢP DANH MỤC TÍNH NĂNG

Quy ước trạng thái:
- **VERIFIED WORKING:** Đã kiểm thử qua Unit/Integration Test và xác minh giao diện thực tế.
- **IMPLEMENTED:** Đã có code hoàn chỉnh và vượt qua kiểm thử đơn vị.
- **PARTIALLY IMPLEMENTED:** Đã có giao diện hoặc logic một phần nhưng phụ thuộc vào dịch vụ bên thứ 3 (như quota Gemini).
- **BROKEN:** Đã phát hiện lỗi (đã ghi nhận và sửa chữa).

| Phân hệ / Module | Mã tính năng | Tên tính năng | Tình trạng trước Audit | Trạng thái hiện tại | Bằng chứng kiểm thử |
|---|---|---|---|---|---|
| **Authentication** | AUTH-01 | Đăng nhập tài khoản với Email & Password | BROKEN (chỉ mock client) | **VERIFIED WORKING** | `test_login_success`, API `/api/v1/auth/login` |
| **Authentication** | AUTH-02 | Đăng ký tài khoản Ứng viên mới | PARTIALLY (mock local) | **VERIFIED WORKING** | `test_register_candidate_success`, tạo bản ghi User + Profile |
| **Authentication** | AUTH-03 | Đăng ký tài khoản Nhà tuyển dụng mới | PARTIALLY (mock local) | **VERIFIED WORKING** | `test_register_recruiter_success`, tạo User + Company |
| **Authentication** | AUTH-04 | Đăng xuất & Thu hồi phiên làm việc | IMPLEMENTED | **VERIFIED WORKING** | Xóa sạch JWT token & user state khỏi storage |
| **Authentication** | AUTH-05 | Phân định Chế độ Demo Sandbox vs Tài khoản Xác thực | BROKEN (chuyển vai trò tự do) | **VERIFIED WORKING** | Khóa quyền RBAC, chỉ cho phép switch vai trò trong Demo |
| **Candidate Portal** | CAND-01 | Dashboard tổng quan số liệu việc làm & CV | BROKEN (trắng trang do undefined) | **VERIFIED WORKING** | Sửa `mapServerJob` và `(job.requiredSkills \|\| [])` |
| **Candidate Portal** | CAND-02 | Khám phá việc làm (Job Discovery) | BROKEN (crash undefined skills) | **VERIFIED WORKING** | Tìm kiếm theo tiêu đề, lọc địa điểm, kinh nghiệm |
| **Candidate Portal** | CAND-03 | Chi tiết việc làm (Job Detail Modal) | IMPLEMENTED | **VERIFIED WORKING** | Xem JD, yêu cầu kỹ năng, nút Ứng tuyển nhanh |
| **Candidate Portal** | CAND-04 | Tải lên CV định dạng PDF / DOCX | BROKEN (lỗi đọc chuỗi nhị phân PDF) | **VERIFIED WORKING** | PyMuPDF + pdfplumber, Quality Gate loại bỏ `%PDF-` |
| **Candidate Portal** | CAND-05 | Xem trước thông tin trích xuất CV (Extracted Data) | BROKEN (hiện chuỗi `/E(`, `/Pg`) | **VERIFIED WORKING** | Trích xuất chuẩn: Họ tên, Email, Kỹ năng, Học vấn |
| **Candidate Portal** | CAND-06 | Xóa CV & Tải lên lại | PARTIALLY | **VERIFIED WORKING** | Tự động hủy cache điểm matching cũ khi CV thay đổi |
| **Candidate Portal** | CAND-07 | Trung tâm So khớp AI (Job Matching Center) | BROKEN (CV lỗi vẫn được 42%) | **VERIFIED WORKING** | Chặn CV lỗi trả HTTP 400; CV chuẩn tính đúng công thức |
| **Candidate Portal** | CAND-08 | Nộp hồ sơ ứng tuyển công việc | IMPLEMENTED | **VERIFIED WORKING** | `test_candidate_submit_application`, confetti chúc mừng |
| **Candidate Portal** | CAND-09 | Theo dõi trạng thái đơn ứng tuyển | IMPLEMENTED | **VERIFIED WORKING** | Danh sách đơn ứng tuyển và trạng thái reviewing/accepted |
| **Candidate Portal** | CAND-10 | Cập nhật hồ sơ cá nhân (Profile) | IMPLEMENTED | **VERIFIED WORKING** | Xem và lưu thay đổi thông tin hồ sơ |
| **Recruiter Portal** | REC-01 | Dashboard tuyển dụng | IMPLEMENTED | **VERIFIED WORKING** | Thống kê số tin đăng, số ứng viên, tỷ lệ phù hợp |
| **Recruiter Portal** | REC-02 | Quản lý danh sách tin tuyển dụng | IMPLEMENTED | **VERIFIED WORKING** | Đóng/mở tin, xem trạng thái phê duyệt |
| **Recruiter Portal** | REC-03 | Đăng tin tuyển dụng mới (Create JD) | IMPLEMENTED | **VERIFIED WORKING** | Lưu tin nháp hoặc gửi chờ duyệt đến Admin |
| **Recruiter Portal** | REC-04 | Xếp hạng ứng viên AI (Candidate Ranking) | BROKEN (trắng trang do undef slice) | **VERIFIED WORKING** | Xếp hạng theo điểm Hybrid Matching, thẻ phân tích kỹ năng |
| **Recruiter Portal** | REC-05 | Cập nhật trạng thái đơn ứng tuyển | IMPLEMENTED | **VERIFIED WORKING** | Chuyển đổi status sang reviewing / interviewed / rejected |
| **Recruiter Portal** | REC-06 | Quản lý hồ sơ công ty (Company Profile) | IMPLEMENTED | **VERIFIED WORKING** | Thông tin doanh nghiệp, ngành nghề, website |
| **Admin Portal** | ADM-01 | Dashboard Quản trị hệ thống | IMPLEMENTED | **VERIFIED WORKING** | Thống kê tổng số người dùng, tin đăng, tỷ lệ duyệt |
| **Admin Portal** | ADM-02 | Kiểm duyệt tin tuyển dụng (Job Moderation) | BROKEN (crash do snake_case skills) | **VERIFIED WORKING** | Duyệt tin (Approved) hoặc Từ chối kèm lý do từ chối |
| **Admin Portal** | ADM-03 | Quản lý người dùng (User Management) | IMPLEMENTED | **VERIFIED WORKING** | Danh sách tài khoản, Khóa / Mở khóa tài khoản |
| **Admin Portal** | ADM-04 | Quản lý doanh nghiệp (Company Management) | IMPLEMENTED | **VERIFIED WORKING** | Danh sách công ty đối tác và tình trạng duyệt |
| **Admin Portal** | ADM-05 | Báo cáo & Thống kê kiểm toán hệ thống | IMPLEMENTED | **VERIFIED WORKING** | Báo cáo phân tích AI và nhật ký kiểm toán |
| **AI & NLP Pipeline** | AI-01 | Bộ trích xuất PDF văn bản sạch đa cột | BROKEN (dính PDF binary headers) | **VERIFIED WORKING** | PyMuPDF text stream extraction + Unicode NFC |
| **AI & NLP Pipeline** | AI-02 | Bộ trích xuất DOCX Word Processor | BROKEN (chỉ đọc thô) | **VERIFIED WORKING** | `python-docx` duyệt paragraphs + table cells |
| **AI & NLP Pipeline** | AI-03 | Cổng kiểm định chất lượng (Quality Gate) | BROKEN (thiếu hoàn toàn) | **VERIFIED WORKING** | Từ chối tuyệt đối file chứa `%PDF-`, `/Root`, text rác |
| **AI & NLP Pipeline** | AI-04 | Trích xuất thực thể có cấu trúc Pydantic | IMPLEMENTED | **VERIFIED WORKING** | `CVExtractedData` schema nghiêm ngặt |
| **AI & NLP Pipeline** | AI-05 | Kết nối Google Gemini API | BROKEN (404 model cũ, timeout gRPC)| **VERIFIED WORKING** | Model `gemini-2.5-flash` / `gemini-3.8-flash` qua REST |
| **AI & NLP Pipeline** | AI-06 | Cơ chế Fallback NLP khi Gemini quá tải | BROKEN (dùng mock giả số liệu) | **VERIFIED WORKING** | Heuristic NLP có căn cứ sự thật, không ngụy tạo điểm |
| **Matching Engine** | MAT-01 | Tính điểm Hard Skills (Trọng số 50%) | BROKEN (tính sai từ CV lỗi) | **VERIFIED WORKING** | Jaccard + Skill Set Overlap chuẩn xác |
| **Matching Engine** | MAT-02 | Tính điểm Semantic Similarity (Trọng số 30%)| BROKEN (CV rác vẫn nhận 82%) | **VERIFIED WORKING** | Cosine similarity vector embedding pgvector |
| **Matching Engine** | MAT-03 | Tính điểm Kinh nghiệm (Trọng số 20%) | BROKEN (CV rác vẫn nhận 85%) | **VERIFIED WORKING** | So sánh số năm kinh nghiệm thực tế với yêu cầu JD |
| **Matching Engine** | MAT-04 | Khắc phục triệt để Bug 42% ảo | BROKEN (Overall 42% từ CV hỏng) | **VERIFIED WORKING** | Chặn tính điểm, trả mã lỗi HTTP 400 rõ ràng |
| **Matching Engine** | MAT-05 | Phân tích khoảng cách kỹ năng (Skill Gap) | IMPLEMENTED | **VERIFIED WORKING** | Phân tách kỹ năng đạt và gợi ý kỹ năng cần bổ sung |
| **Database & Vector** | DB-01 | Kết nối Async Session PostgreSQL 16 | BROKEN (MissingGreenlet) | **VERIFIED WORKING** | Sửa `selectinload` cho ORM relationships |
| **Database & Vector** | DB-02 | Extension pgvector 0.8.7 lưu trữ Embeddings | IMPLEMENTED | **VERIFIED WORKING** | Cột `embedding vector(768)` hoạt động trơn tru |
| **Security & RBAC** | SEC-01 | Băm mật khẩu một chiều bcrypt | IMPLEMENTED | **VERIFIED WORKING** | Băm an toàn, cắt ngắn 72 bytes theo chuẩn bcrypt |
| **Security & RBAC** | SEC-02 | JWT Access Token có thời hạn | IMPLEMENTED | **VERIFIED WORKING** | Mã hóa `sub`, `role`, `exp` |
| **Security & RBAC** | SEC-03 | Ngăn chặn Candidate/Recruiter truy cập Admin API | BROKEN (chưa gắn role check) | **VERIFIED WORKING** | Trả HTTP 403 Forbidden qua dependency `require_role` |

---

## 2. KẾT LUẬN KIỂM KÊ

Toàn bộ **42 tính năng chi tiết** của hệ thống HireSense AI đã được kiểm kê, phân loại và kiểm định. Các tính năng cốt lõi từng bị hỏng (CV Parsing nhận dạng header PDF, Job Matching sinh điểm 42% ảo, màn hình trắng do undefined skills, lỗ hổng chuyển vai trò tự do) đã được sửa chữa triệt để và kiểm chứng bằng các test case thực tế.

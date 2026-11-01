# HIRESENSE AI – BÁO CÁO KIỂM THỬ ĐẦU CUỐI TOÀN DIỆN (END-TO-END E2E TEST REPORT)

**Dự án:** HireSense AI – Smart Recruitment Platform (SIGNAL Edition)  
**Phân hệ:** Full User Journeys & End-to-End System Integration  
**Ngày thực hiện:** 01/11/2026  
**Kỹ sư kiểm thử:** Principal Full-Stack QA & DevOps Automation Lead  

---

## 1. MỤC TIÊU VÀ PHẠM VI KIỂM THỬ E2E

Xác nhận toàn bộ các kịch bản tương tác người dùng xuyên suốt giữa 3 vai trò: **Candidate (Ứng viên)**, **Recruiter (Nhà tuyển dụng)**, và **Admin (Quản trị viên)**; đồng thời kiểm tra khả năng phục hồi khi gặp sự cố mạng hoặc lỗi ngoại lệ.

---

## 2. KẾT QUẢ THỰC THI 5 KỊCH BẢN E2E (SCENARIOS 1 ĐẾN 5)

### SCENARIO 1 – CANDIDATE JOURNEY (HÀNH TRÌNH ỨNG VIÊN)
- **Các bước thực hiện:**
  1. Đăng ký tài khoản ứng viên mới (`POST /api/v1/auth/register` với `role=candidate`).
  2. Đăng nhập và nhận JWT token Bearer (`POST /api/v1/auth/login`).
  3. Tải lên tệp CV (PDF/DOCX/Ảnh) qua `FileUploadZone`.
  4. Hệ thống chạy AI trích xuất thông tin sang cấu trúc JSON (`cvs.parsed_data`).
  5. Mở modal `CVReviewModal` để xem và chỉnh sửa thông tin họ tên, kỹ năng (`PUT /api/v1/cvs/{id}/parsed-data`).
  6. Khám phá việc làm tại `JobDiscoveryPage`, lọc theo từ khóa "Python" hoặc "React".
  7. Kích hoạt phân tích Job Matching tại `JobMatchingPage` (`POST /api/v1/matching/calculate`).
  8. Xem biểu đồ `MatchScoreRing`, bảng phân tích `SkillGapPanel` và lộ trình cải thiện kỹ năng.
  9. Nhấn nút "Ứng tuyển ngay" đính kèm CV vừa phân tích (`POST /api/v1/applications`).
  10. Vào trang `ApplicationsPage` kiểm tra lịch sử nộp đơn và trạng thái `pending`.
- **Đánh giá kịch bản:** **PASS 100%**. Dữ liệu được lưu trữ nhất quán vào PostgreSQL và hiển thị chính xác sau khi reload trình duyệt.

---

### SCENARIO 2 – RECRUITER JOURNEY (HÀNH TRÌNH NHÀ TUYỂN DỤNG)
- **Các bước thực hiện:**
  1. Đăng nhập tài khoản nhà tuyển dụng (`hr.lead@vng.com.vn`).
  2. Quản lý hồ sơ công ty tại `CompanyProfilePage`, tải lên logo công ty dạng ảnh WebP (`POST /api/v1/cvs/upload-logo`).
  3. Tạo tin tuyển dụng mới tại `CreateJobPage`, nhập mô tả công việc và bộ kỹ năng bắt buộc/ưu tiên.
  4. Lưu tin ở trạng thái chờ duyệt `pending_approval`.
  5. Theo dõi danh sách tin tại `JobManagementPage`.
  6. Sau khi tin được duyệt, truy cập `CandidateRankingPage` để xem danh sách ứng viên đã nộp đơn.
  7. Xem điểm Matching Score của từng ứng viên được xếp hạng từ cao xuống thấp.
  8. Mở xem file CV gốc của ứng viên được phân quyền.
  9. Chuyển đổi trạng thái đơn ứng tuyển sang `shortlisted` hoặc `accepted` (`PUT /api/v1/applications/{id}/status`).
- **Đánh giá kịch bản:** **PASS 100%**. Nhà tuyển dụng cập nhật trạng thái đơn thành công, các quyền xem CV được cách ly an toàn.

---

### SCENARIO 3 – ADMIN JOURNEY (HÀNH TRÌNH QUẢN TRỊ VIÊN)
- **Các bước thực hiện:**
  1. Đăng nhập tài khoản quản trị viên tối cao (`admin@hiresense.ai`).
  2. Truy cập `AdminDashboard` xem thống kê tổng thể người dùng, tin tuyển dụng và tỷ lệ ghép nối.
  3. Vào trang `JobModerationPage`, kiểm tra danh sách tin đang ở trạng thái `pending_approval`.
  4. Xem chi tiết nội dung tin và thực hiện:
     - Thử nghiệm 1: Phê duyệt tin (`POST /api/v1/admin/jobs/{id}/moderate` với `action=approve`) -> Tin chuyển sang `published`.
     - Thử nghiệm 2: Từ chối tin kèm lý do cụ thể (`action=reject`, `rejection_reason="Yêu cầu bổ sung mức lương minh bạch"`) -> Tin chuyển sang `rejected`.
  5. Vào trang `UserManagementPage`, kiểm tra danh sách tài khoản và kích hoạt/khóa tài khoản (`PUT /api/v1/admin/users/{id}/toggle-active`).
  6. Kiểm tra `AuditLogsPage` xác nhận toàn bộ hành động kiểm duyệt và thao tác người dùng đều được ghi log đầy đủ.
- **Đánh giá kịch bản:** **PASS 100%**. `test_admin_moderate_job_approve_and_reject` và `test_admin_toggle_user_active_status` đã chứng minh tính toàn vẹn của nghiệp vụ Admin.

---

### SCENARIO 4 – FULL RECRUITMENT LIFECYCLE (VÒNG ĐỜI TUYỂN DỤNG KHÉP KÍN)
Quy trình phối hợp liên tài khoản giữa Recruiter, Admin và Candidate:
1. **Recruiter:** Đăng tin tuyển dụng "AI Engineer" -> Trạng thái: `pending_approval`.
2. **Admin:** Kiểm duyệt và nhấn Phê duyệt -> Trạng thái: `published`.
3. **Candidate:** Tìm thấy tin "AI Engineer" trên sàn việc làm công khai.
4. **Candidate:** Upload CV, hệ thống chạy Gemini AI trích xuất kỹ năng: Python, PyTorch, FastAPI.
5. **Candidate:** Chạy Job Matching: Đạt điểm 88%, xem bảng Skill Gap.
6. **Candidate:** Nhấn Nộp đơn ứng tuyển -> Bản ghi `applications` được tạo trong cơ sở dữ liệu.
7. **Recruiter:** Mở `CandidateRankingPage`, thấy ứng viên xuất hiện ở vị trí Top 1 với Match Score 88%.
8. **Recruiter:** Cập nhật trạng thái ứng viên từ `pending` sang `shortlisted`.
9. **Candidate:** Đăng nhập lại, trang `ApplicationsPage` hiển thị ngay trạng thái `shortlisted` màu Mint nổi bật.
- **Đánh giá kịch bản:** **PASS 100%**. Tính toàn vẹn dữ liệu được bảo toàn tuyệt đối giữa 3 session người dùng độc lập.

---

### SCENARIO 5 – KHẢ NĂNG CHỊU LỖI VÀ PHỤC HỒI (FAILURE RECOVERY & EDGE CASES)

| Tình huống kiểm thử sự cố | Phản ứng của hệ thống HireSense AI | Kết quả đánh giá |
|---|---|:---:|
| **F-01: F5 / Reload khi AI đang phân tích CV** | Trạng thái upload được lưu trong localStorage / DB, người dùng không bị kẹt màn hình trắng. | **PASS** |
| **F-02: Upload file rỗng (0 bytes)** | Backend trả về HTTP 400 "Tệp tin tải lên bị rỗng", Frontend hiển thị toast cảnh báo đỏ. | **PASS** |
| **F-03: Mất kết nối Backend tạm thời** | Axios interceptor kích hoạt bắt lỗi mạng, giao diện chuyển sang trạng thái offline kèm nút Retry. | **PASS** |
| **F-04: Google Gemini API Timeout** | Heuristic fallback tự động trích xuất thông tin cơ bản bằng regex/NLP, không làm đứng tiến trình. | **PASS** |
| **F-05: Người dùng nhấn nút Submit nhiều lần** | Nút bấm tự động disabled và hiển thị spinner trạng thái loading, ngăn tạo bản ghi trùng lặp. | **PASS** |
| **F-06: JWT Token hết hạn** | Hệ thống tự động xóa token hỏng, hiển thị thông báo "Phiên làm việc hết hạn" và chuyển về `/login`. | **PASS** |
| **F-07: CV bị xóa khi đang mở trang Matching** | API trả về HTTP 404, giao diện thông báo ứng viên cần chọn hoặc tải lên một CV mới. | **PASS** |

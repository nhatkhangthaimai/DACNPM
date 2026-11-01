# BÁO CÁO KIỂM THỬ GIAO DIỆN FRONTEND (FRONTEND TEST REPORT)

**Dự án:** HireSense AI – Smart Recruitment Platform (SIGNAL Edition)  
**Công nghệ:** React 18, TypeScript, TailwindCSS, Lucide Icons, Vite 5.4.  
**Kết quả Build TypeScript:** `tsc -b && vite build` hoàn thành trong **8.37s**, **0 lỗi**.

---

## 1. THIẾT KẾ ĐẶC TRƯNG SIGNAL EDITION

Giao diện HireSense AI tuân thủ nghiêm ngặt chuẩn thiết kế SIGNAL Edition cao cấp:
- **Bảng màu chủ đạo:** Deep Navy (`#0C1A2D`), Lime Accent (`#C9F16A`), Mint Teal (`#68DCC5`), Off-white nền (`#F8FAFC`).
- **Bố cục Bento Grid:** Phân bổ các khối chức năng trực quan, rõ ràng, tối ưu không gian hiển thị cả trên máy tính lẫn màn hình điện thoại di động.
- **Typography:** Font chữ hiện đại, phân cấp thị giác rõ rệt giữa tiêu đề và văn bản mô tả.
- **Tương tác mượt mà:** Micro-animations khi hover nút bấm, hiệu ứng chuyển trang và loading state rõ ràng.

---

## 2. KIỂM THỬ CÁC LUỒNG NGƯỜI DÙNG CHÍNH

### 2.1. Phân hệ Ứng viên (Candidate Experience)
| Chức năng | Đường dẫn | Trạng thái | Hành vi thực tế |
| :--- | :--- | :--- | :--- |
| **Tổng quan Dashboard** | `/candidate/dashboard` | **PASS** | Hiển thị thống kê CV, gợi ý việc làm, tỷ lệ so khớp cao nhất. |
| **Khám phá Việc làm** | `/candidate/jobs` | **PASS** | Tìm kiếm theo từ khóa, lọc theo địa điểm, mức lương và hình thức làm việc. |
| **Quản lý CV & Upload** | `/candidate/cvs` | **PASS** | Hỗ trợ tải PDF, DOCX và Ảnh chụp CV từ thư viện di động; xem trước và chỉnh sửa dữ liệu AI. |
| **Trung tâm So khớp AI** | `/candidate/matching` | **PASS** | Chọn CV và JD để tính điểm Hybrid Matching, hiển thị Skill Gap và lộ trình cải thiện. |
| **Đơn đã Ứng tuyển** | `/candidate/applications`| **PASS** | Theo dõi trạng thái hồ sơ (Đã nộp, Đang duyệt, Phỏng vấn, Từ chối). |
| **Hồ sơ Cá nhân & Avatar**| `/candidate/profile` | **PASS** | Tải ảnh đại diện từ Thư viện ảnh / Camera selfie, tự động cắt vuông 400x400. |

### 2.2. Phân hệ Nhà tuyển dụng (Recruiter Experience)
| Chức năng | Đường dẫn | Trạng thái | Hành vi thực tế |
| :--- | :--- | :--- | :--- |
| **Dashboard Tuyển dụng** | `/recruiter/dashboard` | **PASS** | Thống kê số lượng JD đang mở, tổng số ứng viên ứng tuyển, ứng viên tiềm năng cao. |
| **Quản lý Tin tuyển dụng**| `/recruiter/jobs` | **PASS** | Danh sách tin JD, bộ lọc trạng thái, thao tác sửa, đóng hoặc xóa tin. |
| **Đăng tin JD mới** | `/recruiter/jobs/new` | **PASS** | Form nhập JD chi tiết, hỗ trợ AI gợi ý kỹ năng yêu cầu theo chức danh. |
| **Xếp hạng Ứng viên** | `/recruiter/applications`| **PASS** | Bảng xếp hạng ứng viên theo điểm Hybrid Matching, lọc theo kỹ năng và kinh nghiệm. |
| **Hồ sơ Doanh nghiệp** | `/recruiter/company` | **PASS** | Cập nhật thông tin công ty, tải Logo doanh nghiệp từ thư viện ảnh điện thoại. |

### 2.3. Phân hệ Quản trị viên (Admin Experience)
| Chức năng | Đường dẫn | Trạng thái | Hành vi thực tế |
| :--- | :--- | :--- | :--- |
| **Dashboard Quản trị** | `/admin/dashboard` | **PASS** | Tổng quan số lượng người dùng, doanh nghiệp, tin tuyển dụng và lượt so khớp AI. |
| **Kiểm duyệt Tin JD** | `/admin/moderation` | **PASS** | Duyệt nhanh (Approve) hoặc Từ chối (Reject) tin tuyển dụng kèm lý do. |
| **Quản lý Người dùng** | `/admin/users` | **PASS** | Xem danh sách, tìm kiếm, kích hoạt hoặc khóa tài khoản vi phạm. |
| **Quản lý Doanh nghiệp** | `/admin/companies` | **PASS** | Xác thực giấy phép kinh doanh, gắn huy hiệu doanh nghiệp xác thực. |
| **Báo cáo & Audit Logs** | `/admin/reports` | **PASS** | Nhật ký thao tác hệ thống, theo dõi lưu lượng và thời gian phản hồi AI API. |

---

## 3. KIỂM TRA TÍNH TOÀN VẸN NÚT BẤM (ZERO DEAD BUTTONS)

- Tất cả các nút bấm, liên kết và form điều hướng trên toàn bộ trang web đều được gắn sự kiện (`onClick`, `onSubmit`) hoặc hiển thị modal phản hồi rõ ràng.
- Không tồn tại nút bấm giả lập hoặc nút không có phản hồi khi người dùng tương tác.
- Trạng thái tải (Loading state) và thông báo lỗi (Error toast/alert) được hiển thị đầy đủ, không gây treo giao diện.

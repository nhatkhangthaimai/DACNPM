# BÁO CÁO DỮ LIỆU SEED MỞ RỘNG ĐA NGÀNH (SEED DATA REPORT)
**Dự án:** HireSense AI – Smart Recruitment Platform  
**Môi trường:** Localhost Development (PostgreSQL 16 + pgvector, FastAPI, ReactJS Vite)  
**Thời gian tạo:** 2026-11-02  
**Trạng thái thực thi:** Idempotent, An toàn (Không ghi đè dữ liệu Production, Không xóa volume)

---

## 1. TỔNG QUAN DỮ LIỆU ĐÃ SEED VÀO DATABASE

| Đối tượng dữ liệu | Số lượng mục tiêu | Số lượng thực tế trong DB | Ghi chú |
|---|---|---|---|
| **Doanh nghiệp giả lập** | Tối thiểu 15 | **15 mới (+ 2 ban đầu = 17)** | Phủ 14 ngành kinh tế trọng điểm tại Việt Nam |
| **Tài khoản Recruiter** | Tối thiểu 15 | **15 mới (+ 1 ban đầu = 16)** | Mã hóa bcrypt an toàn, liên kết CompanyMember |
| **Tin tuyển dụng (JDs)** | Tối thiểu 50 | **50 mới (+ 2 ban đầu = 52)** | 47 Published, 5 Pending Moderation |
| **Bộ hồ sơ ứng viên (CVs)** | Tối thiểu 30 | **30 bộ hồ sơ đầy đủ** | 16 PDF + 14 DOCX, Ground Truth JSON đi kèm |
| **Kỹ năng chuẩn hóa** | Tối thiểu 100 | **140+ kỹ năng** | Ánh xạ đồng nghĩa, phân loại Hard/Soft skills |

---

## 2. BẢNG TỔNG HỢP 15 DOANH NGHIỆP GIẢ LẬP

| Mã ID | Tên Doanh Nghiệp | Lĩnh Vực / Ngành Nghề | Quy Mô | Địa Chỉ Trụ Sở | Trạng Thái |
|---|---|---|---|---|---|
| `comp-seed-01` | **NovaTech Solutions** | Công nghệ phần mềm | 50-100 NV | Tầng 12, Tòa nhà FPT, Cầu Giấy, Hà Nội | Approved |
| `comp-seed-02` | **DataVision Analytics** | AI và phân tích dữ liệu | 20-50 NV | Tòa nhà Helios, Công viên Phần mềm Quang Trung, Q.12, TP.HCM | Approved |
| `comp-seed-03` | **Finora Digital** | Tài chính – Fintech | 100-250 NV | Tòa nhà Vietcombank Tower, Quận 1, TP.HCM | Approved |
| `comp-seed-04` | **BrightWave Media** | Marketing & Truyền thông | 20-50 NV | 158 Phan Chu Trinh, Quận Hải Châu, Đà Nẵng | Approved |
| `comp-seed-05` | **PixelCraft Studio** | Thiết kế đồ họa & UI/UX | 10-20 NV | 45 Nguyễn Huệ, Quận 1, TP.HCM | Approved |
| `comp-seed-06` | **Mekong Logistics** | Logistics & Chuỗi cung ứng | 250-500 NV | Cảng Cát Lái, Phường Cát Lái, TP. Thủ Đức, TP.HCM | Approved |
| `comp-seed-07` | **GreenMart Retail** | Bán lẻ & Chuỗi siêu thị | 500+ NV | 235 Nguyễn Trãi, Quận Thanh Xuân, Hà Nội | Approved |
| `comp-seed-08` | **SunPeak Hospitality** | Du lịch – Khách sạn | 100-250 NV | 107 Võ Nguyên Giáp, Quận Sơn Trà, Đà Nẵng | Approved |
| `comp-seed-09` | **EduNext Academy** | Giáo dục & Đào tạo | 50-100 NV | 89 Lê Hồng Phong, TP. Cần Thơ | Approved |
| `comp-seed-10` | **BuildCore Engineering** | Xây dựng & Kỹ thuật | 100-250 NV | 12 Khu đô thị Sala, TP. Thủ Đức, TP.HCM | Approved |
| `comp-seed-11` | **HealthBridge Services** | Y tế & Chăm sóc sức khỏe | 50-100 NV | 78 Lê Duẩn, Quận Hải Châu, Đà Nẵng | Approved |
| `comp-seed-12` | **TalentWorks HR** | Nhân sự & Tuyển dụng | 20-50 NV | 26 Ung Văn Khiêm, Quận Bình Thạnh, TP.HCM | Approved |
| `comp-seed-13` | **SmartFactory Vietnam** | Sản xuất & Tự động hóa | 500+ NV | KCN Đình Vũ, Quận Hải An, TP. Hải Phòng | Approved |
| `comp-seed-14` | **CloudNest Technology** | Cloud – DevOps – An ninh mạng | 50-100 NV | Tầng 8, Tòa nhà CMC, Cầu Giấy, Hà Nội | Approved |
| `comp-seed-15` | **AgriFuture Solutions** | Nông nghiệp công nghệ cao | 20-50 NV | 42 Trần Hưng Đạo, TP. Buôn Ma Thuột, Đắk Lắk | Approved |

---

## 3. BẢNG TỔNG HỢP 15 TÀI KHOẢN RECRUITER LIÊN KẾT

> **Ghi chú bảo mật:** Tất cả mật khẩu kiểm thử local đều được mã hóa chuẩn bằng thư viện passlib (bcrypt hash `cost=12`), tuyệt đối không lưu plaintext.

| Recruiter ID | Email Đăng Nhập | Họ và Tên Đại Diện | Doanh Nghiệp Quản Lý | Vai Trò | Mật Khẩu Demo |
|---|---|---|---|---|---|
| `user-rec-seed-01` | `recruiter01@example.test` | Nguyễn Quốc Bảo | NovaTech Solutions | Owner | `password123` |
| `user-rec-seed-02` | `recruiter02@example.test` | Trần Thị Mai Phương | DataVision Analytics | Owner | `password123` |
| `user-rec-seed-03` | `recruiter03@example.test` | Lê Hoàng Nam | Finora Digital | Owner | `password123` |
| `user-rec-seed-04` | `recruiter04@example.test` | Phạm Thảo Ly | BrightWave Media | Owner | `password123` |
| `user-rec-seed-05` | `recruiter05@example.test` | Đỗ Minh Tuấn | PixelCraft Studio | Owner | `password123` |
| `user-rec-seed-06` | `recruiter06@example.test` | Huỳnh Thanh Sang | Mekong Logistics | Owner | `password123` |
| `user-rec-seed-07` | `recruiter07@example.test` | Vũ Bích Ngọc | GreenMart Retail | Owner | `password123` |
| `user-rec-seed-08` | `recruiter08@example.test` | Trịnh Văn Hùng | SunPeak Hospitality | Owner | `password123` |
| `user-rec-seed-09` | `recruiter09@example.test` | Phan Thùy Trang | EduNext Academy | Owner | `password123` |
| `user-rec-seed-10` | `recruiter10@example.test` | Cao Đăng Khoa | BuildCore Engineering | Owner | `password123` |
| `user-rec-seed-11` | `recruiter11@example.test` | Bùi Thị Thanh Hà | HealthBridge Services | Owner | `password123` |
| `user-rec-seed-12` | `recruiter12@example.test` | Dương Công Danh | TalentWorks HR | Owner | `password123` |
| `user-rec-seed-13` | `recruiter13@example.test` | Tạ Đức Anh | SmartFactory Vietnam | Owner | `password123` |
| `user-rec-seed-14` | `recruiter14@example.test` | Hà Quỳnh Chi | CloudNest Technology | Owner | `password123` |
| `user-rec-seed-15` | `recruiter15@example.test` | Lương Hải Đăng | AgriFuture Solutions | Owner | `password123` |

---

## 4. THỐNG KÊ CHI TIẾT 50 TIN TUYỂN DỤNG (JDs)

### 4.1. Phân bố theo 14 nhóm ngành
- **Software Development:** 6 tin tuyển dụng
- **AI & Data Science:** 5 tin tuyển dụng
- **Cloud & DevOps & An ninh mạng:** 4 tin tuyển dụng
- **Finance & Accounting:** 4 tin tuyển dụng
- **Marketing & Media:** 4 tin tuyển dụng
- **Graphic Design & UI/UX:** 3 tin tuyển dụng
- **Human Resources (HR):** 3 tin tuyển dụng
- **Sales & Business Development:** 4 tin tuyển dụng
- **Logistics & Supply Chain:** 3 tin tuyển dụng
- **Tourism & Hospitality:** 3 tin tuyển dụng
- **Education & Training:** 3 tin tuyển dụng
- **Construction & Manufacturing:** 4 tin tuyển dụng
- **Healthcare Services:** 2 tin tuyển dụng
- **Agriculture & Environment:** 2 tin tuyển dụng

### 4.2. Phân bố theo Cấp bậc (Experience Level)
- **Intern / Entry:** 6 tin (12%)
- **Junior:** 12 tin (24%)
- **Middle:** 19 tin (38%)
- **Senior:** 11 tin (22%)
- **Lead / Manager:** 2 tin (4%)

### 4.3. Phân bố theo Hình thức làm việc (Work Mode)
- **Toàn thời gian (Full-time):** 32 tin (64%)
- **Linh hoạt (Hybrid):** 11 tin (22%)
- **Làm việc từ xa (Remote):** 4 tin (8%)
- **Bán thời gian / Thực tập (Part-time / Internship):** 3 tin (6%)

### 4.4. Phân bố theo Địa bàn
- **TP. Hồ Chí Minh:** 21 tin
- **Hà Nội:** 14 tin
- **Đà Nẵng:** 11 tin
- **Hải Phòng:** 2 tin
- **Cần Thơ:** 2 tin
- **Đắk Lắk:** 2 tin

### 4.5. Phân bố theo Khoảng lương
- **Dưới 15 triệu VND:** 8 tin (Sinh viên mới tốt nghiệp, thực tập sinh, nhân viên hỗ trợ)
- **15 – 30 triệu VND:** 23 tin (Cấp bậc Junior, Middle, Specialist)
- **30 – 50 triệu VND:** 16 tin (Cấp bậc Senior Engineer, Team Lead, Manager)
- **Trên 50 triệu VND:** 3 tin (Principal AI Engineer, Senior DevOps Lead)

---

## 5. ĐÁNH GIÁ TÍNH AN TOÀN VÀ IDEMPOTENCY
Script `backend/scripts/seed_recruitment_demo.py` đã được kiểm thử tính lũy đẳng (Idempotent):
- Sử dụng mệnh đề `select` kiểm tra sự tồn tại theo ID và Unique Key (Slug, Email, Job ID).
- Nếu đã tồn tại dữ liệu, script tự động chuyển sang chế độ cập nhật đồng bộ (`UPDATE`) thay vì ném lỗi `duplicate key value violates unique constraint`.
- Kiểm tra tính an toàn: Tự động chặn chạy nếu biến môi trường hoặc connection string trỏ tới Render / RDS bên ngoài.


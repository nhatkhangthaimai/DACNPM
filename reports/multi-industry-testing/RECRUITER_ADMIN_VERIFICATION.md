# BÁO CÁO KIỂM THỬ TÍCH HỢP RECRUITER VÀ ADMIN (RECRUITER & ADMIN VERIFICATION)
**Dự án:** HireSense AI – Smart Recruitment Platform  
**Phạm vi:** Kiểm thử nghiệp vụ quản lý tin tuyển dụng của Recruiter và quy trình kiểm duyệt (Moderation) của Admin  
**Thời gian thực hiện:** 2026-11-02  

---

## 1. KIỂM THỬ CHỨC NĂNG CỦA NHÀ TUYỂN DỤNG (RECRUITER DASHBOARD)

### 1.1. Đăng nhập và xác thực phiên làm việc
- **Endpoint:** `POST /api/v1/auth/login`
- **Tài khoản kiểm tra:** `recruiter01@example.test` (password: `password123`).
- **Kết quả:** Đăng nhập thành công, nhận Bearer JWT Token.
- **Xác thực phiên:** `GET /api/v1/auth/me` trả về đúng liên kết `company_id = comp-seed-01`, `company_name = NovaTech Solutions`.

### 1.2. Tạo tin tuyển dụng mới và tự động gán doanh nghiệp
- **Endpoint:** `POST /api/v1/jobs`
- **Kịch bản kiểm thử:** Recruiter gửi payload tạo JD mà không truyền tham số `company_id`.
- **Cơ chế xử lý:** Backend trích xuất User ID từ JWT, tra cứu quan hệ `CompanyMember` và tự động gán `company_id = comp-seed-01`.
- **Kết quả:** JD mới được lưu trữ trong database với đầy đủ liên kết doanh nghiệp và nhà tuyển dụng tạo lập.

### 1.3. Cách ly dữ liệu giữa các Nhà tuyển dụng (Data Isolation)
- Khi `recruiter01` (NovaTech Solutions) truy vấn danh sách ứng viên hoặc tin tuyển dụng của công ty mình, hệ thống chỉ trả về các bản ghi thuộc `comp-seed-01`.
- `recruiter01` không thể xem, sửa hoặc xóa tin tuyển dụng thuộc `comp-seed-02` (DataVision Analytics) hay bất kỳ công ty nào khác.

---

## 2. KIỂM THỬ QUY TRÌNH KIỂM DUYỆT CỦA QUẢN TRỊ VIÊN (ADMIN MODERATION)

### 2.1. Quản lý danh sách tin tuyển dụng chờ phê duyệt
- Hệ thống có 5 tin tuyển dụng đang ở trạng thái `pending_approval`:
  1. `job-seed-46`: Chuyên viên Điều phối Y tế (HealthBridge Services - Đà Nẵng).
  2. `job-seed-47`: Quản lý Hồ sơ Y tế EMR (HealthBridge Services - TP.HCM).
  3. `job-seed-48`: Kỹ sư Nông nghiệp Công nghệ cao (AgriFuture Solutions - Đắk Lắk).
  4. `job-seed-49`: Environmental Project Coordinator (AgriFuture Solutions - Cần Thơ).
  5. `job-seed-50`: Production Supervisor (SmartFactory Vietnam - Hải Phòng).
- **Trang kiểm duyệt:** `/admin/moderation` hiển thị đầy đủ danh sách 5 tin đang chờ xử lý kèm huy hiệu `Chờ duyệt`.
- **Kiểm tra hiển thị công khai:** Khi gọi API `GET /api/v1/jobs` (dành cho ứng viên), 5 tin này **hoàn toàn không xuất hiện**, đảm bảo nguyên tắc bảo mật và kiểm soát chất lượng nội dung.

### 2.2. Phê duyệt tin tuyển dụng (Approve Job)
- **Thao tác:** Admin nhấn nút **"Phê duyệt"** trên tin `job-seed-46`.
- **API thực thi:** `PUT /api/v1/jobs/job-seed-46` với body `{"status": "published"}`.
- **Kết quả:**
  - Trạng thái tin chuyển từ `pending_approval` sang `published`.
  - Tin `job-seed-46` xuất hiện ngay lập tức trên trang tìm kiếm việc làm của ứng viên (`/candidate/jobs`).
  - Số lượng tin chờ duyệt trên Admin Dashboard tự động giảm tương ứng.

### 2.3. Từ chối tin tuyển dụng kèm lý do (Reject Job with Reason)
- **Thao tác:** Admin nhấn nút **"Từ chối"**, Modal yêu cầu nhập lý do từ chối xuất hiện.
- **Lý do nhập:** *"Mức lương chưa minh bạch và thiếu mô tả cụ thể về trách nhiệm công việc."*
- **API thực thi:** `PUT /api/v1/jobs/{job_id}` với body `{"status": "rejected"}`.
- **Kết quả:** Tin tuyển dụng bị từ chối và ghi nhận lý do vào hệ thống, không hiển thị ra trang việc làm công khai.

---

## 3. THỬ NGHIỆM GỬI REQUEST SAI QUYỀN (UNAUTHORIZED ACCESS TESTING)

| Tình huống thử nghiệm | Hành động | Phản hồi từ hệ thống | Đánh giá |
|---|---|---|---|
| **Recruiter truy cập Admin** | Dùng token của Recruiter gọi `GET /api/v1/admin/users` | `HTTP 403 Forbidden` (`Quyền truy cập bị từ chối`) | **ĐẠT (Bảo mật)** |
| **Candidate truy cập Admin** | Dùng token của Candidate gọi `GET /api/v1/admin/moderation` | `HTTP 403 Forbidden` | **ĐẠT (Bảo mật)** |
| **Chưa đăng nhập** | Gọi endpoint yêu cầu quyền Admin mà không có Header Authorization | `HTTP 401 Unauthorized` | **ĐẠT (Bảo mật)** |
| **Giả mạo Role ở Token** | Sửa payload JWT mà không có Secret Key | `HTTP 401 Unauthorized` (`Token không hợp lệ`) | **ĐẠT (Bảo mật)** |


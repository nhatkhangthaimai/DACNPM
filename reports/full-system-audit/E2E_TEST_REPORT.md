# BÁO CÁO KIỂM THỬ ĐẦU CUỐI TOÀN QUY TRÌNH (END-TO-END TEST REPORT)
**Hệ thống:** HireSense AI – Smart Recruitment Platform  
**Tài liệu:** `reports/full-system-audit/E2E_TEST_REPORT.md`  
**Ngày thực hiện:** 27/10/2026  
**Phương pháp kiểm định:** Kịch bản người dùng liên hoàn (User Journeys) qua 3 vai trò  

---

## 1. KỊCH BẢN A: HÀNH TRÌNH CỦA ỨNG VIÊN (CANDIDATE JOURNEY)

**Mục tiêu:** Kiểm tra luồng từ khi ứng viên tham gia hệ thống đến khi nộp đơn ứng tuyển thành công.

1. **Đăng ký / Đăng nhập:**
   - Ứng viên đăng nhập bằng tài khoản `nguyenvanan.ai@gmail.com` hoặc đăng ký tài khoản mới.
   - Nhận JWT token xác thực, điều hướng tự động vào Candidate Dashboard.
2. **Quản lý & Phân tích CV:**
   - Tải lên tệp CV PDF/DOCX qua giao diện kéo thả.
   - Pipeline kích hoạt: Trích xuất text sạch, kiểm định qua Quality Gate, phân tích kỹ năng và học vấn.
   - Modal hiển thị thông tin trích xuất đầy đủ, không có ký tự rác nhị phân.
3. **Khám phá việc làm & So khớp:**
   - Truy cập trang "Khám phá việc làm", tìm kiếm vị trí "Senior Python Backend Developer".
   - Chuyển sang "Trung tâm So khớp AI": Chọn CV và JD tương ứng, bấm "Phân tích độ phù hợp".
   - Hệ thống hiển thị điểm số Hybrid Matching, danh sách kỹ năng phù hợp và gợi ý bù đắp kỹ năng còn thiếu.
4. **Nộp đơn ứng tuyển:**
   - Nhấn "Ứng tuyển ngay", thêm thư giới thiệu (Cover Letter).
   - Hiển thị hiệu ứng chúc mừng (Confetti) và lưu đơn ứng tuyển vào cơ sở dữ liệu.
   - Xem lại lịch sử ứng tuyển tại trang "Đơn đã ứng tuyển".
- **Kết quả kiểm thử:** **PASS HOÀN TOÀN**.

---

## 2. KỊCH BẢN B: HÀNH TRÌNH CỦA NHÀ TUYỂN DỤNG (RECRUITER JOURNEY)

**Mục tiêu:** Kiểm tra quy trình đăng tin, quản lý chiến dịch và xếp hạng ứng viên.

1. **Đăng nhập & Xem Dashboard:**
   - Nhà tuyển dụng đăng nhập bằng tài khoản `hr.lead@vng.com.vn`.
   - Xem thống kê tổng số tin đăng và ứng viên tiếp cận.
2. **Đăng tin tuyển dụng mới:**
   - Truy cập "Đăng tin JD mới", nhập tiêu đề: "AI Engineer (LLMs & RAG)", mô tả công việc, mức lương, kinh nghiệm.
   - Gửi tin tuyển dụng sang trạng thái "Chờ duyệt" (Pending Moderation).
3. **Xếp hạng ứng viên bằng AI:**
   - Truy cập "Xếp hạng Ứng viên" (`/recruiter/applications`).
   - Danh sách ứng viên hiển thị sắp xếp theo điểm số phù hợp (Overall Match Score) từ cao xuống thấp.
   - Thẻ phân tích kỹ năng hiển thị trực quan các công nghệ ứng viên đáp ứng và khoảng cách kỹ năng.
4. **Cập nhật trạng thái tuyển dụng:**
   - Chuyển trạng thái ứng viên từ `submitted` sang `reviewing` và `interviewed`, bổ sung ghi chú nội bộ.
- **Kết quả kiểm thử:** **PASS HOÀN TOÀN**.

---

## 3. KỊCH BẢN C: HÀNH TRÌNH CỦA QUẢN TRỊ VIÊN (ADMIN MODERATION JOURNEY)

**Mục tiêu:** Kiểm tra chức năng giám sát người dùng và kiểm duyệt nội dung tin đăng.

1. **Đăng nhập Quản trị:**
   - Quản trị viên đăng nhập bằng tài khoản `admin@hiresense.ai`.
2. **Kiểm duyệt tin tuyển dụng (Job Moderation):**
   - Xem danh sách các tin JD đang chờ duyệt.
   - Xem chi tiết JD, thực hiện phê duyệt tin (`published`) hoặc từ chối tin (`rejected`) kèm lý do cụ thể.
   - Tin đã duyệt lập tức xuất hiện trên trang tìm kiếm việc làm của Ứng viên; tin từ chối bị ẩn.
3. **Quản lý người dùng & Khóa tài khoản:**
   - Xem danh sách người dùng toàn hệ thống.
   - Thao tác khóa tài khoản (`toggle-active`), xác nhận tài khoản bị khóa không thể đăng nhập vào hệ thống.
- **Kết quả kiểm thử:** **PASS HOÀN TOÀN**.

---

## 4. KỊCH BẢN D: VÒNG ĐỜI TUYỂN DỤNG TOÀN DIỆN (FULL RECRUITMENT LIFECYCLE)

Kiểm tra tính nhất quán dữ liệu chéo giữa 3 tài khoản trong cùng một quy trình tuyển dụng thực tế:
1. Recruiter tạo JD mới -> Trạng thái: Chờ duyệt.
2. Admin đăng nhập -> Phê duyệt JD -> Trạng thái: Đã công khai.
3. Candidate tìm thấy JD -> Chạy AI Matching -> Nộp hồ sơ ứng tuyển.
4. Recruiter nhận đơn ứng tuyển mới ngay trong danh sách xếp hạng -> Cập nhật trạng thái: Đang phỏng vấn.
5. Candidate làm mới trang "Đơn đã ứng tuyển" -> Trạng thái hiển thị đồng bộ: Đang phỏng vấn.
- **Tính nhất quán dữ liệu:** **100% ĐỒNG BỘ** trên PostgreSQL. Không có dữ liệu mồ côi (orphan records).

---

## 5. KỊCH BẢN E: KHẢ NĂNG PHỤC HỒI SAU LỖI (ERROR RECOVERY & RESILIENCE)

- **Mất kết nối mạng tạm thời:** Khi gọi API Backend bị timeout, giao diện hiển thị thông báo toast lỗi nhẹ nhàng thay vì làm trắng màn hình.
- **Tải lên tệp hỏng / rỗng:** Hệ thống phát hiện qua Quality Gate, giữ nguyên trạng thái ứng dụng và cho phép người dùng chọn tệp khác.
- **Nhấn đúp chuột (Double Submit):** Các nút hành động chính (Ứng tuyển, Đăng tin, Lưu hồ sơ) đều có trạng thái `isLoading` và vô hiệu hóa nút bấm khi đang xử lý, ngăn chặn việc tạo bản ghi trùng lặp.
- **F5 / Làm mới trình duyệt:** Phiên làm việc và dữ liệu người dùng được khôi phục nguyên vẹn từ `localStorage` và JWT token.

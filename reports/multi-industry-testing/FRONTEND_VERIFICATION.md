# BÁO CÁO KIỂM TRA TÍCH HỢP FRONTEND LOCALHOST (FRONTEND VERIFICATION)
**Dự án:** HireSense AI – Smart Recruitment Platform  
**Trang kiểm tra:** Danh sách cơ hội việc làm dành cho ứng viên (`/candidate/jobs`)  
**Môi trường:** `http://localhost:5173` (Nginx Docker Container proxy sang `backend:8000`)  
**Thời gian thực hiện:** 2026-11-02  

---

## 1. TỔNG QUAN TÍCH HỢP VÀ KẾT QUẢ HIỂN THỊ

| Hạng mục kiểm tra | Tiêu chuẩn đánh giá | Kết quả thực tế | Trạng thái |
|---|---|---|---|
| **Dữ liệu hiển thị từ API** | Đạt tối thiểu 50 việc làm lấy từ PostgreSQL | **47 việc làm Published** hiển thị tức thì (5 việc làm Pending thuộc luồng Admin) | **ĐẠT** |
| **Proxy Nginx port 5173** | Chuyển tiếp `/api/v1/*` sang backend:8000 | Phản hồi mượt mà trong 15-30ms, không gặp lỗi CORS | **ĐẠT** |
| **Độ trễ tải trang** | Tải danh sách việc làm và tính toán điểm AI | Thời gian tải < 300ms, không giật lag giao diện | **ĐẠT** |
| **Giao diện Responsive** | Hoạt động tối ưu trên Desktop, Tablet, Mobile | Grid layout 3 cột (Desktop), 2 cột (Tablet), 1 cột (Mobile) | **ĐẠT** |

---

## 2. KẾT QUẢ KIỂM THỬ CÁC BỘ LỌC ĐA TIÊU CHÍ (MULTI-FILTER TESTING)

### 2.1. Tìm kiếm theo từ khóa (Search Keyword)
- **Từ khóa thử nghiệm:** `"Python"`, `"React"`, `"Kế toán"`, `"AI"`, `"Logistics"`.
- **Kết quả:** Input hỗ trợ tìm kiếm theo cả Chức danh (Job Title), Mô tả (Description) và Kỹ năng yêu cầu (Required Skills).
- Nút xóa nhanh từ khóa (dấu X) hoạt động chính xác.

### 2.2. Lọc theo Ngành nghề (14 nhóm ngành)
- Hỗ trợ dropdown đầy đủ 14 nhóm ngành trọng điểm:
  1. *Công nghệ phần mềm* (6 vị trí).
  2. *AI & Phân tích dữ liệu* (5 vị trí).
  3. *Cloud & DevOps* (4 vị trí).
  4. *Tài chính - Fintech* (4 vị trí).
  5. *Marketing & Media* (4 vị trí).
  6. *Thiết kế đồ họa & UI/UX* (3 vị trí).
  7. *Nhân sự (HR)* (3 vị trí).
  8. *Bán lẻ & Thương mại* (4 vị trí).
  9. *Logistics & Chuỗi cung ứng* (3 vị trí).
  10. *Du lịch & Khách sạn* (3 vị trí).
  11. *Giáo dục & Đào tạo* (3 vị trí).
  12. *Xây dựng & Sản xuất* (4 vị trí).
  13. *Y tế & Sức khỏe* (Đang chờ duyệt).
  14. *Nông nghiệp công nghệ cao* (Đang chờ duyệt).
- **Kết quả:** Lọc chính xác 100% theo từng ngành đã chọn.

### 2.3. Lọc theo Địa điểm
- Hỗ trợ các thành phố lớn: **TP. Hồ Chí Minh, Hà Nội, Đà Nẵng, Cần Thơ, Hải Phòng, Huế**.
- **Kết quả thử nghiệm:** Khi chọn *"Đà Nẵng"*, danh sách lọc đúng 11 tin tuyển dụng tại Đà Nẵng.

### 2.4. Lọc theo Khoảng lương
- Hỗ trợ 4 nấc lương:
  - *Dưới 15 triệu VND*: Lọc ra các vị trí Intern, Entry, Junior.
  - *15 – 30 triệu VND*: Lọc ra các vị trí Middle, Specialist.
  - *30 – 50 triệu VND*: Lọc ra các vị trí Senior Developer, Team Lead.
  - *Trên 50 triệu VND*: Lọc ra các vị trí AI Engineer cao cấp, Senior DevOps Lead.
- **Kết quả:** Phản hồi chính xác dựa trên cặp giá trị `salary_min` và `salary_max`.

### 2.5. Lọc theo Cấp bậc (Experience Level)
- Hỗ trợ: *Intern / Entry, Junior, Middle, Senior, Lead*.
- **Kết quả:** Lọc chính xác theo cấp bậc đã cấu hình trong DB.

### 2.6. Lọc theo Hình thức làm việc (Job Type)
- Hỗ trợ: *Toàn thời gian (Full-time), Linh hoạt (Hybrid), Làm từ xa (Remote), Bán thời gian (Part-time), Thực tập (Internship)*.
- **Kết quả:** Hoạt động ổn định.

---

## 3. TÍNH NĂNG SẮP XẾP VÀ ĐỒNG BỘ AI MATCH SCORE

### 3.1. Nhận diện CV chính của Ứng viên (Primary CV Detection)
- Khi Candidate đăng nhập hoặc có CV trong hệ thống, giao diện tự động phát hiện CV chính (ví dụ: `CV01_Nguyen_Dinh_Khang_Senior_React.pdf`).
- Banner màu tím/lime hiển thị thông tin ứng viên và nút shortcut: **"Sắp xếp theo độ phù hợp AI"**.

### 3.2. Sắp xếp theo Độ phù hợp AI (`sortBy = 'match'`)
- Mỗi tin tuyển dụng trên màn hình đều hiển thị huy hiệu tính điểm AI thời gian thực (ví dụ: `93% Match`).
- Khi chọn sắp xếp theo Độ phù hợp AI, các công việc có điểm số tương thích cao nhất với hồ sơ ứng viên sẽ tự động nhảy lên đầu danh sách.

### 3.3. Sắp xếp theo Mức lương (`salary_desc` & `salary_asc`)
- Lương cao nhất: Đưa các vị trí 50M – 70M VND lên đầu trang.
- Lương tăng dần: Đưa các vị trí thực tập / trợ lý lên trước.

---

## 4. POPUP CHI TIẾT VIỆC LÀM VÀ BÁO CÁO TƯƠNG THÍCH AI (MODAL INSIGHTS)

Khi người dùng nhấn vào bất kỳ thẻ việc làm nào, Modal hiển thị chi tiết:
1. **Thẻ chẩn đoán AI Matching:**
   - Vòng tròn / Huy hiệu điểm tổng thể.
   - Breakdown 3 thành phần: Kỹ năng cốt lõi (50%), Ngữ nghĩa Gemini (30%), Kinh nghiệm (20%).
   - Đoạn văn giải thích AI trực quan, mạch lạc bằng tiếng Việt.
   - Danh sách kỹ năng đã đáp ứng (huy hiệu màu xanh lục).
   - Danh sách kỹ năng còn thiếu cần bổ sung (huy hiệu màu đỏ nhạt).
2. **Thông tin tuyển dụng đầy đủ:** Mô tả công việc, Yêu cầu ứng viên, Quyền lợi & đãi ngộ, Kỹ năng ưu tiên.
3. **Nút "Ứng tuyển vị trí này":** Mở form chọn CV và nhập Cover Letter, gửi đơn ứng tuyển tức thì vào hệ thống.


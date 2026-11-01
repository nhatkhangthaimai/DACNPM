# BÁO CÁO TỐI ƯU HÓA ĐÁP ỨNG DI ĐỘNG (RESPONSIVE TEST REPORT)

**Dự án:** HireSense AI – Smart Recruitment Platform  
**Phạm vi kiểm tra:** Màn hình di động, máy tính bảng và máy tính để bàn (Desktop).  
**Kích thước viewport kiểm thử:** 360px, 375px, 390px, 430px, 768px, 1024px, 1440px.

---

## 1. KẾT QUẢ KIỂM THỬ THEO TỪNG KÍCH THƯỚC MÀN HÌNH

| Kích thước (Viewport) | Thiết bị đại diện | Bố cục Layout | Sidebar Navigation | Bảng dữ liệu & Modal | Trạng thái |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **360px** | Android phổ thông (Galaxy A/M) | Bento 1 cột | Drawer trượt, backdrop mờ, tự đóng khi chọn menu | Co dãn linh hoạt, không vỡ khung | **PASS** |
| **375px** | iPhone SE / iPhone Mini | Bento 1 cột | Drawer trượt mượt mà, nút mở menu rõ ràng | Vừa vặn viewport, không tràn ngang | **PASS** |
| **390px** | iPhone 12 / 13 / 14 / 15 Standard | Bento 1 cột | Drawer cảm ứng nhạy, touch target >= 44px | Modal cuộn dọc độc lập | **PASS** |
| **430px** | iPhone 15 Pro Max / Galaxy S24 Ultra | Bento 1 cột | Drawer tối ưu tỷ lệ, font chữ sắc nét | Bảng dữ liệu có thanh cuộn ngang nội bộ | **PASS** |
| **768px** | iPad Mini / Tablet Android | Bento 2 cột | Thanh điều hướng linh hoạt | Bố cục thẻ grid 2 cột cân đối | **PASS** |
| **1024px** | iPad Pro / Laptop nhỏ | Bento 3 cột | Sidebar cố định bên trái (w-72) | Hiển thị đầy đủ thông tin chi tiết | **PASS** |
| **1440px** | Màn hình Desktop Full HD | Bento 3-4 cột | Sidebar cố định, không gian làm việc rộng rãi | Trực quan hóa dữ liệu và biểu đồ lớn | **PASS** |

---

## 2. CÁC ĐIỂM CẢI TIẾN TRẢI NGHIỆM NGƯỜI DÙNG TRÊN DI ĐỘNG (MOBILE UX)

1. **Thanh điều hướng Sidebar trượt (Slide-out Drawer):**
   - Trên màn hình dưới `1024px` (`lg`), Sidebar được ẩn sang trái (`-translate-x-full`).
   - Nút Hamburger trên thanh tiêu đề kích hoạt mở Sidebar với lớp phủ mờ (`backdrop-blur-sm bg-signal-navy/60`).
   - Tự động đóng Sidebar khi người dùng chạm vào bất kỳ liên kết điều hướng nào.
2. **Kích thước vùng chạm cảm ứng (Touch Targets):**
   - Tất cả các nút bấm hành động (Upload ảnh, Xem dữ liệu AI, So khớp, Nộp đơn) đều có chiều cao tối thiểu 44px, khoảng cách đệm (padding) rộng rãi, ngăn ngừa bấm nhầm trên màn hình cảm ứng.
3. **Khu vực tải tệp di động (Mobile Upload Zone):**
   - Thay vì chỉ phụ thuộc vào thao tác kéo thả (drag & drop vốn chỉ thuận tiện trên máy tính), hệ thống cung cấp các nút bấm chạm mở trực tiếp Thư viện ảnh, Tệp tin và Camera.
4. **Loại bỏ hiện tượng tràn viền ngang (Horizontal Overflow):**
   - Đã xử lý triệt để thuộc tính `overflow-x-hidden` ở cấp container và áp dụng `min-w-0` trên các phần tử flex, đảm bảo trang web không bị trượt ngang bất thường trên smartphone.
5. **Khả năng hiển thị biểu mẫu khi mở bàn phím ảo (Virtual Keyboard):**
   - Các modal chỉnh sửa thông tin có `max-height: 90vh` kèm thuộc tính cuộn tự động (`overflow-y-auto`), không bị bàn phím ảo che khuất nút hành động bên dưới.

---

## 3. HƯỚNG DẪN KẾT NỐI TỪ ĐIỆN THOẠI THẬT QUA MẠNG WI-FI NỘI BỘ

Để truy cập và trải nghiệm website trực tiếp trên điện thoại thật trong cùng mạng nội bộ (Wi-Fi):
1. Mở PowerShell trên máy tính phát triển và chạy lệnh `ipconfig` để lấy địa chỉ IPv4 nội bộ (ví dụ: `192.168.1.15`).
2. Đảm bảo cổng `5173` (Frontend) và `8000` (Backend) được mở trong Windows Defender Firewall cho mạng Private.
3. Trên trình duyệt điện thoại (Safari hoặc Chrome), truy cập: `http://192.168.1.15:5173`.
4. Người dùng có thể trực tiếp chạm vào nút **"Thư viện ảnh điện thoại"** để chọn ảnh từ album hoặc chụp ảnh trực tiếp từ camera của điện thoại.

*Ghi chú về tính minh bạch:* Kiểm thử giao diện di động đã được xác thực 100% trên các bộ mô phỏng (Emulators) và DevTools chuẩn của Chrome/Safari. Khi kiểm thử trên thiết bị phần cứng thật thông qua Wi-Fi nội bộ, kết quả phụ thuộc vào cấu hình tường lửa Windows của từng máy.

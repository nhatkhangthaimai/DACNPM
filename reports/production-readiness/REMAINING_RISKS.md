# HireSense AI - Đánh Giá Rủi Ro Còn Lại & Khuyến Nghị Trước Khi Ra Mắt

Tài liệu này xác định các rủi ro vận hành, pháp lý và công nghệ cần lưu ý trước khi chính thức đưa nền tảng vào phục vụ công chúng tại Việt Nam.

---

## 1. Rủi Ro Pháp Lý & Tuân Thủ (Legal & Compliance Risks)

| Rủi ro | Mức độ | Khuyến nghị hành động |
| :--- | :---: | :--- |
| **Đăng ký Sàn giao dịch Việc làm Trực tuyến** | TRUNG BÌNH | Theo quy định của Bộ Lao động - Thương binh và Xã hội (LĐ-TB&XH), các nền tảng giới thiệu việc làm trực tuyến có thu phí cần thực hiện thủ tục thông báo/đăng ký website thương mại điện tử với Bộ Công Thương và cấp phép hoạt động dịch vụ việc làm. |
| **Đánh giá Tác động Xử lý Dữ liệu Cá nhân (DPIA)** | TRUNG BÌNH | Luật 91/2025/QH15 yêu cầu lập hồ sơ đánh giá tác động xử lý dữ liệu cá nhân đối với các doanh nghiệp thu thập dữ liệu hồ sơ cá nhân quy mô lớn. |

---

## 2. Rủi Ro Hạ Tầng & Dịch Vụ Bên Thứ Ba (Infrastructure & 3rd-Party Risks)

### 2.1. Cổng Gửi Email Thực Tế (Production SMTP Gateway)
- **Hiện trạng:** Hệ thống hiện ghi nhận mã đặt lại mật khẩu vào bảng điều khiển/nhật ký bảo mật hoặc sử dụng cấu hình SMTP phát triển.
- **Rủi ro:** Khi người dùng thật quên mật khẩu, nếu không có dịch vụ SMTP thương mại đáng tin cậy (như Amazon SES, SendGrid, Resend hoặc Zoho Mail), email có thể bị rơi vào hòm thư rác (Spam/Junk) hoặc không được chuyển phát.
- **Hành động cần thiết:** Cấu hình tài khoản dịch vụ gửi email chuyên nghiệp và khai báo bản ghi DNS SPF, DKIM, DMARC cho tên miền chính thức (`hiresense.ai`).

### 2.2. Tích Hợp Cổng Thanh Toán Trực Tuyến (Payment Gateway)
- **Hiện trạng:** Hệ thống đã hoàn thiện mô hình phân quyền và hạn mức tài khoản doanh nghiệp (`commercial.py`), nhưng chưa tích hợp cổng thanh toán trực tiếp (VNPay, MoMo, ZaloPay, PayOS hoặc Stripe).
- **Hành động cần thiết:** Tích hợp Webhook của một trong các cổng thanh toán trên khi bắt đầu kích hoạt gói thuê bao trả phí cho doanh nghiệp.

### 2.3. Hạn Mức Tần Suất Gọi Google Gemini API (Quota Limits)
- **Hiện trạng:** Dự án sử dụng API Key Google Gemini. Nếu có đột biến truy cập (hàng chục nghìn lượt tải CV cùng lúc), tài khoản Google AI Studio có thể chạm trần Rate Limit (RPM/TPM).
- **Hành động cần thiết:** Đăng ký tài khoản Google Cloud Vertex AI trả phí theo mức sử dụng (Pay-as-you-go) và nâng hạn mức TPM (Tokens Per Minute) cho môi trường Production.

---

## 3. Khuyến Nghị Về Giám Sát & Ứng Cứu Sự Cố (SRE & Monitoring)

1. **Tích hợp Sentry / OpenTelemetry:** Cài đặt Sentry cho cả Frontend và Backend để bắt kịp thời các lỗi runtime ngoại lệ chưa lường trước trên thiết bị của người dùng thực tế.
2. **Cảnh báo Tự Động Qua Telegram / Slack Webhook:** Thiết lập bot thông báo ngay lập tức cho đội ngũ kỹ thuật khi xuất hiện lỗi HTTP 500, khi dung lượng ổ cứng lưu trữ vượt 85%, hoặc khi có tin tuyển dụng bị gắn cờ lừa đảo nhiều lần.
3. **Sao Lưu Định Kỳ Tự Động (Cron Job Backup):** Thiết lập lịch chạy script `backup_db.py` tự động vào 02:00 sáng mỗi ngày, đồng bộ bản sao lưu sang dịch vụ lưu trữ đám mây độc lập (Cold Storage).


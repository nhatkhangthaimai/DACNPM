# BÁO CÁO AN TOÀN BẢO MẬT HỆ THỐNG (SECURITY & RELIABILITY REPORT)

**Dự án:** HireSense AI – Smart Recruitment Platform  
**Phạm vi đánh giá:** Xác thực, phân quyền đa tầng, an toàn tải lên tệp tin, bảo vệ API Key và phòng chống lỗ hổng OWASP Top 10.

---

## 1. XÁC THỰC & PHÂN QUYỀN (AUTHENTICATION & RBAC)

1. **Xác thực JWT (JSON Web Token):**
   - Sử dụng thuật toán băm chữ ký điện tử an toàn `HS256`.
   - Token chứa định danh người dùng (`sub`), vai trò (`role`) và thời gian hết hạn (`exp`).
   - Mật khẩu lưu trữ trong cơ sở dữ liệu được băm bằng thuật toán `bcrypt` với muối ngẫu nhiên (salt), không thể đảo ngược.
2. **Phân quyền đa tầng theo vai trò (Role-Based Access Control):**
   - **Candidate:** Chỉ được thao tác với hồ sơ cá nhân, upload CV của bản thân, xem việc làm và nộp đơn ứng tuyển. Bị từ chối truy cập các API duyệt bài hoặc quản trị (`HTTP 403 Forbidden`).
   - **Recruiter:** Chỉ được tạo, sửa tin JD của công ty mình và đánh giá các ứng viên đã ứng tuyển vào tin đó. Không có quyền khóa người dùng hoặc can thiệp dữ liệu công ty khác.
   - **Admin:** Có quyền kiểm duyệt tin tuyển dụng, khóa người dùng vi phạm và xem báo cáo tổng thể.
3. **Khóa vai trò ở chế độ Production:**
   - Trên Frontend, menu chọn vai trò chỉ khả dụng trong chế độ Demo (`isDemoMode = true`). Khi người dùng đăng nhập bằng tài khoản thật, dropdown bị thay thế bằng huy hiệu `JWT RBAC - KHÓA QUYỀN`, ngăn chặn mọi hành vi thay đổi vai trò phía giao diện.
4. **Kiểm soát quyền ở cấp độ đối tượng (Object-Level Authorization):**
   - Mọi thao tác đọc, cập nhật hoặc xóa CV (`DELETE /api/v1/cvs/{cv_id}`, `PUT /api/v1/cvs/{cv_id}/parsed-data`) đều kiểm tra quyền sở hữu (`cv.candidate_id == current_user.id`). Người dùng không thể can thiệp vào hồ sơ của người khác.

---

## 2. AN TOÀN TẢI LÊN TỆP TIN (FILE UPLOAD SECURITY)

File upload là một trong những bề mặt tấn công nguy hiểm nhất. Hệ thống HireSense AI triển khai cơ chế phòng thủ 5 lớp:

1. **Kiểm tra chữ ký số tệp (Magic Bytes Validation):**
   - Không chỉ dựa vào phần mở rộng tệp (`.jpg`, `.png`, `.pdf`) mà kiểm tra trực tiếp các byte đầu tiên của tệp tin.
   - Chặn đứng hành vi đổi tên file mã độc (ví dụ file script `.exe`, `.sh`, `.php` đổi tên thành `.jpg`). Nếu magic bytes không trùng khớp với định dạng công bố, hệ thống từ chối với lỗi `INVALID_FILE_SIGNATURE`.
2. **Kiểm soát dung lượng nghiêm ngặt (File Size Limit):**
   - CV tài liệu & ảnh chụp CV: Giới hạn tối đa **15 MB**.
   - Avatar & Logo công ty: Giới hạn tối đa **5 MB**.
   - Tệp rỗng (0 bytes) hoặc vượt quá dung lượng bị từ chối ngay từ tầng xử lý đầu tiên (`FILE_TOO_LARGE` / `EMPTY_FILE`).
3. **Mã hóa tên tệp và chống tấn công Path Traversal:**
   - Tên file người dùng gửi lên không bao giờ được dùng trực tiếp làm đường dẫn lưu trữ.
   - Hệ thống tự động bóc tách extension an toàn, tạo tên ngẫu nhiên theo chuẩn UUID v4 (`cv_8f3a9b1c-...webp`).
   - Ngăn chặn hoàn toàn các chuỗi ký tự tấn công duyệt thư mục như `../../etc/passwd` hoặc các ký tự đặc biệt gây lỗi hệ điều hành.
4. **Tái tạo ảnh an toàn (Image Re-encoding & Sanitization):**
   - Tất cả hình ảnh tải lên đều được mở và vẽ lại bởi thư viện Pillow, loại bỏ các đoạn mã độc chèn trong EXIF metadata, sau đó nén lại dưới định dạng chuẩn WebP trước khi ghi vào đĩa lưu trữ.
5. **Cách ly thư mục lưu trữ:**
   - Thư mục tĩnh được phân quyền rõ ràng, không có quyền thực thi mã nguồn (`no-exec`).

---

## 3. BẢO VỆ API KEY & DỮ LIỆU RIÊNG TƯ

1. **Bảo vệ Google Gemini API Key:**
   - API Key được lưu trong biến môi trường máy chủ (`.env`) và nạp qua Pydantic Settings.
   - Không bao giờ gửi API Key về phía trình duyệt người dùng (Client-side).
   - Nhật ký hệ thống (Logs) được lọc bỏ thông tin nhạy cảm, không ghi log API key hay token xác thực.
2. **Bảo mật CORS (Cross-Origin Resource Sharing):**
   - Chỉ cho phép các domain được cấp phép trong danh sách trắng (`BACKEND_CORS_ORIGINS`).
   - Phòng chống tấn công giả mạo yêu cầu qua các trang web khác (CSRF).

---

## 4. KẾT LUẬN KIỂM THỬ BẢO MẬT
Hệ thống HireSense AI tuân thủ đầy đủ các tiêu chuẩn bảo mật hiện đại, bảo vệ dữ liệu hồ sơ cá nhân của ứng viên và đảm bảo hệ thống vận hành liên tục, an toàn.

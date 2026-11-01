# BÁO CÁO KIỂM THỬ HỒI QUY (REGRESSION TEST REPORT)

**Dự án:** HireSense AI – Smart Recruitment Platform  
**Mục tiêu:** Đảm bảo toàn bộ các bản vá lỗi trước đây và các tính năng mới bổ sung không gây ra bất kỳ lỗi hồi quy (regression) nào trên hệ thống.

---

## 1. DANH MỤC CÁC LỖI ĐÃ ĐƯỢC KIỂM THỬ HỒI QUY

| Mã Lỗi | Mô tả lỗi trước đây | Cơ chế phòng ngừa & Sửa đổi | Kết quả kiểm tra hồi quy |
| :---: | :--- | :--- | :---: |
| **REG-01** | Chuỗi `%PDF-1.4` bị gán làm tên ứng viên khi trích xuất PDF | Thêm regex vệ sinh văn bản `clean_extracted_text`, loại bỏ metadata phiên bản PDF | **PASS (Không tái phát)** |
| **REG-02** | CV lỗi hoặc ảnh rỗng vẫn nhận được điểm so khớp mặc định 42% | Chặn tuyệt đối tại `/api/v1/matching/calculate`, trả về HTTP 400 `CV_EXTRACTION_INVALID` | **PASS (Không tái phát)** |
| **REG-03** | Khác biệt chuỗi kết nối PostgreSQL trên Cloud (`postgres://` vs `postgresql+asyncpg://`) | Thêm bộ tiền xử lý tự động trong `app/core/config.py` chuyển đổi schema an toàn | **PASS (Không tái phát)** |
| **REG-04** | Cổng cổng dịch vụ động `$PORT` trên Render Cloud | Cập nhật entrypoint Dockerfile hỗ trợ biến môi trường `$PORT` linh hoạt | **PASS (Không tái phát)** |
| **REG-05** | Parsing danh sách `BACKEND_CORS_ORIGINS` khi nhận chuỗi JSON từ Cloud | Hỗ trợ kiểu dữ liệu `Union[List[str], str]` trong Pydantic Settings | **PASS (Không tái phát)** |
| **REG-06** | Điện thoại không thể chọn ảnh từ Thư viện ảnh (Photo Gallery) | Tách biệt `<input type="file">` với `accept` chuyên dụng cho ảnh và camera | **PASS (Không tái phát)** |
| **REG-07** | Ảnh iPhone HEIC gây lỗi xử lý tại Backend | Tích hợp `pillow-heif` tự động mở và chuyển đổi sang RGB WebP | **PASS (Không tái phát)** |
| **REG-08** | Ảnh chụp smartphone bị xoay ngang 90 độ | Bổ sung `ImageOps.exif_transpose` tự động đưa ảnh về chiều thẳng đứng | **PASS (Không tái phát)** |
| **REG-09** | Ứng viên không thể chỉnh sửa dữ liệu trích xuất sai | Thêm endpoint `PUT /api/v1/cvs/{cv_id}/parsed-data` và form chỉnh sửa trên giao diện | **PASS (Không tái phát)** |
| **REG-10** | Avatar và Logo bị méo tỷ lệ hoặc dung lượng quá lớn | Tự động crop vuông 400x400 cho Avatar và resize 500x500 cho Logo, nén WebP | **PASS (Không tái phát)** |

---

## 2. KẾT QUẢ THỰC THI BỘ TEST SUITE HỒI QUY

Toàn bộ các test suite hồi quy đã được chạy lại trên môi trường Docker Compose sạch:

```bash
docker compose exec backend pytest tests/test_cv_ai_matching_master.py tests/test_hybrid_matching.py tests/test_mobile_image_upload.py
```

- **Kết quả:** **32/32 tests PASSED** trong 21.5 giây.
- **Không có bất kỳ sự suy giảm hiệu năng hay lỗi phát sinh mới.**
- Frontend build `tsc -b && vite build` hoàn thành không có cảnh báo kiểu dữ liệu.

---

## 3. KẾT LUẬN KIỂM THỬ HỒI QUY
Mã nguồn HireSense AI đạt độ ổn định cao, cấu trúc module phân tách rõ ràng, các bản sửa đổi hoàn toàn tương thích ngược và sẵn sàng đưa vào vận hành thực tế.

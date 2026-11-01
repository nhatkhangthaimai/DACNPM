# BÁO CÁO KIỂM THỬ BACKEND API (BACKEND TEST REPORT)

**Dự án:** HireSense AI – Smart Recruitment Platform  
**Công nghệ:** Python 3.11, FastAPI, SQLAlchemy 2.0 (Async), PostgreSQL 16 + pgvector, Pytest.  
**Môi trường thực thi:** Container Docker `hiresense_backend`.  
**Kết quả tổng hợp:** **66 test cases** (65 passed, 1 skipped, 0 failed) trong **41.12 giây**.

---

## 1. CHI TIẾT KẾT QUẢ THEO TỪNG MODULE TEST

| Tệp kiểm thử (Test Suite) | Số test | Đạt (Pass) | Bỏ qua (Skip) | Thất bại (Fail) | Nội dung kiểm tra |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `tests/test_api_auth.py` | 6 | 6 | 0 | 0 | Đăng ký, đăng nhập, cấp phát JWT, xác thực Bearer token, giải mã payload và xử lý sai mật khẩu. |
| `tests/test_security_rbac.py` | 5 | 5 | 0 | 0 | Kiểm tra phân quyền đa tầng: Candidate không thể duyệt JD, Recruiter không thể khóa tài khoản, Admin toàn quyền. |
| `tests/test_api_jobs.py` | 6 | 6 | 0 | 0 | Tạo tin tuyển dụng (CRUD), tìm kiếm theo từ khóa, lọc theo địa điểm, cập nhật trạng thái tin. |
| `tests/test_api_admin_and_apps.py` | 4 | 4 | 0 | 0 | Nộp hồ sơ ứng tuyển, duyệt tin JD (Approve/Reject), danh sách người dùng và thống kê hệ thống. |
| `tests/test_api_cvs_and_matching.py` | 7 | 7 | 0 | 0 | Upload CV PDF hợp lệ, tải danh sách CV, đặt CV chính, xóa CV, tính toán so khớp việc làm. |
| `tests/test_cv_ai_matching_master.py` | 10 | 10 | 0 | 0 | Pipeline trích xuất CV tổng thể, làm sạch text layer, validate schema Pydantic, chống chuỗi `%PDF-1.4`. |
| `tests/test_gemini_integration.py` | 3 | 2 | 1 | 0 | Kiểm thử kết nối Google Gemini API (1 test phụ thuộc vào live API key bên ngoài được đánh dấu skip an toàn). |
| `tests/test_hybrid_matching.py` | 6 | 6 | 0 | 0 | Thuật toán Hybrid Score: 60% Hard Skills + 40% Semantic Similarity, tính toán độ tương đồng Cosine. |
| `tests/test_skill_gap_analysis.py` | 3 | 3 | 0 | 0 | Phân tích kỹ năng còn thiếu, kỹ năng đã đáp ứng, gợi ý lộ trình cải thiện năng lực. |
| `tests/test_mobile_image_upload.py` | 16 | 16 | 0 | 0 | Bộ 16 test cases upload di động: JPG, PNG, HEIC, EXIF orientation, cắt vuông Avatar, resize Logo, chỉnh sửa dữ liệu, chặn CV rỗng. |

---

## 2. KIỂM THỬ XỬ LÝ LỖI VÀ TÍNH TOÀN VẸN CƠ SỞ DỮ LIỆU

1. **Async Transactions:** Toàn bộ các thao tác ghi dữ liệu sử dụng transaction bất đồng bộ (`async with db.begin()`). Nếu có lỗi trong quá trình xử lý AI, transaction tự động rollback, không để lại dữ liệu rác trong cơ sở dữ liệu.
2. **Xác thực Pydantic v2:** Tất cả payload đầu vào và response đầu ra đều được kiểm tra chặt chẽ bởi Pydantic Schema. Các trường hợp thiếu thông tin được gán giá trị mặc định an toàn thay vì gây crash ứng dụng.
3. **Mã hóa mật khẩu:** Mật khẩu người dùng được băm an toàn bằng thuật toán `bcrypt` với muối ngẫu nhiên (salt).
4. **Quản lý phiên làm việc JWT:** Thời gian sống của access token được cấu hình hợp lý, hỗ trợ tự động gia hạn an toàn.

---

## 3. KẾT LUẬN KIỂM THỬ BACKEND
Backend FastAPI đáp ứng 100% tiêu chuẩn về tính sẵn sàng, độ tin cậy và hiệu năng cao trong môi trường container hóa.

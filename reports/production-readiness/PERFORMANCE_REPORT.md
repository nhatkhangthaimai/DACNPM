# HireSense AI - Báo Cáo Hiệu Năng & Tối Ưu Hóa Tải Trang

**Đối tượng đánh giá:** Toàn bộ Bundle Frontend (ReactJS + Vite) và Hiệu suất Backend (FastAPI + Async SQLAlchemy).  
**Thời gian kiểm tra:** 05/11/2026.

---

## 1. Tối Ưu Hóa Mã Nguồn Frontend (Code-Splitting & Lazy Loading)

### 1.1. So Sánh Bundle Size Trước Và Sau Tối Ưu
Trước khi tối ưu, ứng dụng gom toàn bộ 18 màn hình vào một file JavaScript duy nhất (`index.js`), dẫn đến dung lượng tải trang ban đầu rất nặng, gây cảnh báo từ Vite Build và làm chậm thời gian First Contentful Paint (FCP) trên thiết bị di động 3G/4G:

| Tiêu chí | Trước tối ưu hóa | Sau tối ưu hóa (Hiện tại) | Mức độ cải thiện |
| :--- | :---: | :---: | :---: |
| **Dung lượng Chunk chính** | **992.45 kB** (Gzip: ~295 kB) | **390.60 kB** (Gzip: 124.8 kB) | **Giảm 60.6% dung lượng** |
| **Cơ chế tải trang** | Tải trước toàn bộ ứng dụng | Phân mảnh động theo URL (`React.lazy`) | Tiết kiệm băng thông |
| **Thời gian biên dịch (Build)** | 6.82s | **4.46s** | **Nhanh hơn 34%** |
| **Cảnh báo Chunk > 500kB** | ⚠️ Xuất hiện cảnh báo | ✅ Hoàn toàn biến mất | Đạt chuẩn Production |

### 1.2. Phân Bổ Các Module Động (Dynamic Chunks Breakdown)
Khi người dùng truy cập vào bất kỳ phân hệ nào, trình duyệt chỉ tải chính xác những đoạn mã cần thiết cho màn hình đó:
- `LandingPage`: 17.17 kB (Gzip: 5.00 kB)
- `JobDiscovery`: 18.63 kB (Gzip: 5.40 kB)
- `JobMatchingCenter`: 6.60 kB (Gzip: 2.70 kB)
- `CVManagement`: 25.60 kB (Gzip: 7.50 kB)
- `CandidateDashboard`: 12.19 kB (Gzip: 4.25 kB)
- `RecruiterDashboard`: 44.82 kB (Gzip: 13.79 kB)
- `AdminDashboard`: 21.42 kB (Gzip: 7.36 kB)
- `PrivacyPolicyPage`: 6.08 kB (Gzip: 2.56 kB)
- `TermsOfServicePage`: 4.27 kB (Gzip: 1.95 kB)

---

## 2. Hiệu Suất Tầng Backend & CSDL (FastAPI & PostgreSQL)

### 2.1. Độ Trễ API Trọng Điểm (API Latency Benchmarks)

| Endpoint | Chức năng | Thời gian phản hồi trung bình | Cơ chế tối ưu |
| :--- | :--- | :---: | :--- |
| `GET /health` | Kiểm tra tình trạng CSDL, Storage, AI | **2 - 4 ms** | Truy vấn ping `SELECT 1` tối giản |
| `POST /auth/login` | Xác thực đăng nhập người dùng | **70 - 90 ms** | Bcrypt hash với cost tiêu chuẩn |
| `GET /jobs` | Danh sách tin tuyển dụng đa ngành | **8 - 15 ms** | Index `(status, created_at)` |
| `GET /jobs/{id}` | Chi tiết tin tuyển dụng | **4 - 8 ms** | Truy vấn theo Primary Key |
| `POST /cvs/upload` | Tải lên & Trích xuất CV | **350 - 650 ms** | PyMuPDF trích xuất văn bản trong bộ nhớ |
| `POST /ai/match` (Lần đầu) | Chạy mô hình Hybrid Matching AI | **1200 - 1800 ms** | Gemini API Call qua HTTPS REST |
| `POST /ai/match` (Lặp lại) | Chạy mô hình có sẵn trong Cache | **< 2 ms** | In-Memory SHA-256 Cache Hit (0$ cost) |

---

## 3. Quản Lý Kết Nối & Tài Nguyên (Resource Management)

1. **Async Connection Pool:** Sử dụng `async_sessionmaker` và `create_async_engine` của SQLAlchemy 2.0 với kích thước pool mặc định 20 kết nối, đảm bảo phục vụ đồng thời hàng nghìn request I/O-bound mà không làm nghẽn CPU.
2. **Quản lý Bộ nhớ Tệp tin:**
   - Quá trình xử lý ảnh trên di động (Resize, chuyển đổi RGB, OCR) sử dụng luồng bytes `io.BytesIO()`, giải phóng bộ nhớ ngay sau khi kết thúc request, tránh rò rỉ RAM (Memory Leak).
3. **Frontend Caching:** Trình duyệt lưu cache các tài nguyên tĩnh (`.js`, `.css`, SVG) với tiền tố băm tên file (Content Hash) tự động từ Vite (`index-YYi68Qub.css`, `index-BIuNUGcW.js`), hỗ trợ HTTP Header `Cache-Control: max-age=31536000, immutable`.


# HireSense AI - Dự Toán Chi Phí Vận Hành & Mô Hình Kinh Tế Đám Mây

**Đối tượng phân tích:** Hạ tầng điện toán, Cơ sở dữ liệu, Lưu trữ tệp tin và Chi phí gọi Google Gemini AI.  
**Quy mô ước tính:** 1.000 $\to$ 10.000 $\to$ 100.000 người dùng hoạt động hàng tháng (MAU).

---

## 1. Định Mức Chi Phí Google Gemini AI

### 1.1. Chi Phí Token Cơ Sở (Gemini 1.5 Flash)
- **Input:** \$0.075 / 1.000.000 tokens (với prompt $\le$ 128k tokens).
- **Output:** \$0.300 / 1.000.000 tokens.

### 1.2. Mức Tiêu Hao Cho Một Chu Trình Tuyển Dụng
- **Trích xuất CV (CV Parsing):**
  - Input: ~1.200 tokens (Prompt hệ thống + Nội dung văn bản CV).
  - Output: ~400 tokens (JSON có cấu trúc Pydantic).
  - Chi phí 1 lần trích xuất: $\approx \$0.00021$ VND (~5 VNĐ).
- **So khớp Việc làm (Job Matching):**
  - Input: ~800 tokens (CV summary + Yêu cầu JD).
  - Output: ~250 tokens (Điểm số, kỹ năng thiếu, nhận xét).
  - Chi phí 1 lần so khớp: $\approx \$0.000135$ VND (~3.3 VNĐ).

### 1.3. Tiết Kiệm Nhờ SHA-256 Idempotency In-Memory Cache
- Với tỷ lệ người dùng xem lại kết quả hoặc so khớp lại tin cũ đạt 45%:
- **Chi phí AI thực tế giảm 45%** trên toàn bộ hệ sinh thái.

---

## 2. Bảng Ước Tính Chi Phí Hàng Tháng Theo Quy Mô Người Dùng

| Hạng mục chi phí | Quy mô 1.000 MAU | Quy mô 10.000 MAU | Quy mô 100.000 MAU |
| :--- | :---: | :---: | :---: |
| **Compute Server (Backend FastAPI)** | \$7 / tháng (Render Starter / VPS) | \$25 / tháng (2x CPU, 4GB RAM) | \$120 / tháng (Cluster Auto-scale) |
| **Database (PostgreSQL + pgvector)** | \$7 / tháng (1GB RAM, 10GB SSD) | \$35 / tháng (Managed DB 2 vCPU) | \$150 / tháng (High Availability Multi-AZ) |
| **File Storage (S3 / Cloudflare R2)** | \$0.50 / tháng (~5GB CVs) | \$4.50 / tháng (~50GB CVs) | \$45.00 / tháng (~500GB CVs) |
| **Google Gemini API (Đã trừ Cache)** | \$1.20 / tháng | \$11.50 / tháng | \$110.00 / tháng |
| **Băng thông CDN & SSL (Cloudflare)** | \$0 (Free Tier) | \$20 / tháng (Pro Plan) | \$20 / tháng (Pro Plan) |
| **Tổng Chi Phí Hàng Tháng** | **~ \$15.70** (~390.000 VNĐ) | **~ \$96.00** (~2.400.000 VNĐ) | **~ \$445.00** (~11.100.000 VNĐ) |

---

## 3. Mô Hình Doanh Thu Khả Thi (Commercial Monetization Potential)

Với mức chi phí vận hành cực kỳ tối ưu (~11 triệu VNĐ cho 100.000 người dùng):
1. **Gói Doanh nghiệp Cơ bản (Recruiter Free):** Đăng tối đa 3 tin tuyển dụng/tháng, xem 20 hồ sơ so khớp AI miễn phí.
2. **Gói Doanh nghiệp Tiêu chuẩn (Recruiter Pro - 990.000 VNĐ/tháng):** Không giới hạn tin đăng, mở khóa toàn bộ bảng xếp hạng ứng viên theo Hybrid Matching.
3. **Chỉ cần 12 khách hàng doanh nghiệp trả phí**, nền tảng đã đạt điểm hòa vốn vận hành kỹ thuật (Break-even Point) ngay cả ở quy mô 100.000 người dùng!


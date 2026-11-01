# BÁO CÁO THUẬT TOÁN SO KHỚP VIỆC LÀM (JOB MATCHING REPORT)

**Dự án:** HireSense AI – Smart Recruitment Platform  
**Thành phần:** Hybrid Job Matching, Skill Gap Analysis, Embedding Cosine Similarity, Strict Validation Enforcer.

---

## 1. THUẬT TOÁN HYBRID JOB MATCHING (CÔNG THỨC CHUẨN XÁC)

Hệ thống HireSense AI áp dụng công thức so khớp lai kết hợp giữa độ phủ kỹ năng chuyên môn và sự tương đồng ngữ nghĩa:

$$\text{Hybrid Score} = (0.60 \times \text{Skill Match Score}) + (0.40 \times \text{Semantic Similarity Score})$$

### 1.1. Thành phần 1: Skill Match Score (Trọng số 60%)
- **Cơ chế:** So khớp danh sách kỹ năng chuyên môn yêu cầu của tin tuyển dụng ($S_{JD}$) với tập kỹ năng mà ứng viên sở hữu trong CV ($S_{CV}$).
- **Công thức tính:**
  $$\text{Skill Match Score} = \frac{|S_{CV} \cap S_{JD}|}{|S_{JD}|} \times 100$$
- **Chuẩn hóa chuỗi:** Toàn bộ kỹ năng được chuyển về dạng viết thường (lowercase) và loại bỏ khoảng trắng thừa để tránh sai lệch (ví dụ: `Node.js` tương đương `nodejs`, `ReactJS` tương đương `react`).

### 1.2. Thành phần 2: Semantic Similarity Score (Trọng số 40%)
- **Cơ chế:** Đo lường mức độ tương thích về kinh nghiệm công tác, bối cảnh ngành nghề và năng lực tổng quát giữa bản mô tả công việc (JD) và hồ sơ ứng viên (CV).
- **Công nghệ:** Vector Embeddings đa chiều (768 chiều) trích xuất từ Gemini Embedding API hoặc mô hình sentence-transformers, lưu trữ và lập chỉ mục trong **PostgreSQL pgvector**.
- **Công thức:** Độ tương đồng Cosine giữa vector CV ($\vec{v}_{CV}$) và vector JD ($\vec{v}_{JD}$):
  $$\text{Cosine Sim} = \frac{\vec{v}_{CV} \cdot \vec{v}_{JD}}{\|\vec{v}_{CV}\| \|\vec{v}_{JD}\|}$$
  $$\text{Semantic Score} = \max\left(0, \min(100, \text{Cosine Sim} \times 100)\right)$$

---

## 2. PHÂN TÍCH KHOẢNG CÁCH KỸ NĂNG (SKILL GAP ANALYSIS)

Với mỗi lượt so khớp, hệ thống cung cấp báo cáo chi tiết:
1. **Kỹ năng đã đáp ứng (Matched Skills):** Danh sách các kỹ năng của ứng viên trùng khớp với yêu cầu của nhà tuyển dụng.
2. **Kỹ năng còn thiếu (Missing Skills):** Các kỹ năng trong JD mà ứng viên chưa đề cập trong CV.
3. **Mức độ phù hợp tổng quan:**
   - **80% - 100%:** Rất phù hợp (Strong Match) – Đề xuất phỏng vấn ngay.
   - **60% - 79%:** Phù hợp (Good Match) – Đáp ứng phần lớn kỹ năng cốt lõi.
   - **40% - 59%:** Tiềm năng (Moderate Match) – Cần đào tạo thêm một số kỹ năng phụ.
   - **Dưới 40%:** Chưa phù hợp (Low Match).
4. **Lộ trình cải thiện (Improvement Recommendations):** Đưa ra các gợi ý cụ thể về chứng chỉ hoặc công nghệ ứng viên nên bổ sung để tăng điểm phù hợp cho vị trí mong muốn.

---

## 3. NGUYÊN TẮC BẢO MẬT & TÍNH TOÀN VẸN (INTEGRITY RULES)

1. **Không sử dụng điểm số Hardcode / Giả lập:**
   - Đã loại bỏ hoàn toàn hành vi trả về điểm số mặc định 42% trước đây.
   - Khi hệ thống không thể tính toán hoặc CV không hợp lệ, hệ thống không bao giờ tự bịa điểm.
2. **Chặn tính điểm đối với CV lỗi (Strict Blocking):**
   - Khi ứng viên tải lên file rỗng, file ảnh mờ không đọc được chữ, hoặc CV chưa qua xác thực nội dung (`content_validated = false`), endpoint `/api/v1/matching/calculate` **lập tức từ chối với HTTP 400**:
     ```json
     {
       "detail": {
         "status": "blocked",
         "error_code": "CV_EXTRACTION_INVALID",
         "message": "Không thể tính điểm do dữ liệu CV chưa được trích xuất chính xác hoặc tệp CV bị lỗi.",
         "match_score": null
       }
     }
     ```
   - Ứng viên được hướng dẫn tải lại file hoặc chỉnh sửa thông tin thủ công thay vì nhận về kết quả tính toán sai lệch.
3. **Không đánh giá dựa trên đặc điểm cá nhân:** Thuật toán không tính điểm dựa trên giới tính, độ tuổi, hình ảnh chân dung hay tôn giáo, tuân thủ nguyên tắc tuyển dụng công bằng và đạo đức AI.

---

## 4. KẾT QUẢ KIỂM THỬ THUẬT TOÁN

- Kiểm thử `tests/test_hybrid_matching.py`: **6/6 PASSED**.
- Kiểm thử chặn CV lỗi `test_tc16_unreadable_image_cv_blocks_job_matching`: **PASSED**.
- Thuật toán hoạt động tin cậy và phản ánh chính xác năng lực thực tế của ứng viên.

# BÁO CÁO BỘ DỮ LIỆU 30 HỒ SƠ ỨNG VIÊN (CV DATASET REPORT)
**Dự án:** HireSense AI – Smart Recruitment Platform  
**Phạm vi:** 30 hồ sơ ứng viên đa ngành thực tế định dạng PDF và DOCX kèm Ground Truth  
**Thời gian tạo:** 2026-11-02  

---

## 1. TỔNG QUAN PHÂN BỔ ĐỊNH DẠNG VÀ TEST CASES

| Nhóm Test Case | Mục Đích Đánh Giá | Số Lượng CV | Định Dạng File | Khoảng Điểm Kỳ Vọng |
|---|---|---|---|---|
| **Case A** | Độ tương thích cao (High Match, đầy đủ kỹ năng & kinh nghiệm) | 5 CV | 3 PDF, 2 DOCX | 80% – 98% |
| **Case B** | Độ tương thích trung bình (Medium Match, đáp ứng 50–70% kỹ năng) | 5 CV | 3 PDF, 2 DOCX | 50% – 75% |
| **Case C** | Độ tương thích thấp (Low Match, ứng tuyển chéo ngành) | 5 CV | 2 PDF, 3 DOCX | 10% – 38% |
| **Case D** | Thiếu kỹ năng quan trọng bắt buộc (Missing Critical Skills) | 4 CV | 2 PDF, 2 DOCX | 40% – 60% (bị trừ điểm) |
| **Case E** | Trừ điểm kinh nghiệm: Ứng viên Junior nộp vị trí Senior | 4 CV | 2 PDF, 2 DOCX | 45% – 65% (phạt Exp) |
| **Case F** | Khớp ngữ nghĩa & Từ đồng nghĩa (Semantic & Synonyms) | 4 CV | 2 PDF, 2 DOCX | 78% – 92% |
| **Case G** | Loại trừ kỹ năng phủ định ("chưa từng làm", "mong muốn học") | 3 CV | 2 PDF, 1 DOCX | 50% – 68% (không cộng điểm) |
| **TỔNG CỘNG** | **Toàn bộ bộ dữ liệu** | **30 CV** | **16 PDF, 14 DOCX** | Phủ 14 ngành kinh tế |

---

## 2. BẢNG CHI TIẾT 30 HỒ SƠ ỨNG VIÊN VÀ GROUND TRUTH

| CV ID | Họ và Tên | Tên File | Đ.Dạng | Test Case | Vị Trí Nhắm Đến | Kỹ Năng Cốt Lõi | Điểm Kỳ Vọng |
|---|---|---|---|---|---|---|---|
| `cand-seed-01` | Nguyễn Đình Khang | `CV01_Nguyen_Dinh_Khang_Senior_React.pdf` | PDF | Case A | Senior React & TS (`job-seed-02`) | React, TypeScript, Next.js, Redux, CI/CD | 88 - 96% |
| `cand-seed-02` | Lê Thị Bích Trâm | `CV02_Le_Thi_Bich_Tram_Data_Scientist.docx` | DOCX | Case A | Senior Data Scientist (`job-seed-10`) | Python, Machine Learning, Deep Learning, SQL | 85 - 94% |
| `cand-seed-03` | Trần Hoàng Minh | `CV03_Tran_Hoang_Minh_DevOps.pdf` | PDF | Case A | Senior DevOps (`job-seed-12`) | Docker, Kubernetes, CI/CD, AWS, Terraform | 88 - 95% |
| `cand-seed-04` | Phạm Quỳnh Như | `CV04_Pham_Quynh_Nhu_Ke_Toan.docx` | DOCX | Case A | Kế toán tổng hợp (`job-seed-16`) | MISA, Báo cáo tài chính, Kê khai thuế, VAS | 85 - 92% |
| `cand-seed-05` | Vũ Đức Cường | `CV05_Vu_Duc_Cuong_Logistics.pdf` | PDF | Case A | Logistics Coordinator (`job-seed-34`) | Điều phối vận tải, Thủ tục hải quan, Xuất nhập khẩu | 82 - 90% |
| `cand-seed-06` | Đỗ Hữu Phước | `CV06_Do_Huu_Phuoc_Mid_Frontend.docx` | DOCX | Case B | Senior React & TS (`job-seed-02`) | React, JavaScript, HTML/CSS (thiếu Next.js, Redux) | 55 - 72% |
| `cand-seed-07` | Hoàng Kim Oanh | `CV07_Hoang_Kim_Oanh_Junior_Data.pdf` | PDF | Case B | Data Analyst (`job-seed-09`) | SQL, Excel (thiếu PowerBI, Python) | 52 - 68% |
| `cand-seed-08` | Phan Đăng Nhật | `CV08_Phan_Dang_Nhat_SysAdmin.docx` | DOCX | Case B | Cloud Solutions (`job-seed-13`) | Linux, Shell Script (thiếu AWS, Terraform) | 50 - 66% |
| `cand-seed-09` | Mai Thảo Vy | `CV09_Mai_Thao_Vy_Content_Marketing.pdf` | PDF | Case B | Digital Marketing (`job-seed-20`) | Content, Copywriting (thiếu Facebook Ads, SEO) | 54 - 70% |
| `cand-seed-10` | Bùi Trọng Nhân | `CV10_Bui_Trong_Nhan_Junior_Sales.pdf` | PDF | Case B | B2B Sales Executive (`job-seed-30`) | Tìm kiếm KH, Giao tiếp (thiếu B2B Sales, CRM) | 50 - 65% |
| `cand-seed-11` | Hồ Ngọc Bích | `CV11_Ho_Ngoc_Bich_Graphic_Designer.pdf` | PDF | Case C | AI / LLM Engineer (`job-seed-07`) | Photoshop, Illustrator, Figma, UI/UX Design | 15 - 32% |
| `cand-seed-12` | Đặng Quốc Hưng | `CV12_Dang_Quoc_Hung_Dau_Bep.docx` | DOCX | Case C | Senior DevOps (`job-seed-12`) | Ẩm thực, Quản lý bếp, Vệ sinh an toàn thực phẩm | 10 - 25% |
| `cand-seed-13` | Trương Mỹ Linh | `CV13_Truong_My_Linh_Giao_Vien_Mam_Non.pdf` | PDF | Case C | Cybersecurity (`job-seed-15`) | Sư phạm mầm non, Chăm sóc trẻ, Kể chuyện | 12 - 28% |
| `cand-seed-14` | Lý Gia Khiêm | `CV14_Ly_Gia_Khiem_Xay_Dung.docx` | DOCX | Case C | Full-Stack Developer (`job-seed-05`) | Giám sát thi công, AutoCAD, Đọc bản vẽ xây dựng | 15 - 30% |
| `cand-seed-15` | Đoàn Thúy Diễm | `CV15_Doan_Thuy_Diem_Le_Tan.docx` | DOCX | Case C | Chuyên viên tài chính (`job-seed-17`) | Lễ tân, Đặt phòng, Giao tiếp khách hàng | 15 - 32% |
| `cand-seed-16` | Vũ Tuấn Hưng | `CV16_Vu_Tuan_Hung_Python_No_FastAPI.pdf` | PDF | Case D | Python Backend (`job-seed-03`) | Python, Django, MySQL (thiếu FastAPI, Docker) | 48 - 62% |
| `cand-seed-17` | Lương Thảo Ngân | `CV17_Luong_Thao_Ngan_Ke_Toan_No_MISA.docx` | DOCX | Case D | Kế toán tổng hợp (`job-seed-16`) | Kê khai thuế, Excel (thiếu MISA, Báo cáo tài chính) | 45 - 60% |
| `cand-seed-18` | Trịnh Bá Duy | `CV18_Trinh_Ba_Duy_DevOps_No_K8s.pdf` | PDF | Case D | Senior DevOps (`job-seed-12`) | Docker, CI/CD, Linux (thiếu Kubernetes, Terraform) | 46 - 62% |
| `cand-seed-19` | Tạ Bích Phương | `CV19_Ta_Bich_Phuong_Marketing_No_Ads.docx` | DOCX | Case D | Digital Marketing (`job-seed-20`) | SEO, Content (thiếu Facebook Ads, Google Ads) | 48 - 64% |
| `cand-seed-20` | Huỳnh Văn Nam | `CV20_Huynh_Van_Nam_Fresher_React.pdf` | PDF | Case E | Senior React & TS (`job-seed-02`) | React, TypeScript, HTML/CSS (Kinh nghiệm 6 tháng) | 48 - 65% |
| `cand-seed-21` | Võ Ngọc Lan | `CV21_Vo_Ngoc_Lan_Junior_Data_Science.docx` | DOCX | Case E | Senior Data Scientist (`job-seed-10`) | Python, Machine Learning (Kinh nghiệm 1 năm) | 46 - 63% |
| `cand-seed-22` | Quách Minh Trí | `CV22_Quach_Minh_Tri_Fresher_DevOps.pdf` | PDF | Case E | Senior DevOps (`job-seed-12`) | Docker, Linux, CI/CD cơ bản (Kinh nghiệm 8 tháng) | 45 - 62% |
| `cand-seed-23` | Diệp Trúc Quỳnh | `CV23_Diep_Truc_Quynh_Junior_HRBP.docx` | DOCX | Case E | HRBP Senior (`job-seed-29`) | Tuyển dụng, C&B cơ bản (Kinh nghiệm 1.5 năm) | 45 - 60% |
| `cand-seed-24` | Hà Văn Thắng | `CV24_Ha_Van_Thang_ReactJS_K8s_Go.pdf` | PDF | Case F | Senior React & TS (`job-seed-02`) | ReactJS, Golang, K8s, Postgres, Typescript | 84 - 94% |
| `cand-seed-25` | Lâm Khánh Chi | `CV25_Lam_Khanh_Chi_VAS_Tax.docx` | DOCX | Case F | Kế toán tổng hợp (`job-seed-16`) | Chuẩn mực kế toán VAS, Kế toán thuế, BCTC | 82 - 92% |
| `cand-seed-26` | Trương Gia Huy | `CV26_Truong_Gia_Huy_NLP_NLU.pdf` | PDF | Case F | NLP Research (`job-seed-11`) | NLU, Xử lý ngôn ngữ tự nhiên, PyTorch, BERT | 85 - 94% |
| `cand-seed-27` | Phạm Hồng Phúc | `CV27_Pham_Hong_Phuc_SEM_GA.docx` | DOCX | Case F | SEO Specialist (`job-seed-21`) | SEM, Search Engine Optimization, GA4, Ahrefs | 80 - 90% |
| `cand-seed-28` | Châu Quốc Tuấn | `CV28_Chau_Quoc_Tuan_Neg_Docker.pdf` | PDF | Case G | Python Backend (`job-seed-03`) | Python, FastAPI, PostgreSQL (chưa từng làm Docker) | 58 - 68% |
| `cand-seed-29` | Trần Ngọc Diệp | `CV29_Tran_Ngoc_Diep_Neg_MISA.docx` | DOCX | Case G | Kế toán tổng hợp (`job-seed-16`) | Kê khai thuế, BCTC (chưa có kinh nghiệm MISA) | 55 - 66% |
| `cand-seed-30` | Nguyễn Bảo Long | `CV30_Nguyen_Bao_Long_Neg_Ads.pdf` | PDF | Case G | Digital Marketing (`job-seed-20`) | SEO, Content (chưa từng chạy Facebook Ads) | 52 - 65% |


"""
HireSense AI - Multi-Industry Master Data Definitions
Includes:
- 15 Simulated Companies in Vietnam
- 15 Recruiter Accounts (1 per company)
- 50 Multi-Industry Job Descriptions across 14 categories
- 30 Candidate CVs (PDF & DOCX) with Ground Truth metadata
"""

# ==========================================
# 1. 15 SIMULATED COMPANIES
# ==========================================
COMPANIES_DATA = [
    {
        "id": "comp-seed-01",
        "name": "NovaTech Solutions",
        "slug": "novatech-solutions",
        "industry": "Công nghệ phần mềm",
        "company_size": "201-500",
        "location": "Đà Nẵng",
        "address": "15 Quang Trung, Quận Hải Châu, Đà Nẵng",
        "website": "https://novatech.example.test",
        "logo_url": "/uploads/logo_novatech.webp",
        "description": "Công ty công nghệ phần mềm chuyên phát triển các giải pháp Web, Mobile và điện toán đám mây cho thị trường quốc tế.",
        "status": "approved"
    },
    {
        "id": "comp-seed-02",
        "name": "DataVision Analytics",
        "slug": "datavision-analytics",
        "industry": "AI & Phân tích dữ liệu",
        "company_size": "51-200",
        "location": "Hà Nội",
        "address": "12 Cầu Giấy, Phường Dịch Vọng, Quận Cầu Giấy, Hà Nội",
        "website": "https://datavision.example.test",
        "logo_url": "/uploads/logo_datavision.webp",
        "description": "Doanh nghiệp tiên phong trong nghiên cứu và ứng dụng Trí tuệ nhân tạo (AI), Học máy (ML) và phân tích dữ liệu lớn.",
        "status": "approved"
    },
    {
        "id": "comp-seed-03",
        "name": "Finora Digital",
        "slug": "finora-digital",
        "industry": "Tài chính – Fintech",
        "company_size": "201-500",
        "location": "TP.HCM",
        "address": "88 Nguyễn Du, Phường Bến Nghé, Quận 1, TP.HCM",
        "website": "https://finora.example.test",
        "logo_url": "/uploads/logo_finora.webp",
        "description": "Tập đoàn công nghệ tài chính cung cấp giải pháp thanh toán điện tử, ngân hàng số và quản lý đầu tư thông minh.",
        "status": "approved"
    },
    {
        "id": "comp-seed-04",
        "name": "BrightWave Media",
        "slug": "brightwave-media",
        "industry": "Marketing & Truyền thông",
        "company_size": "51-200",
        "location": "TP.HCM",
        "address": "45 Pasteur, Phường Bến Nghé, Quận 1, TP.HCM",
        "website": "https://brightwave.example.test",
        "logo_url": "/uploads/logo_brightwave.webp",
        "description": "Agency truyền thông sáng tạo, chuyên cung cấp chiến lược Digital Marketing, SEO, Social Media và sản xuất nội dung số.",
        "status": "approved"
    },
    {
        "id": "comp-seed-05",
        "name": "PixelCraft Studio",
        "slug": "pixelcraft-studio",
        "industry": "Thiết kế đồ họa & UI/UX",
        "company_size": "11-50",
        "location": "Đà Nẵng",
        "address": "78 Bạch Đằng, Quận Hải Châu, Đà Nẵng",
        "website": "https://pixelcraft.example.test",
        "logo_url": "/uploads/logo_pixelcraft.webp",
        "description": "Studio sáng tạo hàng đầu về thiết kế trải nghiệm người dùng (UI/UX), đồ họa thương hiệu và hoạt họa kỹ thuật số.",
        "status": "approved"
    },
    {
        "id": "comp-seed-06",
        "name": "Mekong Logistics",
        "slug": "mekong-logistics",
        "industry": "Vận tải – Logistics",
        "company_size": "500+",
        "location": "Cần Thơ",
        "address": "120 Nguyễn Văn Cừ, Quận Ninh Kiều, Cần Thơ",
        "website": "https://mekonglogistics.example.test",
        "logo_url": "/uploads/logo_mekong.webp",
        "description": "Nhà cung cấp dịch vụ logistics tích hợp, quản lý kho bãi, vận tải đa phương thức và khai báo hải quan khu vực ĐBSCL.",
        "status": "approved"
    },
    {
        "id": "comp-seed-07",
        "name": "GreenMart Retail",
        "slug": "greenmart-retail",
        "industry": "Bán lẻ & Chuỗi cung ứng",
        "company_size": "500+",
        "location": "TP.HCM",
        "address": "250 Hoàng Diệu, Quận 4, TP.HCM",
        "website": "https://greenmart.example.test",
        "logo_url": "/uploads/logo_greenmart.webp",
        "description": "Chuỗi siêu thị bán lẻ thực phẩm sạch và tiêu dùng nhanh với hệ thống phân phối hiện đại phủ sóng toàn quốc.",
        "status": "approved"
    },
    {
        "id": "comp-seed-08",
        "name": "SunPeak Hospitality",
        "slug": "sunpeak-hospitality",
        "industry": "Du lịch – Khách sạn",
        "company_size": "201-500",
        "location": "Huế",
        "address": "30 Lê Lợi, TP. Huế, Thừa Thiên Huế",
        "website": "https://sunpeak.example.test",
        "logo_url": "/uploads/logo_sunpeak.webp",
        "description": "Hệ thống nghỉ dưỡng, khách sạn cao cấp và điều hành tour du lịch văn hóa di sản miền Trung Việt Nam.",
        "status": "approved"
    },
    {
        "id": "comp-seed-09",
        "name": "EduNext Academy",
        "slug": "edunext-academy",
        "industry": "Giáo dục & Đào tạo",
        "company_size": "51-200",
        "location": "Hà Nội",
        "address": "18 Hoàng Quốc Việt, Quận Cầu Giấy, Hà Nội",
        "website": "https://edunext.example.test",
        "logo_url": "/uploads/logo_edunext.webp",
        "description": "Hệ thống học viện đào tạo ngoại ngữ, kỹ năng số và phát triển năng lực quản trị doanh nghiệp ứng dụng công nghệ EdTech.",
        "status": "approved"
    },
    {
        "id": "comp-seed-10",
        "name": "BuildCore Engineering",
        "slug": "buildcore-engineering",
        "industry": "Xây dựng & Kỹ thuật",
        "company_size": "201-500",
        "location": "Hải Phòng",
        "address": "62 Lạch Tray, Quận Ngô Quyền, Hải Phòng",
        "website": "https://buildcore.example.test",
        "logo_url": "/uploads/logo_buildcore.webp",
        "description": "Tổng thầu thi công xây dựng dân dụng, công nghiệp và tư vấn thiết kế kết cấu công trình hạ tầng cảng biển.",
        "status": "approved"
    },
    {
        "id": "comp-seed-11",
        "name": "HealthBridge Services",
        "slug": "healthbridge-services",
        "industry": "Y tế – Chăm sóc sức khỏe",
        "company_size": "51-200",
        "location": "TP.HCM",
        "address": "102 Sư Vạn Hạnh, Quận 10, TP.HCM",
        "website": "https://healthbridge.example.test",
        "logo_url": "/uploads/logo_healthbridge.webp",
        "description": "Tổ chức y tế cung cấp dịch vụ khám chữa bệnh chất lượng cao, quản lý hồ sơ sức khỏe điện tử và điều phối chăm sóc y tế.",
        "status": "approved"
    },
    {
        "id": "comp-seed-12",
        "name": "TalentWorks HR",
        "slug": "talentworks-hr",
        "industry": "Nhân sự – Tuyển dụng",
        "company_size": "11-50",
        "location": "Hà Nội",
        "address": "55 Kim Mã, Quận Ba Đình, Hà Nội",
        "website": "https://talentworks.example.test",
        "logo_url": "/uploads/logo_talentworks.webp",
        "description": "Công ty tư vấn giải pháp nhân sự toàn diện, cung ứng nhân lực cấp cao và xây dựng hệ thống đãi ngộ cạnh tranh.",
        "status": "approved"
    },
    {
        "id": "comp-seed-13",
        "name": "SmartFactory Vietnam",
        "slug": "smartfactory-vietnam",
        "industry": "Sản xuất & Chế tạo",
        "company_size": "500+",
        "location": "Hải Phòng",
        "address": "Khu Công nghiệp Đình Vũ, Quận Hải An, Hải Phòng",
        "website": "https://smartfactory.example.test",
        "logo_url": "/uploads/logo_smartfactory.webp",
        "description": "Nhà máy sản xuất linh kiện cơ khí chính xác và thiết bị điện tử áp dụng tiêu chuẩn công nghiệp 4.0 và tự động hóa.",
        "status": "approved"
    },
    {
        "id": "comp-seed-14",
        "name": "CloudNest Technology",
        "slug": "cloudnest-technology",
        "industry": "Điện toán đám mây – DevOps",
        "company_size": "51-200",
        "location": "Đà Nẵng",
        "address": "02 Tiên Sơn, Quận Hải Châu, Đà Nẵng",
        "website": "https://cloudnest.example.test",
        "logo_url": "/uploads/logo_cloudnest.webp",
        "description": "Đơn vị cung cấp dịch vụ hạ tầng đám mây, kiến trúc DevOps tự động hóa CI/CD và giải pháp an toàn thông tin chuyên sâu.",
        "status": "approved"
    },
    {
        "id": "comp-seed-15",
        "name": "AgriFuture Solutions",
        "slug": "agrifuture-solutions",
        "industry": "Nông nghiệp công nghệ cao",
        "company_size": "11-50",
        "location": "Cần Thơ",
        "address": "45 Võ Văn Kiệt, Quận Bình Thủy, Cần Thơ",
        "website": "https://agrifuture.example.test",
        "logo_url": "/uploads/logo_agrifuture.webp",
        "description": "Doanh nghiệp nông nghiệp thông minh ứng dụng hệ thống cảm biến IoT, tưới nhỏ giọt tự động và chuẩn mực VietGAP.",
        "status": "approved"
    }
]

# ==========================================
# 2. 15 RECRUITER ACCOUNTS (1 per company)
# ==========================================
RECRUITERS_DATA = [
    {
        "id": f"user-rec-seed-{i+1:02d}",
        "email": f"recruiter{i+1:02d}@example.test",
        "full_name": name,
        "phone": f"0912{i+1:02d}999",
        "company_id": COMPANIES_DATA[i]["id"],
        "company_name": COMPANIES_DATA[i]["name"]
    }
    for i, name in enumerate([
        "Nguyễn Quốc Bảo (NovaTech)",
        "Phạm Minh Đức (DataVision)",
        "Vũ Thu Trang (Finora)",
        "Đặng Hoàng Yến (BrightWave)",
        "Lê Anh Tuấn (PixelCraft)",
        "Trần Hữu Nam (Mekong Logistics)",
        "Bùi Phương Mai (GreenMart)",
        "Hoàng Văn Khánh (SunPeak)",
        "Đỗ Thanh Thảo (EduNext)",
        "Ngô Trọng Tín (BuildCore)",
        "Nguyễn Thị Lan Anh (HealthBridge)",
        "Dương Minh Phúc (TalentWorks)",
        "Phan Văn Hậu (SmartFactory)",
        "Trịnh Quang Hải (CloudNest)",
        "Lâm Quốc Cường (AgriFuture)"
    ])
]
# ==========================================
# 3. 50 MULTI-INDUSTRY JOB DESCRIPTIONS
# ==========================================
JOBS_DATA = [
    # --- Nhóm 1: Software Development (6 JDs) ---
    {
        "id": "job-seed-01",
        "company_id": "comp-seed-01",
        "creator_id": "user-rec-seed-01",
        "title": "Junior Frontend Developer",
        "category": "Software Development",
        "job_type": "full_time",
        "location": "Đà Nẵng",
        "salary_min": 12000000,
        "salary_max": 18000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Tham gia phát triển giao diện người dùng cho các ứng dụng Web SaaS của đối tác quốc tế. Phối hợp chặt chẽ với UI/UX Designer và Backend team để chuyển đổi bản vẽ Figma thành mã nguồn chất lượng cao.",
        "requirements": "Tốt nghiệp Cao đẳng/Đại học chuyên ngành CNTT hoặc liên quan. Có từ 1-2 năm kinh nghiệm lập trình Frontend với JavaScript, HTML5, CSS3, ReactJS. Sử dụng thành thạo Git để quản lý phiên bản mã nguồn. Hiểu biết cơ bản về Responsive Web Design và RESTful API. Tinh thần học hỏi nhanh và chủ động trong công việc.",
        "benefits": "Lương tháng 13, thưởng dự án theo KPI. Bảo hiểm sức khỏe toàn diện PTI. Môi trường làm việc trẻ trung, trang bị Macbook Pro. Hỗ trợ kinh phí thi chứng chỉ quốc tế.",
        "required_skills": ["ReactJS", "JavaScript", "HTML", "CSS", "Git"],
        "preferred_skills": ["TypeScript", "Tailwind CSS", "Figma"]
    },
    {
        "id": "job-seed-02",
        "company_id": "comp-seed-01",
        "creator_id": "user-rec-seed-01",
        "title": "Senior React & TypeScript Engineer",
        "category": "Software Development",
        "job_type": "hybrid",
        "location": "Đà Nẵng",
        "salary_min": 35000000,
        "salary_max": 55000000,
        "currency": "VND",
        "experience_level": "senior",
        "status": "published",
        "description": "Chịu trách nhiệm thiết kế kiến trúc Frontend, tối ưu hóa hiệu năng render và xây dựng Design System dùng chung cho nền tảng thương mại điện tử đa quốc gia. Hướng dẫn và review code cho các kỹ sư Junior và Middle.",
        "requirements": "Có ít nhất 4 năm kinh nghiệm chuyên sâu với React, TypeScript và quản lý trạng thái nâng cao (Redux Toolkit, Zustand). Thành thạo tối ưu Web Core Vitals, SSR/SSG với Next.js. Kinh nghiệm viết Unit Test với Jest/Cypress và tích hợp CI/CD pipeline. Khả năng đọc hiểu tài liệu và giao tiếp kỹ thuật bằng tiếng Anh tốt.",
        "benefits": "Thu nhập cạnh tranh cùng gói cổ phần ESOP hàng năm. Chế độ làm việc Hybrid linh hoạt (2 ngày làm việc tại nhà mỗi tuần). Gói bảo hiểm sức khỏe VIP cho bản thân và gia đình.",
        "required_skills": ["React", "TypeScript", "Next.js", "Redux", "CI/CD", "Git"],
        "preferred_skills": ["GraphQL", "Tailwind CSS", "Docker"]
    },
    {
        "id": "job-seed-03",
        "company_id": "comp-seed-01",
        "creator_id": "user-rec-seed-01",
        "title": "Python Backend Developer",
        "category": "Software Development",
        "job_type": "full_time",
        "location": "Đà Nẵng",
        "salary_min": 22000000,
        "salary_max": 38000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Xây dựng các dịch vụ backend microservices xử lý lưu lượng cao bằng Python và FastAPI. Thiết kế cơ sở dữ liệu quan hệ tối ưu hóa truy vấn trên PostgreSQL và cấu hình bộ nhớ đệm với Redis.",
        "requirements": "Từ 2-4 năm kinh nghiệm phát triển backend với Python (FastAPI hoặc Django). Thành thạo cơ sở dữ liệu PostgreSQL, tối ưu câu lệnh SQL và indexing. Có kinh nghiệm triển khai ứng dụng bằng Docker và Docker Compose. Hiểu rõ kiến trúc Microservices, RESTful API và cơ chế xác thực JWT/OAuth2.",
        "benefits": "Thưởng hiệu suất định kỳ 6 tháng/lần. Trợ cấp ăn trưa và gửi xe. Teambuilding nghỉ dưỡng 5 sao thường niên. Cơ hội onsite công tác tại Singapore và Nhật Bản.",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis"],
        "preferred_skills": ["Kubernetes", "AWS", "Celery"]
    },
    {
        "id": "job-seed-04",
        "company_id": "comp-seed-02",
        "creator_id": "user-rec-seed-02",
        "title": "Senior Java Developer",
        "category": "Software Development",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 35000000,
        "salary_max": 50000000,
        "currency": "VND",
        "experience_level": "senior",
        "status": "published",
        "description": "Phát triển hệ thống lõi xử lý dữ liệu giao dịch tài chính quy mô lớn trên nền tảng Java Core và Spring Boot. Đảm bảo tính toàn vẹn dữ liệu, tính khả dụng cao và bảo mật nghiêm ngặt theo tiêu chuẩn ngân hàng.",
        "requirements": "Tối thiểu 5 năm kinh nghiệm lập trình Java, thành thạo Spring Boot, Spring Cloud, Hibernate/JPA. Kinh nghiệm chuyên sâu với hệ quản trị cơ sở dữ liệu Oracle, MySQL hoặc PostgreSQL. Thành thạo Message Broker (Apache Kafka, RabbitMQ). Khả năng phân tích và xử lý lỗi hệ thống phân tán phức tạp.",
        "benefits": "Lương tháng 13 + thưởng hiệu quả kinh doanh từ 2-4 tháng lương. Gói khám sức khỏe định kỳ tại Bệnh viện Quốc tế Vinmec. Chế độ đào tạo thăng tiến rõ ràng lên vị trí Tech Lead.",
        "required_skills": ["Java", "Spring Boot", "Kafka", "MySQL", "Microservices"],
        "preferred_skills": ["Kubernetes", "Redis", "Docker"]
    },
    {
        "id": "job-seed-05",
        "company_id": "comp-seed-03",
        "creator_id": "user-rec-seed-03",
        "title": "Full-Stack Developer",
        "category": "Software Development",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 25000000,
        "salary_max": 42000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Phụ trách phát triển toàn diện tính năng từ giao diện người dùng ReactJS đến API backend Node.js và tích hợp cơ sở dữ liệu MongoDB/PostgreSQL cho sản phẩm ví điện tử thông minh.",
        "requirements": "Có 3+ năm kinh nghiệm Full-stack với ReactJS ở Frontend và Node.js/Express hoặc NestJS ở Backend. Nắm vững TypeScript, lập trình bất đồng bộ và kiến trúc Event-Driven. Kinh nghiệm tích hợp cổng thanh toán bên thứ ba (VNPay, ZaloPay, Stripe). Tinh thần trách nhiệm cao đối với chất lượng sản phẩm.",
        "benefits": "Cung cấp thiết bị làm việc hiện đại. 15 ngày phép năm có lương. Trợ cấp phụ cấp chứng chỉ công nghệ 2,000,000 VND/tháng. Bữa phụ trà bánh trái cây miễn phí mỗi ngày.",
        "required_skills": ["ReactJS", "Node.js", "TypeScript", "PostgreSQL", "RESTful API"],
        "preferred_skills": ["MongoDB", "Docker", "AWS"]
    },
    {
        "id": "job-seed-06",
        "company_id": "comp-seed-05",
        "creator_id": "user-rec-seed-05",
        "title": "Mobile React Native Developer",
        "category": "Software Development",
        "job_type": "hybrid",
        "location": "Đà Nẵng",
        "salary_min": 20000000,
        "salary_max": 35000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Xây dựng và phát hành các ứng dụng di động đa nền tảng iOS & Android bằng React Native cho các sản phẩm mạng xã hội chia sẻ ảnh sáng tạo.",
        "requirements": "Từ 2-3 năm kinh nghiệm phát triển ứng dụng di động bằng React Native. Hiểu biết sâu về Native Modules (Java/Kotlin, Swift/Objective-C). Kinh nghiệm tối ưu hóa hiệu năng render ảnh động và danh sách vô tận (FlatList). Có ứng dụng thực tế đã phát hành trên App Store hoặc Google Play Store.",
        "benefits": "Thưởng phát hành ứng dụng đạt mốc tải về. Giờ làm việc linh hoạt (Flexitime). Khóa học tiếng Anh giao tiếp với giáo viên bản xứ do công ty tài trợ 100%.",
        "required_skills": ["React Native", "JavaScript", "TypeScript", "Redux", "Git"],
        "preferred_skills": ["iOS", "Android", "Firebase"]
    },

    # --- Nhóm 2: Artificial Intelligence & Data (5 JDs) ---
    {
        "id": "job-seed-07",
        "company_id": "comp-seed-02",
        "creator_id": "user-rec-seed-02",
        "title": "AI Engineer",
        "category": "Artificial Intelligence & Data",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 35000000,
        "salary_max": 60000000,
        "currency": "VND",
        "experience_level": "senior",
        "status": "published",
        "description": "Nghiên cứu, huấn luyện và triển khai các mô hình ngôn ngữ lớn (LLMs), mô hình nhúng vector (Embeddings) và kiến trúc RAG phục vụ trích xuất tri thức tự động cho nền tảng tuyển dụng thông minh.",
        "requirements": "Tốt nghiệp Thạc sĩ hoặc Cử nhân xuất sắc ngành Khoa học Máy tính, Trí tuệ Nhân tạo. Có từ 3 năm kinh nghiệm thực tế với PyTorch, TensorFlow, Transformers (Hugging Face). Nắm vững kỹ thuật prompt engineering, RAG, vector database (pgvector, Milvus, Qdrant). Khả năng tối ưu inference và triển khai mô hình với FastAPI và Triton/ONNX.",
        "benefits": "Cụm máy chủ tính toán GPU chuyên dụng (A100/H100) phục vụ nghiên cứu. Cơ hội tham gia xuất bản bài báo khoa học quốc tế. Thưởng sáng chế và giải pháp công nghệ.",
        "required_skills": ["Python", "PyTorch", "LLMs", "RAG", "Machine Learning"],
        "preferred_skills": ["pgvector", "Docker", "FastAPI", "NLP"]
    },
    {
        "id": "job-seed-08",
        "company_id": "comp-seed-02",
        "creator_id": "user-rec-seed-02",
        "title": "Machine Learning Engineer",
        "category": "Artificial Intelligence & Data",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 25000000,
        "salary_max": 45000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Phát triển các pipeline huấn luyện và đánh giá mô hình học máy phục vụ bài toán xếp hạng ứng viên, dự đoán mức độ gắn kết công việc và phát hiện gian lận hồ sơ.",
        "requirements": "2-4 năm kinh nghiệm áp dụng Machine Learning trong môi trường sản phẩm thực tế. Thành thạo Scikit-learn, XGBoost, LightGBM và thư viện xử lý dữ liệu Pandas, NumPy. Có kinh nghiệm xây dựng MLOps pipeline tự động hóa (MLflow, Kubeflow). Hiểu biết sâu về thống kê ứng dụng và kỹ thuật Feature Engineering.",
        "benefits": "Môi trường học thuật kết hợp thực tiễn sản phẩm cao cấp. Được bảo trợ tham dự các hội thảo công nghệ AI trong và ngoài nước. Thưởng dự án theo tiến độ triển khai.",
        "required_skills": ["Python", "Machine Learning", "Scikit-learn", "SQL", "Pandas"],
        "preferred_skills": ["MLflow", "Docker", "PyTorch"]
    },
    {
        "id": "job-seed-09",
        "company_id": "comp-seed-03",
        "creator_id": "user-rec-seed-03",
        "title": "Data Analyst",
        "category": "Artificial Intelligence & Data",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 18000000,
        "salary_max": 28000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Thu thập, làm sạch và phân tích các chỉ số hành vi người dùng, luồng giao dịch thanh toán và chuyển đổi kênh quảng cáo. Thiết kế các báo cáo Dashboard trực quan phục vụ Ban Giám đốc ra quyết định chiến lược.",
        "requirements": "Có 1-3 năm kinh nghiệm trong vai trò Phân tích Dữ liệu (Data Analyst). Viết truy vấn SQL thành thạo, có khả năng xử lý dữ liệu phức tạp. Sử dụng thành thạo PowerBI hoặc Tableau và ngôn ngữ Python phục vụ phân tích thống kê. Tư duy logic tốt, khả năng trình bày dữ liệu (Data Storytelling) mạch lạc.",
        "benefits": "Phụ cấp ăn trưa, sim điện thoại và vé gửi xe. Thưởng thành tích kinh doanh hàng quý. Cơ hội đào tạo nâng cao lên vị trí Data Scientist hoặc Analytics Manager.",
        "required_skills": ["SQL", "PowerBI", "Python", "Data Analysis", "Excel"],
        "preferred_skills": ["Tableau", "PostgreSQL", "Google Analytics"]
    },
    {
        "id": "job-seed-10",
        "company_id": "comp-seed-02",
        "creator_id": "user-rec-seed-02",
        "title": "Data Scientist",
        "category": "Artificial Intelligence & Data",
        "job_type": "hybrid",
        "location": "Hà Nội",
        "salary_min": 30000000,
        "salary_max": 50000000,
        "currency": "VND",
        "experience_level": "senior",
        "status": "published",
        "description": "Xây dựng các mô hình dự báo kinh tế lượng, phân khúc khách hàng tự động và hệ thống gợi ý việc làm cá nhân hóa (Recommendation Engine) dựa trên công nghệ Graph & Deep Learning.",
        "requirements": "Tối thiểu 4 năm kinh nghiệm trong lĩnh vực Khoa học Dữ liệu. Nền tảng vững chắc về toán học, xác suất thống kê và thuật toán tối ưu. Kinh nghiệm xử lý dữ liệu lớn trên nền tảng PySpark, Hadoop hoặc BigQuery. Khả năng chuyển hóa bài toán kinh doanh phức tạp thành giải pháp thuật toán định lượng cụ thể.",
        "benefits": "Mức lương thỏa thuận không giới hạn theo năng lực. Gói khám chữa bệnh gia đình trị giá 30 triệu/năm. Nghỉ phép 16 ngày/năm.",
        "required_skills": ["Python", "Machine Learning", "PySpark", "SQL", "Deep Learning"],
        "preferred_skills": ["Data Science", "AWS", "Docker"]
    },
    {
        "id": "job-seed-11",
        "company_id": "comp-seed-02",
        "creator_id": "user-rec-seed-02",
        "title": "NLP Engineer",
        "category": "Artificial Intelligence & Data",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 28000000,
        "salary_max": 48000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Nghiên cứu và tinh chỉnh các mô hình xử lý ngôn ngữ tự nhiên (NLP) cho tiếng Việt: trích xuất thông tin thực thể (NER), phân loại văn bản, tóm tắt tự động hồ sơ tuyển dụng và chấm điểm tương đồng ngữ nghĩa.",
        "requirements": "Từ 2 năm kinh nghiệm chuyên sâu về NLP. Thành thạo tiếng Việt xử lý ngôn ngữ (PhoBERT, vncorenlp, underthesea). Có kinh nghiệm huấn luyện và fine-tuning mô hình ngôn ngữ dựa trên Transformer với PyTorch. Hiểu biết về Semantic Search và Vector Embeddings.",
        "benefits": "Trợ cấp nghiên cứu 5 triệu/tháng. Được cung cấp tài khoản cloud tính toán cao cấp. Môi trường trẻ trung, sáng tạo, không gò bó thời gian.",
        "required_skills": ["NLP", "Python", "PyTorch", "Transformers", "Machine Learning"],
        "preferred_skills": ["FastAPI", "Docker", "pgvector"]
    },

    # --- Nhóm 3: DevOps & Cybersecurity (4 JDs) ---
    {
        "id": "job-seed-12",
        "company_id": "comp-seed-14",
        "creator_id": "user-rec-seed-14",
        "title": "DevOps Engineer",
        "category": "DevOps & Cybersecurity",
        "job_type": "full_time",
        "location": "Đà Nẵng",
        "salary_min": 25000000,
        "salary_max": 45000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Quản lý và vận hành hệ thống hạ tầng microservices trên nền tảng AWS và Kubernetes. Thiết lập và tự động hóa các đường ống CI/CD bằng GitLab CI/GitHub Actions, tối ưu hóa chi phí đám mây và thời gian triển khai.",
        "requirements": "Tối thiểu 3 năm kinh nghiệm trong vai trò DevOps/SRE. Quản trị thành thạo hệ điều hành Linux và hạ tầng mạng đám mây. Kinh nghiệm thực tiễn sâu với Docker, Kubernetes, Helm Charts và Terraform (Infrastructure as Code). Khả năng ứng trực và khắc phục sự cố hệ thống 24/7.",
        "benefits": "Trợ cấp trực ca và xử lý sự cố ngoài giờ. Cơ hội thi lấy các chứng chỉ AWS Solutions Architect / CKA được chi trả toàn phần. Du lịch nước ngoài hàng năm.",
        "required_skills": ["DevOps", "Kubernetes", "Docker", "CI/CD", "AWS", "Linux"],
        "preferred_skills": ["Terraform", "Prometheus", "GitLab CI"]
    },
    {
        "id": "job-seed-13",
        "company_id": "comp-seed-14",
        "creator_id": "user-rec-seed-14",
        "title": "Cloud Engineer",
        "category": "DevOps & Cybersecurity",
        "job_type": "hybrid",
        "location": "Đà Nẵng",
        "salary_min": 28000000,
        "salary_max": 45000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Thiết kế, xây dựng và di chuyển các hệ thống doanh nghiệp lên môi trường đám mây AWS / Azure / GCP. Giám sát tính sẵn sàng, sao lưu tự động và phân tán tải lưu lượng.",
        "requirements": "Có 3 năm kinh nghiệm với dịch vụ đám mây AWS hoặc Google Cloud Platform. Nắm chắc kiến trúc VPC, IAM, EC2, S3, RDS, CloudWatch. Có chứng chỉ AWS Associate hoặc GCP Professional là lợi thế lớn. Kỹ năng scripting tự động hóa bằng Python hoặc Bash.",
        "benefits": "Làm việc tại văn phòng view sông Hàn thơ mộng. Gói bảo hiểm sức khỏe Bảo Việt hạng Kim Cương. Cơ chế thưởng dự án rõ ràng minh bạch.",
        "required_skills": ["AWS", "Cloud", "Linux", "Docker", "Python"],
        "preferred_skills": ["GCP", "Terraform", "Kubernetes"]
    },
    {
        "id": "job-seed-14",
        "company_id": "comp-seed-14",
        "creator_id": "user-rec-seed-14",
        "title": "System Administrator",
        "category": "DevOps & Cybersecurity",
        "job_type": "full_time",
        "location": "Đà Nẵng",
        "salary_min": 15000000,
        "salary_max": 24000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Quản trị hệ thống máy chủ nội bộ Linux/Windows Server, quản lý tài khoản Active Directory, sao lưu dữ liệu và hỗ trợ kỹ thuật hạ tầng mạng LAN/WAN, Firewall cho toàn bộ công ty.",
        "requirements": "1-3 năm kinh nghiệm quản trị hệ thống máy chủ và mạng doanh nghiệp. Nắm vững giao thức mạng TCP/IP, DNS, DHCP, VPN. Có kinh nghiệm cấu hình thiết bị mạng Cisco, Fortinet hoặc Mikrotik. Tinh thần trách nhiệm, phản ứng nhanh với các sự cố kết nối nội bộ.",
        "benefits": "Môi trường công nghệ hiện đại. Cơm trưa miễn phí tại căng tin công ty. Đánh giá tăng lương định kỳ 1 năm 1 lần.",
        "required_skills": ["Linux", "Windows Server", "Networking", "VPN", "Firewall"],
        "preferred_skills": ["Docker", "Bash Scripting", "Active Directory"]
    },
    {
        "id": "job-seed-15",
        "company_id": "comp-seed-03",
        "creator_id": "user-rec-seed-03",
        "title": "Cybersecurity Analyst",
        "category": "DevOps & Cybersecurity",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 25000000,
        "salary_max": 42000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Theo dõi và phát hiện các lỗ hổng bảo mật, kiểm thử xâm nhập (Penetration Testing) ứng dụng web và API tài chính, đồng thời xây dựng chính sách an toàn thông tin tuân thủ chuẩn PCI-DSS và ISO 27001.",
        "requirements": "Có 2-4 năm kinh nghiệm trong lĩnh vực An toàn thông tin / Bảo mật hệ thống. Thành thạo các công cụ kiểm thử bảo mật như Burp Suite, Nessus, Wireshark, Metasploit. Nắm vững lỗ hổng OWASP Top 10 và các phương thức tấn công ứng dụng web. Có chứng chỉ CEH, CompTIA Security+ hoặc OSCP là điểm cộng lớn.",
        "benefits": "Thu nhập hấp dẫn, phụ cấp độc hại kỹ thuật số. Được tài trợ toàn bộ chi phí thi các chứng chỉ quốc tế uy tín. Cơ hội làm việc cùng các chuyên gia bảo mật hàng đầu.",
        "required_skills": ["Cybersecurity", "An toàn thông tin", "Penetration Testing", "Linux", "Networking"],
        "preferred_skills": ["Python", "OWASP", "SIEM"]
    },

    # --- Nhóm 4: Finance & Accounting (4 JDs) ---
    {
        "id": "job-seed-16",
        "company_id": "comp-seed-03",
        "creator_id": "user-rec-seed-03",
        "title": "Kế toán tổng hợp",
        "category": "Finance & Accounting",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 14000000,
        "salary_max": 22000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Kiểm tra và kiểm soát các định khoản nghiệp vụ phát sinh, lập bảng cân đối kế toán, lập báo cáo tài chính định kỳ theo chuẩn mực kế toán Việt Nam (VAS) và quyết toán thuế với cơ quan thuế.",
        "requirements": "Tốt nghiệp Đại học chuyên ngành Kế toán - Kiểm toán hoặc Tài chính. Có từ 3 năm kinh nghiệm ở vị trí Kế toán tổng hợp. Sử dụng thành thạo phần mềm kế toán MISA hoặc Fast Accounting và Excel nâng cao. Nắm chắc Luật Thuế hiện hành (VAT, TNDN, TNCN). Trung thực, cẩn thận và có trách nhiệm cao với số liệu.",
        "benefits": "Lương tháng 13 + thưởng quyết toán năm. Chế độ phụ cấp công tác và điện thoại. Môi trường công ty tài chính năng động, quy chuẩn rõ ràng.",
        "required_skills": ["Kế toán tổng hợp", "Báo cáo tài chính", "Kế toán thuế", "MISA", "Excel"],
        "preferred_skills": ["Fast Accounting", "Phân tích tài chính", "VAS"]
    },
    {
        "id": "job-seed-17",
        "company_id": "comp-seed-03",
        "creator_id": "user-rec-seed-03",
        "title": "Chuyên viên phân tích tài chính",
        "category": "Finance & Accounting",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 20000000,
        "salary_max": 35000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Xây dựng mô hình dự báo tài chính, đánh giá hiệu quả đầu tư các dự án công nghệ mới, lập kế hoạch ngân sách và phân tích dòng tiền giúp Ban Lãnh đạo tối ưu hóa nguồn vốn kinh doanh.",
        "requirements": "Tốt nghiệp chuyên ngành Tài chính doanh nghiệp hoặc Ngân hàng. 2-4 năm kinh nghiệm làm việc tại vị trí Chuyên viên Phân tích Tài chính (Financial Analyst). Khả năng xây dựng Financial Modeling chuyên sâu bằng Excel. Có chứng chỉ CFA (Level 1 trở lên) hoặc ACCA là lợi thế cạnh tranh lớn. Kỹ năng thuyết trình số liệu mạch lạc.",
        "benefits": "Thưởng hiệu quả đầu tư dự án theo quý. Được tài trợ kinh phí học và thi chứng chỉ CFA. Môi trường làm việc chuyên nghiệp chuẩn quốc tế tại Quận 1.",
        "required_skills": ["Phân tích tài chính", "Financial Modeling", "Excel", "Báo cáo tài chính", "Quản trị dòng tiền"],
        "preferred_skills": ["CFA", "PowerBI", "SQL"]
    },
    {
        "id": "job-seed-18",
        "company_id": "comp-seed-03",
        "creator_id": "user-rec-seed-03",
        "title": "Chuyên viên tín dụng doanh nghiệp",
        "category": "Finance & Accounting",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 15000000,
        "salary_max": 28000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Thẩm định hồ sơ năng lực tài chính và phương án kinh doanh của khách hàng doanh nghiệp vừa và nhỏ (SMEs). Đề xuất hạn mức cấp tín dụng, theo dõi thu hồi nợ và quản trị rủi ro nợ xấu.",
        "requirements": "Tốt nghiệp Đại học khối ngành Kinh tế, Tài chính Ngân hàng. 1-3 năm kinh nghiệm thẩm định tín dụng tại các ngân hàng thương mại hoặc công ty tài chính. Nắm chắc quy trình thẩm định, kỹ năng đọc hiểu báo cáo tài chính và kiểm tra tài sản bảo đảm. Kỹ năng giao tiếp và xử lý tình huống khéo léo.",
        "benefits": "Thu nhập gồm Lương cứng + Hoa hồng tín dụng theo doanh số không giới hạn. Cơ hội mở rộng mạng lưới quan hệ với các chủ doanh nghiệp lớn.",
        "required_skills": ["Thẩm định tín dụng", "Phân tích tài chính", "Quản trị rủi ro", "Báo cáo tài chính", "Excel"],
        "preferred_skills": ["Đàm phán", "Kinh tế vi mô", "Sales B2B"]
    },
    {
        "id": "job-seed-19",
        "company_id": "comp-seed-07",
        "creator_id": "user-rec-seed-07",
        "title": "Kế toán nội bộ chuỗi bán lẻ",
        "category": "Finance & Accounting",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 10000000,
        "salary_max": 16000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Theo dõi và đối soát thu chi hàng ngày tại các điểm siêu thị bán lẻ, kiểm soát công nợ phải thu/phải trả nhà cung cấp, kiểm kê hàng hóa định kỳ và lập báo cáo quỹ tiền mặt.",
        "requirements": "Tốt nghiệp Cao đẳng trở lên ngành Kế toán. Có từ 1-2 năm kinh nghiệm kế toán nội bộ hoặc kế toán kho tại các chuỗi bán lẻ, F&B. Kỹ năng Excel khá (VLOOKUP, SUMIFS, Pivot Table). Cẩn thận, chi tiết, chịu được áp lực đối chiếu số liệu cuối tháng.",
        "benefits": "Giảm giá 15% khi mua sắm tại chuỗi siêu thị GreenMart. Đóng bảo hiểm đầy đủ theo quy định của nhà nước. Thưởng lễ tết và lương tháng 13.",
        "required_skills": ["Kế toán nội bộ", "Kiểm soát công nợ", "Excel", "Quản lý kho", "Đối soát số liệu"],
        "preferred_skills": ["MISA", "ERP", "Bán lẻ"]
    },

    # --- Nhóm 5: Marketing & Truyền thông (4 JDs) ---
    {
        "id": "job-seed-20",
        "company_id": "comp-seed-04",
        "creator_id": "user-rec-seed-04",
        "title": "Digital Marketing Specialist",
        "category": "Marketing",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 18000000,
        "salary_max": 30000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Lập kế hoạch, triển khai và tối ưu hóa các chiến dịch quảng cáo đa kênh (Google Ads, Facebook Ads, TikTok Ads) nhằm đạt mục tiêu tăng trưởng lượt chuyển đổi và doanh số cho khách hàng doanh nghiệp.",
        "requirements": "Có từ 2-4 năm kinh nghiệm chạy quảng cáo Digital Performance Marketing với ngân sách từ 200 triệu/tháng trở lên. Thành thạo Google Analytics (GA4), Meta Ads Manager và thiết lập sự kiện chuyển đổi qua Google Tag Manager. Tư duy số liệu nhạy bén, khả năng A/B testing mẫu quảng cáo liên tục.",
        "benefits": "Thưởng KPI hấp dẫn theo hiệu quả chiến dịch. Môi trường Agency trẻ trung, năng động, không mặc đồng phục. Teambuilding và sự kiện tiệc công ty diễn ra thường xuyên.",
        "required_skills": ["Digital Marketing", "Facebook Ads", "Google Ads", "Google Analytics", "SEM"],
        "preferred_skills": ["TikTok Ads", "SEO", "Content Marketing"]
    },
    {
        "id": "job-seed-21",
        "company_id": "comp-seed-04",
        "creator_id": "user-rec-seed-04",
        "title": "SEO Specialist",
        "category": "Marketing",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 15000000,
        "salary_max": 25000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Nghiên cứu bộ từ khóa, tối ưu hóa On-page, Off-page và Technical SEO cho website thương mại điện tử nhằm duy trì thứ hạng Top Google bền vững và gia tăng lưu lượng truy cập tự nhiên (Organic Traffic).",
        "requirements": "Có 2-3 năm kinh nghiệm thực chiến SEO. Thành thạo các công cụ phân tích SEO như Ahrefs, SEMrush, Google Search Console, Screaming Frog. Nắm vững cấu trúc Technical SEO (Schema, sitemap, Core Web Vitals, index). Có các dự án SEO từ khóa cạnh tranh đã lên Top thành công để minh họa.",
        "benefits": "Thưởng thăng hạng từ khóa lên Top 1-3. Cung cấp tài khoản công cụ SEO bản quyền đầy đủ. Môi trường khuyến khích thử nghiệm chiến thuật mới.",
        "required_skills": ["SEO", "Google Analytics", "Google Search Console", "Content Strategy", "Technical SEO"],
        "preferred_skills": ["WordPress", "HTML", "Copywriting"]
    },
    {
        "id": "job-seed-22",
        "company_id": "comp-seed-04",
        "creator_id": "user-rec-seed-04",
        "title": "Content Marketing Executive",
        "category": "Marketing",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 12000000,
        "salary_max": 18000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Sáng tạo nội dung bài viết chuẩn SEO cho Website, kịch bản video ngắn cho TikTok/Reels và thông điệp truyền thông cho các chiến dịch ra mắt sản phẩm mới của thương hiệu.",
        "requirements": "Tốt nghiệp chuyên ngành Báo chí, Truyền thông, Ngôn ngữ hoặc Marketing. Có 1-2 năm kinh nghiệm viết nội dung sáng tạo (Copywriting/Content Marketing). Khả năng viết lách mạch lạc, bắt trend tốt, am hiểu tâm lý người đọc thế hệ Gen Z và Millennials. Biết sử dụng công cụ thiết kế cơ bản như Canva hoặc Photoshop là lợi thế.",
        "benefits": "Môi trường tự do sáng tạo, khuyến khích ý tưởng độc đáo. Được làm việc trực tiếp cùng Creative Director kỳ cựu. Du lịch công ty 2 lần/năm.",
        "required_skills": ["Content Marketing", "Copywriting", "Social Media", "Sáng tạo nội dung", "Storytelling"],
        "preferred_skills": ["Canva", "SEO", "Kịch bản Video"]
    },
    {
        "id": "job-seed-23",
        "company_id": "comp-seed-04",
        "creator_id": "user-rec-seed-04",
        "title": "Social Media Executive",
        "category": "Marketing",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 11000000,
        "salary_max": 17000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Quản trị và phát triển các kênh mạng xã hội chính thức (Fanpage Facebook, Group cộng đồng, Kênh TikTok, LinkedIn). Tương tác với người theo dõi, tăng trưởng lượng tiếp cận tự nhiên và giải quyết khủng hoảng truyền thông mạng xã hội bước đầu.",
        "requirements": "Tối thiểu 1 năm kinh nghiệm quản trị kênh mạng xã hội cho doanh nghiệp. Kỹ năng giao tiếp và tương tác cộng đồng duyên dáng, nhạy bén với các xu hướng truyền thông xã hội mới nhất. Khả năng lập kế hoạch xuất bản nội dung (Content Calendar) hàng tuần.",
        "benefits": "Trợ cấp trang thiết bị quay chụp hiện đại. Thưởng vượt chỉ tiêu tương tác kênh. Chế độ bảo hiểm và phúc lợi đầy đủ.",
        "required_skills": ["Social Media", "Quản trị mạng xã hội", "Content Marketing", "Community Management", "Facebook Ads"],
        "preferred_skills": ["TikTok", "CapCut", "Copywriting"]
    },

    # --- Nhóm 6: Graphic Design & UI/UX (3 JDs) ---
    {
        "id": "job-seed-24",
        "company_id": "comp-seed-05",
        "creator_id": "user-rec-seed-05",
        "title": "Graphic Designer",
        "category": "Graphic Design",
        "job_type": "full_time",
        "location": "Đà Nẵng",
        "salary_min": 14000000,
        "salary_max": 22000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Thiết kế bộ nhận diện thương hiệu (Logo, Brand Guidelines), ấn phẩm truyền thông số (Banner, Infographic, Poster quảng cáo) và bao bì sản phẩm cho các đối tác sáng tạo.",
        "requirements": "Tốt nghiệp chuyên ngành Thiết kế đồ họa, Mỹ thuật ứng dụng hoặc có chứng chỉ đào tạo đồ họa chuyên nghiệp. Sử dụng thành thạo bộ công cụ Adobe Creative Suite: Photoshop, Illustrator, InDesign. Có gu thẩm mỹ hiện đại, tư duy màu sắc và bố cục (Layout/Typography) xuất sắc. Bắt buộc gửi kèm Portfolio sản phẩm thực tế khi ứng tuyển.",
        "benefits": "Cung cấp bảng vẽ Wacom và màn hình chuyên đồ họa 4K. Không gian làm việc mở, truyền cảm hứng nghệ thuật. Thưởng thiết kế xuất sắc hàng tháng.",
        "required_skills": ["Photoshop", "Illustrator", "Thiết kế đồ họa", "Branding", "Typography"],
        "preferred_skills": ["Figma", "InDesign", "In ấn"]
    },
    {
        "id": "job-seed-25",
        "company_id": "comp-seed-05",
        "creator_id": "user-rec-seed-05",
        "title": "UI/UX Designer",
        "category": "Graphic Design",
        "job_type": "hybrid",
        "location": "Đà Nẵng",
        "salary_min": 22000000,
        "salary_max": 38000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Nghiên cứu hành vi người dùng (User Research), xây dựng Wireframe, User Flow, Interactive Prototype và thiết kế giao diện người dùng độ sắc nét cao (High-fidelity UI) cho ứng dụng di động và web thương mại điện tử.",
        "requirements": "Từ 2-4 năm kinh nghiệm thiết kế UI/UX cho sản phẩm số. Thành thạo công cụ Figma (Auto-layout, Components, Variants, Design Tokens). Nắm vững nguyên lý thiết kế tương tác, Design Thinking và khả năng thực hiện Usability Testing. Có Portfolio thể hiện quy trình giải quyết vấn đề bằng trải nghiệm người dùng.",
        "benefits": "Thu nhập cạnh tranh. Chế độ làm việc Hybrid linh hoạt. Được đài thọ tham gia các hội nghị UX quốc tế và mua các tài khoản plugin/thư viện bản quyền.",
        "required_skills": ["Figma", "UI/UX", "Wireframing", "Prototyping", "User Research"],
        "preferred_skills": ["Design System", "Photoshop", "HTML/CSS"]
    },
    {
        "id": "job-seed-26",
        "company_id": "comp-seed-05",
        "creator_id": "user-rec-seed-05",
        "title": "Motion Graphic Designer",
        "category": "Graphic Design",
        "job_type": "full_time",
        "location": "Đà Nẵng",
        "salary_min": 18000000,
        "salary_max": 30000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Sáng tạo các video đồ họa chuyển động 2D (Motion Graphics), video giới thiệu tính năng sản phẩm công nghệ (Product Explainer Video), hoạt họa logo và hiệu ứng kỹ thuật số cho các chiến dịch quảng bá quốc tế.",
        "requirements": "2-3 năm kinh nghiệm trong lĩnh vực Motion Graphics và Video Editing. Sử dụng chuyên sâu Adobe After Effects, Premiere Pro, kết hợp tốt với Illustrator và Photoshop. Hiểu sâu về nhịp điệu (Pacing), nguyên lý hoạt họa (12 Principles of Animation) và âm thanh bổ trợ.",
        "benefits": "Trang bị dàn máy tính đồ họa chuyên dụng cấu hình cực khủng. Thưởng tác phẩm viral và dự án hoàn thành xuất sắc. Giờ giấc làm việc thoải mái theo tiến độ.",
        "required_skills": ["After Effects", "Premiere", "Motion Graphics", "Photoshop", "Illustrator"],
        "preferred_skills": ["Cinema 4D", "3D Animation", "Storyboarding"]
    },

    # --- Nhóm 7: Human Resources (3 JDs) ---
    {
        "id": "job-seed-27",
        "company_id": "comp-seed-12",
        "creator_id": "user-rec-seed-12",
        "title": "HR Generalist",
        "category": "Human Resources",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 15000000,
        "salary_max": 24000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Phụ trách điều phối các hoạt động nhân sự tổng hợp tại công ty: quản lý hồ sơ nhân sự, theo dõi hợp đồng lao động, chấm công - tính lương, thực hiện thủ tục bảo hiểm xã hội (BHXH) và hỗ trợ giải quyết quan hệ lao động.",
        "requirements": "Tốt nghiệp Đại học ngành Quản trị Nhân lực, Luật hoặc Kinh tế. Có từ 2-4 năm kinh nghiệm làm nhân sự tổng hợp. Nắm vững Bộ luật Lao động và các quy định về BHXH, Thuế TNCN hiện hành. Kỹ năng giao tiếp, lắng nghe và giải quyết xung đột thấu đáo.",
        "benefits": "Môi trường làm việc thân thiện, tôn trọng văn hóa cá nhân. Đóng đầy đủ 100% bảo hiểm trên lương thực tế. Thưởng thâm niên và quà tặng dịp sinh nhật, lễ tết.",
        "required_skills": ["Tuyển dụng", "Tính lương", "Luật lao động", "C&B", "Quan hệ lao động"],
        "preferred_skills": ["BHXH", "Excel", "Onboarding"]
    },
    {
        "id": "job-seed-28",
        "company_id": "comp-seed-12",
        "creator_id": "user-rec-seed-12",
        "title": "Recruitment Specialist",
        "category": "Human Resources",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 16000000,
        "salary_max": 26000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Tìm kiếm, sàng lọc hồ sơ ứng viên và điều phối quy trình phỏng vấn cho các vị trí công nghệ thông tin và quản lý cấp trung theo yêu cầu của đối tác khách hàng.",
        "requirements": "Có ít nhất 2 năm kinh nghiệm tuyển dụng (ưu tiên kinh nghiệm Tech Recruiter hoặc Headhunter). Khả năng tìm nguồn ứng viên (Sourcing) xuất sắc qua LinkedIn, TopCV, GitHub. Kỹ năng phỏng vấn theo phương pháp hành vi (STAR) và đàm phán thư mời nhận việc (Offer).",
        "benefits": "Lương cứng + Thưởng hoa hồng tuyển dụng theo từng vị trí tuyển thành công (không giới hạn). Được tiếp cận mạng lưới ứng viên cao cấp toàn quốc.",
        "required_skills": ["Tuyển dụng", "Talent Acquisition", "Headhunting", "Phỏng vấn", "LinkedIn Sourcing"],
        "preferred_skills": ["Tech Recruitment", "Đàm phán", "STAR Method"]
    },
    {
        "id": "job-seed-29",
        "company_id": "comp-seed-12",
        "creator_id": "user-rec-seed-12",
        "title": "HR Business Partner (HRBP)",
        "category": "Human Resources",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 30000000,
        "salary_max": 50000000,
        "currency": "VND",
        "experience_level": "senior",
        "status": "published",
        "description": "Đồng hành cùng Ban Lãnh đạo các khối kinh doanh để hoạch định cơ cấu tổ chức, xây dựng khung năng lực, lộ trình thăng tiến và chiến lược giữ chân nhân tài then chốt.",
        "requirements": "Tối thiểu 5 năm kinh nghiệm trong mảng nhân sự, trong đó có ít nhất 2 năm ở vị trí HRBP hoặc HR Manager. Am hiểu sâu sắc về vận hành kinh doanh và tư duy chiến lược con người. Kỹ năng tham vấn (Consulting), huấn luyện (Coaching) và dẫn dắt sự thay đổi tổ chức.",
        "benefits": "Thu nhập xứng tầm chuyên gia. Xe đưa đón công tác. Tham gia các chương trình đào tạo quản trị cấp cao tại nước ngoài.",
        "required_skills": ["HRBP", "Chiến lược nhân sự", "Quản trị nhân lực", "Luật lao động", "Khung năng lực"],
        "preferred_skills": ["Performance Management", "Coaching", "OKRs/KPIs"]
    },

    # --- Nhóm 8: Sales & Business (4 JDs) ---
    {
        "id": "job-seed-30",
        "company_id": "comp-seed-07",
        "creator_id": "user-rec-seed-07",
        "title": "Sales Executive (B2B FMCG)",
        "category": "Sales & Business",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 12000000,
        "salary_max": 25000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Tìm kiếm khách hàng đại lý mới, chào bán danh mục hàng hóa thực phẩm sạch và tiêu dùng nhanh vào các chuỗi nhà hàng, khách sạn và siêu thị tiện lợi trong khu vực phụ trách.",
        "requirements": "Có 1-2 năm kinh nghiệm kinh doanh bán hàng B2B (ưu tiên ngành hàng FMCG, F&B hoặc bán lẻ). Kỹ năng giao tiếp, đàm phán giá và thuyết phục khách hàng tốt. Năng động, chịu khó đi thị trường và hướng tới mục tiêu doanh số.",
        "benefits": "Lương cứng ổn định + Hoa hồng bán hàng theo doanh thu cực kỳ hấp dẫn. Phụ cấp xăng xe và điện thoại hàng tháng.",
        "required_skills": ["Sales", "B2B Sales", "Đàm phán", "Bán hàng", "Chăm sóc khách hàng"],
        "preferred_skills": ["FMCG", "CRM", "Phát triển thị trường"]
    },
    {
        "id": "job-seed-31",
        "company_id": "comp-seed-01",
        "creator_id": "user-rec-seed-01",
        "title": "Business Development Executive (IT SaaS)",
        "category": "Sales & Business",
        "job_type": "full_time",
        "location": "Đà Nẵng",
        "salary_min": 18000000,
        "salary_max": 35000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Khai thác thị trường, tiếp cận các doanh nghiệp có nhu cầu chuyển đổi số và tư vấn bán giải pháp phần mềm tuyển dụng thông minh HireSense AI cho các tập đoàn tại Việt Nam và Đông Nam Á.",
        "requirements": "Từ 2 năm kinh nghiệm phát triển kinh doanh hoặc bán phần mềm B2B (SaaS / Enterprise Software). Kỹ năng demo giải pháp công nghệ tự tin và khả năng thuyết phục khách hàng C-level (CEO, CHRO). Tiếng Anh giao tiếp và đàm phán thương mại trôi chảy.",
        "benefits": "Thu nhập đột phá theo phần trăm hợp đồng ký kết. Làm việc trong môi trường công nghệ cao cấp. Cơ hội thăng tiến lên Head of Business Development.",
        "required_skills": ["Business Development", "B2B Sales", "Đàm phán", "SaaS Sales", "CRM"],
        "preferred_skills": ["Thuyết trình", "Tiếng Anh thương mại", "HubSpot"]
    },
    {
        "id": "job-seed-32",
        "company_id": "comp-seed-04",
        "creator_id": "user-rec-seed-04",
        "title": "Account Manager (Marketing Agency)",
        "category": "Sales & Business",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 20000000,
        "salary_max": 35000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Làm đầu mối liên lạc chính với các nhãn hàng khách hàng lớn, tiếp nhận bản brief yêu cầu truyền thông, phối hợp cùng team Creative/Planning để bảo vệ kế hoạch và đảm bảo sự hài lòng của khách hàng trong suốt chiến dịch.",
        "requirements": "Tối thiểu 3 năm kinh nghiệm trong vai trò Account tại các Marketing/Advertising Agency. Am hiểu quy trình sản xuất chiến dịch quảng cáo và các chỉ số đo lường hiệu quả truyền thông. Kỹ năng quản lý kỳ vọng khách hàng, xử lý khủng hoảng và duy trì quan hệ đối tác bền chặt.",
        "benefits": "Thưởng doanh số dự án duy trì (Account Retention Bonus). Môi trường giao lưu cùng các Brand Manager hàng đầu. Chế độ du lịch và giải trí hàng quý.",
        "required_skills": ["Account Management", "Quản lý khách hàng", "Đàm phán", "Digital Marketing", "Client Relationship"],
        "preferred_skills": ["Briefing", "Project Management", "Thuyết trình"]
    },
    {
        "id": "job-seed-33",
        "company_id": "comp-seed-09",
        "creator_id": "user-rec-seed-09",
        "title": "Customer Success Specialist",
        "category": "Sales & Business",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 14000000,
        "salary_max": 22000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Hướng dẫn học viên và phụ huynh khai thác tối đa nền tảng học trực tuyến, giải quyết các thắc mắc trong quá trình học tập và đồng hành để nâng cao tỷ lệ tái tục khóa học.",
        "requirements": "Có 1-3 năm kinh nghiệm ở vị trí Chăm sóc khách hàng hoặc Customer Success. Giọng nói chuẩn, truyền cảm, kiên nhẫn và tận tâm phục vụ. Kỹ năng sử dụng phần mềm quản lý quan hệ khách hàng (CRM) và xử lý phàn nàn khéo léo.",
        "benefits": "Học bổng tiếng Anh 100% cho bản thân và giảm 50% cho người thân. Thưởng duy trì học viên hàng tháng. Môi trường giáo dục nhân văn.",
        "required_skills": ["Customer Success", "Chăm sóc khách hàng", "Giao tiếp", "CRM", "Xử lý tình huống"],
        "preferred_skills": ["EdTech", "Telesales", "Tiếng Anh"]
    },

    # --- Nhóm 9: Logistics & Chuỗi cung ứng (3 JDs) ---
    {
        "id": "job-seed-34",
        "company_id": "comp-seed-06",
        "creator_id": "user-rec-seed-06",
        "title": "Logistics Coordinator",
        "category": "Logistics",
        "job_type": "full_time",
        "location": "Cần Thơ",
        "salary_min": 12000000,
        "salary_max": 18000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Điều phối kế hoạch vận chuyển hàng hóa nông thủy sản từ vùng nguyên liệu ĐBSCL đến các cảng biển xuất khẩu. Làm việc với đội xe tải, hãng tàu và các đơn vị giao nhận để đảm bảo lịch trình đúng hẹn.",
        "requirements": "Tốt nghiệp Cao đẳng/Đại học chuyên ngành Kinh tế đối ngoại, Logistics hoặc Xuất nhập khẩu. Có từ 1-2 năm kinh nghiệm điều phối vận tải nội địa hoặc quốc tế. Hiểu biết cơ bản về chứng từ vận tải (Bill of Lading, Packing List) và quy tắc Incoterms. Kỹ năng xử lý tình huống phát sinh nhanh nhạy.",
        "benefits": "Phụ cấp điện thoại và ăn ca tại công ty. Thưởng mùa vụ cao điểm nông sản. Bảo hiểm tai nạn 24/24.",
        "required_skills": ["Logistics", "Xuất nhập khẩu", "Incoterms", "Điều phối vận tải", "Chứng từ hàng hóa"],
        "preferred_skills": ["WMS", "Freight Forwarding", "Tiếng Anh thương mại"]
    },
    {
        "id": "job-seed-35",
        "company_id": "comp-seed-06",
        "creator_id": "user-rec-seed-06",
        "title": "Supply Chain Analyst",
        "category": "Logistics",
        "job_type": "full_time",
        "location": "Cần Thơ",
        "salary_min": 18000000,
        "salary_max": 28000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Phân tích số liệu chuỗi cung ứng, dự báo nhu cầu hàng hóa mùa vụ, tối ưu hóa mức tồn kho an toàn và chi phí logistics toàn chuỗi phân phối lạnh (Cold Chain).",
        "requirements": "Có 2-4 năm kinh nghiệm trong lĩnh vực Quản lý chuỗi cung ứng hoặc Phân tích kế hoạch cung ứng. Sử dụng thành thạo phần mềm ERP (SAP/Oracle) và Excel nâng cao. Tư duy phân tích định lượng xuất sắc, nắm chắc phương pháp quản trị tồn kho (EOQ, Safety Stock, JIT).",
        "benefits": "Cơ hội tham gia các dự án tự động hóa chuỗi cung ứng lớn nhất miền Tây. Lương tháng 13 + thưởng hoàn thành mục tiêu tiết giảm chi phí.",
        "required_skills": ["Chuỗi cung ứng", "Supply Chain", "Phân tích dữ liệu", "Excel", "Quản lý tồn kho"],
        "preferred_skills": ["ERP", "SAP", "WMS"]
    },
    {
        "id": "job-seed-36",
        "company_id": "comp-seed-06",
        "creator_id": "user-rec-seed-06",
        "title": "Warehouse Supervisor",
        "category": "Logistics",
        "job_type": "full_time",
        "location": "Cần Thơ",
        "salary_min": 15000000,
        "salary_max": 24000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Giám sát toàn bộ hoạt động nhập - xuất - lưu trữ tại tổng kho logistics diện tích 10,000 m2. Quản lý đội ngũ nhân viên kho và tài xế xe nâng, đảm bảo an toàn lao động và độ chính xác tồn kho tuyệt đối.",
        "requirements": "3+ năm kinh nghiệm quản lý kho hàng quy mô lớn. Thành thạo phần mềm quản lý kho (WMS) và mã vạch Barcode/RFID. Có kỹ năng tổ chức sắp xếp kho theo chuẩn 5S và phòng cháy chữa cháy (PCCC). Kỹ năng lãnh đạo và quản lý đội nhóm công nhân tốt.",
        "benefits": "Trợ cấp phụ cấp trách nhiệm kho vận. Thưởng kiểm kê chính xác hàng quý. Cơ hội đào tạo lên Giám đốc Kho vận.",
        "required_skills": ["Quản lý kho", "WMS", "5S", "Kiểm kê hàng hóa", "An toàn lao động"],
        "preferred_skills": ["TMS", "Quản lý đội ngũ", "ERP"]
    },

    # --- Nhóm 10: Du lịch & Khách sạn (3 JDs) ---
    {
        "id": "job-seed-37",
        "company_id": "comp-seed-08",
        "creator_id": "user-rec-seed-08",
        "title": "Nhân viên lễ tân khách sạn 5 sao",
        "category": "Tourism & Hospitality",
        "job_type": "full_time",
        "location": "Huế",
        "salary_min": 9000000,
        "salary_max": 15000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Thực hiện thủ tục Check-in, Check-out chuyên nghiệp cho khách lưu trú quốc tế và nội địa. Cung cấp thông tin du lịch di sản Huế, tiếp nhận và xử lý các yêu cầu của khách hàng nhằm mang lại trải nghiệm nghỉ dưỡng hoàn hảo.",
        "requirements": "Tốt nghiệp Cao đẳng/Đại học chuyên ngành Quản trị Khách sạn, Du lịch hoặc Ngoại ngữ. Tiếng Anh giao tiếp lưu loát (tương đương TOEIC 700+ hoặc IELTS 6.0+). Ngoại hình sáng, tác phong chỉn chu, nụ cười thân thiện. Biết sử dụng phần mềm quản lý khách sạn Opera PMS là lợi thế lớn.",
        "benefits": "Hưởng phí dịch vụ (Service Charge) hàng tháng hấp dẫn. Cung cấp đồng phục và bữa ăn trong ca làm việc. Chế độ nghỉ dưỡng miễn phí tại các khách sạn thuộc tập đoàn SunPeak.",
        "required_skills": ["Lễ tân", "Hospitality Management", "Tiếng Anh giao tiếp", "Customer Service", "Check-in/Check-out"],
        "preferred_skills": ["Opera PMS", "Giao tiếp ngoại ngữ", "Xử lý phàn nàn"]
    },
    {
        "id": "job-seed-38",
        "company_id": "comp-seed-08",
        "creator_id": "user-rec-seed-08",
        "title": "Travel Consultant (Tour Outbound & Inbound)",
        "category": "Tourism & Hospitality",
        "job_type": "full_time",
        "location": "Huế",
        "salary_min": 11000000,
        "salary_max": 20000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Tư vấn lộ trình du lịch văn hóa, lịch sử và ẩm thực cho khách du lịch cá nhân và đoàn thể. Thiết kế tour trọn gói theo yêu cầu (Customized Tour), báo giá và phối hợp với hướng dẫn viên điều hành tour an toàn.",
        "requirements": "1-2 năm kinh nghiệm trong vai trò Tư vấn tour du lịch hoặc Điều hành tour. Am hiểu sâu sắc về danh lam thắng cảnh, văn hóa cố đô Huế và các tỉnh miền Trung. Kỹ năng giao tiếp và thuyết phục khách hàng tốt. Sử dụng tiếng Anh tốt cả 4 kỹ năng.",
        "benefits": "Thu nhập gồm Lương cơ bản + Hoa hồng bán tour không giới hạn. Cơ hội đi khảo sát tuyến điểm du lịch (Famtrip) miễn phí định kỳ.",
        "required_skills": ["Tư vấn du lịch", "Thiết kế tour", "Customer Service", "Tiếng Anh", "Booking Management"],
        "preferred_skills": ["Điều hành tour", "Đàm phán", "Kỹ năng thuyết phục"]
    },
    {
        "id": "job-seed-39",
        "company_id": "comp-seed-08",
        "creator_id": "user-rec-seed-08",
        "title": "Hotel Operations Supervisor",
        "category": "Tourism & Hospitality",
        "job_type": "full_time",
        "location": "Huế",
        "salary_min": 18000000,
        "salary_max": 28000000,
        "currency": "VND",
        "experience_level": "senior",
        "status": "published",
        "description": "Giám sát vận hành hàng ngày của khối phòng lưu trú và ẩm thực (Front Office & Housekeeping), đảm bảo các tiêu chuẩn dịch vụ 5 sao được duy trì nhất quán, đào tạo nhân sự và giải quyết các trường hợp khách VIP.",
        "requirements": "Tối thiểu 4 năm kinh nghiệm làm việc trong ngành khách sạn nghỉ dưỡng cao cấp, trong đó có 2 năm ở vị trí giám sát. Nắm vững quy trình vận hành tiêu chuẩn (SOP). Khả năng lãnh đạo và xử lý tình huống khẩn cấp bình tĩnh, thấu tình đạt lý.",
        "benefits": "Gói đãi ngộ cấp quản lý. Thưởng doanh thu khách sạn. Cơ hội thăng tiến lên Trưởng bộ phận Tiền sảnh (FOM) hoặc Giám đốc Điều hành.",
        "required_skills": ["Hospitality Management", "Quản lý khách sạn", "SOP", "Opera PMS", "Đào tạo nhân viên"],
        "preferred_skills": ["Xử lý khủng hoảng", "Tiếng Anh lưu loát", "Quản trị doanh thu"]
    },

    # --- Nhóm 11: Giáo dục & Đào tạo (3 JDs) ---
    {
        "id": "job-seed-40",
        "company_id": "comp-seed-09",
        "creator_id": "user-rec-seed-09",
        "title": "Giáo viên tiếng Anh IELTS",
        "category": "Education",
        "job_type": "part_time",
        "location": "Hà Nội",
        "salary_min": 18000000,
        "salary_max": 35000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Giảng dạy các lớp luyện thi chứng chỉ IELTS mục tiêu 6.5 - 8.0 cho học sinh, sinh viên và người đi làm. Chấm bài viết (Writing Task 1 & 2), rèn luyện kỹ năng Nói (Speaking) và truyền cảm hứng học tập chủ động.",
        "requirements": "Tốt nghiệp Đại học chuyên ngành Sư phạm tiếng Anh, Ngôn ngữ Anh hoặc du học sinh. Có chứng chỉ IELTS Academic từ 7.5 trở lên (không kỹ năng nào dưới 7.0) và chứng chỉ giảng dạy quốc tế (TESOL, CELTA, TEFL). Ít nhất 2 năm kinh nghiệm luyện thi IELTS thực tế với tỷ lệ học viên đạt mục tiêu cao.",
        "benefits": "Thu nhập theo giờ giảng dạy cạnh tranh (400,000 - 700,000 VND/giờ). Thưởng điểm số học viên đạt target. Giáo trình điện tử và học liệu số có sẵn chuẩn quốc tế.",
        "required_skills": ["English Teaching", "IELTS", "TESOL", "Soạn giáo án", "Quản lý lớp học"],
        "preferred_skills": ["CELTA", "Public Speaking", "EdTech"]
    },
    {
        "id": "job-seed-41",
        "company_id": "comp-seed-09",
        "creator_id": "user-rec-seed-09",
        "title": "Chuyên viên đào tạo doanh nghiệp (Corporate Trainer)",
        "category": "Education",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 20000000,
        "salary_max": 32000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Khảo sát nhu cầu đào tạo (TNA) của các khách hàng doanh nghiệp, thiết kế khung chương trình đào tạo kỹ năng mềm và kỹ năng số, trực tiếp đứng lớp điều phối các workshop phát triển năng lực lãnh đạo.",
        "requirements": "Tối thiểu 3 năm kinh nghiệm trong mảng L&D (Learning & Development) hoặc đào tạo doanh nghiệp. Khả năng thiết kế bài giảng tương tác cao, sử dụng thành thạo các phương pháp đào tạo hiện đại (Experiential Learning, Gamification). Kỹ năng đứng trước đám đông lôi cuốn, truyền cảm hứng.",
        "benefits": "Môi trường giao lưu cùng các diễn giả và chuyên gia hàng đầu. Thưởng hợp đồng đào tạo doanh nghiệp thành công. Chế độ công tác phí đầy đủ.",
        "required_skills": ["Corporate Training", "Đào tạo", "TNA", "Kỹ năng mềm", "Thiết kế khóa học"],
        "preferred_skills": ["Public Speaking", "Coaching", "Instructional Design"]
    },
    {
        "id": "job-seed-42",
        "company_id": "comp-seed-09",
        "creator_id": "user-rec-seed-09",
        "title": "Academic Coordinator",
        "category": "Education",
        "job_type": "full_time",
        "location": "Hà Nội",
        "salary_min": 13000000,
        "salary_max": 20000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Điều phối học vụ, sắp xếp lịch giảng dạy của giáo viên nước ngoài và giáo viên Việt Nam, tổ chức các kỳ thi thử và kiểm tra định kỳ, theo dõi tiến độ học tập và tiếp nhận phản hồi từ học viên.",
        "requirements": "Tốt nghiệp Đại học ngành Sư phạm, Ngoại ngữ hoặc Quản lý Giáo dục. Tiếng Anh giao tiếp tốt để làm việc trực tiếp với giáo viên bản xứ. Kỹ năng tổ chức sắp xếp công việc khoa học, chi tiết, thành thạo tin học văn phòng.",
        "benefits": "Môi trường làm việc đa văn hóa, sử dụng tiếng Anh hàng ngày. Cơ hội học tập và thăng tiến lên Trưởng phòng Học vụ. Giờ làm việc ổn định.",
        "required_skills": ["Quản lý học vụ", "Tiếng Anh giao tiếp", "Sắp xếp lịch trình", "Excel", "Customer Service"],
        "preferred_skills": ["Education Management", "EdTech", "Tổ chức sự kiện"]
    },

    # --- Nhóm 12: Xây dựng & Sản xuất (4 JDs) ---
    {
        "id": "job-seed-43",
        "company_id": "comp-seed-10",
        "creator_id": "user-rec-seed-10",
        "title": "Kỹ sư xây dựng kết cấu",
        "category": "Construction & Manufacturing",
        "job_type": "full_time",
        "location": "Hải Phòng",
        "salary_min": 18000000,
        "salary_max": 30000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Thực hiện tính toán mô hình kết cấu bê tông cốt thép và kết cấu thép cho các công trình nhà xưởng công nghiệp và hạ tầng cảng biển. Thiết kế bản vẽ thi công và bảo vệ phương án kết cấu trước chủ đầu tư.",
        "requirements": "Tốt nghiệp Đại học Xây dựng, Kiến trúc hoặc Bách Khoa chuyên ngành Xây dựng Dân dụng & Công nghiệp. Có từ 3 năm kinh nghiệm tính toán kết cấu. Sử dụng thành thạo phần mềm chuyên ngành: AutoCAD, Etabs, SAFE, SAP2000 và Revit Structure. Nắm chắc các Tiêu chuẩn Xây dựng Việt Nam (TCVN) và tiêu chuẩn quốc tế (AISC, ACI).",
        "benefits": "Lương tháng 13 + thưởng hoàn thành tiến độ công trình. Phụ cấp công trình xa và nhà ở công vụ. Đóng bảo hiểm đầy đủ.",
        "required_skills": ["Kỹ sư xây dựng", "AutoCAD", "Etabs", "Kết cấu xây dựng", "Bóc tách khối lượng"],
        "preferred_skills": ["Revit", "SAP2000", "TCVN"]
    },
    {
        "id": "job-seed-44",
        "company_id": "comp-seed-13",
        "creator_id": "user-rec-seed-13",
        "title": "Mechanical Engineer (Kỹ sư cơ khí chế tạo)",
        "category": "Construction & Manufacturing",
        "job_type": "full_time",
        "location": "Hải Phòng",
        "salary_min": 16000000,
        "salary_max": 26000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "published",
        "description": "Thiết kế chi tiết linh kiện máy móc, khuôn mẫu cơ khí chính xác bằng phần mềm 3D CAD/CAM. Giám sát quá trình gia công cơ khí trên máy CNC và tối ưu hóa quy trình sản xuất cơ khí chính xác.",
        "requirements": "Tốt nghiệp chuyên ngành Cơ khí chế tạo máy, Cơ điện tử. Có 2-4 năm kinh nghiệm thiết kế cơ khí. Sử dụng thành thạo phần mềm SolidWorks hoặc Inventor và AutoCAD. Hiểu biết sâu về dung sai lắp ghép, vật liệu cơ khí và công nghệ gia công kim loại.",
        "benefits": "Làm việc tại nhà máy công nghệ cao hiện đại. Xe đưa đón hàng ngày từ trung tâm Hải Phòng. Phụ cấp độc hại và trợ cấp thâm niên kỹ thuật.",
        "required_skills": ["Kỹ sư cơ khí", "SolidWorks", "AutoCAD", "Gia công cơ khí", "CNC"],
        "preferred_skills": ["Inventor", "CAM", "Khuôn mẫu"]
    },
    {
        "id": "job-seed-45",
        "company_id": "comp-seed-13",
        "creator_id": "user-rec-seed-13",
        "title": "Quality Assurance (QA/QC) Engineer",
        "category": "Construction & Manufacturing",
        "job_type": "full_time",
        "location": "Hải Phòng",
        "salary_min": 14000000,
        "salary_max": 22000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "published",
        "description": "Kiểm soát chất lượng linh kiện đầu vào (IQC), kiểm tra quy trình công đoạn sản xuất (IPQC) và kiểm tra chất lượng thành phẩm xuất xưởng (OQC) theo hệ thống quản lý chất lượng ISO 9001 và 5S.",
        "requirements": "Có 1-3 năm kinh nghiệm làm QA/QC tại các nhà máy sản xuất linh kiện điện tử hoặc cơ khí. Sử dụng thành thạo các dụng cụ đo lường chính xác (thước cặp, panme, máy đo 2D/3D CMM). Nắm chắc 7 công cụ quản lý chất lượng (7 QC Tools) và tinh thần làm việc tỉ mỉ.",
        "benefits": "Cơm trưa miễn phí tại nhà ăn công ty. Phụ cấp chuyên cần và đồng phục bảo hộ lao động cao cấp. Cơ hội đào tạo chứng chỉ Lead Auditor ISO.",
        "required_skills": ["QA/QC", "ISO 9001", "5S", "Kiểm tra chất lượng", "Dụng cụ đo lường"],
        "preferred_skills": ["Six Sigma", "7 QC Tools", "Tiếng Anh kỹ thuật"]
    },
    {
        "id": "job-seed-46",
        "company_id": "comp-seed-13",
        "creator_id": "user-rec-seed-13",
        "title": "Production Supervisor (Giám sát sản xuất)",
        "category": "Construction & Manufacturing",
        "job_type": "full_time",
        "location": "Hải Phòng",
        "salary_min": 20000000,
        "salary_max": 32000000,
        "currency": "VND",
        "experience_level": "senior",
        "status": "pending_approval",
        "description": "Chịu trách nhiệm quản lý toàn bộ ca sản xuất với hơn 100 công nhân, phân bổ kế hoạch sản xuất hàng ngày, kiểm soát tỷ lệ phế phẩm (Scrap Rate) và thúc đẩy cải tiến liên tục theo phương pháp Kaizen và Lean Manufacturing.",
        "requirements": "Tối thiểu 4 năm kinh nghiệm trong môi trường sản xuất công nghiệp, trong đó có 2 năm ở vai trò Giám sát ca sản xuất. Kỹ năng quản lý nhân sự sản xuất, lập kế hoạch chi tiết và ứng phó sự cố ngừng chuyền sản xuất nhanh chóng.",
        "benefits": "Lương bổng thỏa thuận xứng đáng. Thưởng vượt định mức sản lượng hàng tháng. Chế độ bảo hiểm bảo an toàn diện.",
        "required_skills": ["Giám sát sản xuất", "Lean Manufacturing", "5S", "Kaizen", "Quản lý nhân lực"],
        "preferred_skills": ["ISO 9001", "Six Sigma", "An toàn lao động"]
    },

    # --- Nhóm 13: Y tế & Chăm sóc sức khỏe (2 JDs) ---
    {
        "id": "job-seed-47",
        "company_id": "comp-seed-11",
        "creator_id": "user-rec-seed-11",
        "title": "Nhân viên điều phối y tế (Clinical Coordinator)",
        "category": "Healthcare Services",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 14000000,
        "salary_max": 22000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "pending_approval",
        "description": "Tiếp nhận thông tin bệnh nhân, điều phối lịch hẹn khám chuyên khoa, hướng dẫn bệnh nhân thực hiện các quy trình cận lâm sàng và phối hợp với đội ngũ bác sĩ nhằm đảm bảo quy trình khám chữa bệnh liên tục, chu đáo.",
        "requirements": "Tốt nghiệp chuyên ngành Y tế công cộng, Điều dưỡng hoặc Quản lý Bệnh viện. Có từ 1-3 năm kinh nghiệm làm việc tại phòng khám hoặc bệnh viện đa khoa. Nắm chắc quy trình khám chữa bệnh và thuật ngữ y khoa cơ bản. Giao tiếp nhã nhặn, thấu cảm và có tâm với người bệnh.",
        "benefits": "Gói bảo hiểm chăm sóc sức khỏe y tế chất lượng cao. Khám sức khỏe định kỳ miễn phí cho người thân tại hệ thống phòng khám HealthBridge. Thưởng ngày Thầy thuốc Việt Nam.",
        "required_skills": ["Clinical Coordination", "Điều phối y tế", "Chăm sóc bệnh nhân", "Thuật ngữ y khoa", "Giao tiếp"],
        "preferred_skills": ["HIS", "Bảo hiểm y tế", "Tiếng Anh y khoa"]
    },
    {
        "id": "job-seed-48",
        "company_id": "comp-seed-11",
        "creator_id": "user-rec-seed-11",
        "title": "Chuyên viên quản lý hồ sơ y tế điện tử (EMR Specialist)",
        "category": "Healthcare Services",
        "job_type": "full_time",
        "location": "TP.HCM",
        "salary_min": 15000000,
        "salary_max": 24000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "pending_approval",
        "description": "Quản trị và số hóa hệ thống hồ sơ bệnh án điện tử (EMR/HIS), bảo đảm tính bảo mật dữ liệu sức khỏe bệnh nhân, mã hóa chẩn đoán bệnh theo chuẩn quốc tế ICD-10 và hỗ trợ trích xuất dữ liệu phục vụ báo cáo Sở Y tế.",
        "requirements": "Tốt nghiệp ngành Tin học Y tế, Công nghệ Thông tin hoặc Quản trị Y tế. Có 2 năm kinh nghiệm quản lý phần mềm bệnh viện (HIS/LIS/PACS). Hiểu biết về bảo mật thông tin y tế và quy định lưu trữ hồ sơ bệnh án. Kỹ năng thống kê dữ liệu cẩn thận, chính xác.",
        "benefits": "Môi trường y tế số hóa hiện đại hàng đầu. Thưởng hoàn thành dự án chuyển đổi số y tế. Cơ hội nâng cao trình độ chuyên môn.",
        "required_skills": ["Medical Records", "HIS", "Quản lý hồ sơ y tế", "ICD-10", "Bảo mật dữ liệu"],
        "preferred_skills": ["SQL", "LIS", "Bảo hiểm y tế"]
    },

    # --- Nhóm 14: Nông nghiệp công nghệ cao & Môi trường (2 JDs) ---
    {
        "id": "job-seed-49",
        "company_id": "comp-seed-15",
        "creator_id": "user-rec-seed-15",
        "title": "Agricultural Technology Specialist",
        "category": "Agriculture & Environment",
        "job_type": "full_time",
        "location": "Cần Thơ",
        "salary_min": 15000000,
        "salary_max": 25000000,
        "currency": "VND",
        "experience_level": "mid",
        "status": "pending_approval",
        "description": "Vận hành và chuyển giao công nghệ hệ thống nhà màng nông nghiệp thông minh, điều khiển hệ thống tưới nhỏ giọt tự động qua cảm biến IoT, theo dõi dinh dưỡng cây trồng và kiểm soát quy trình sản xuất đạt chuẩn VietGAP.",
        "requirements": "Tốt nghiệp Đại học ngành Nông nghiệp công nghệ cao, Khoa học Cây trồng hoặc Nông học. 2-3 năm kinh nghiệm thực tế tại các nông trại công nghệ cao. Am hiểu sinh lý cây trồng, dinh dưỡng thủy canh và phòng trừ dịch hại tổng hợp (IPM). Có khả năng làm việc tại trang trại thực nghiệm.",
        "benefits": "Cung cấp chỗ ở tại trang trại sinh thái thông minh. Thưởng mùa vụ thu hoạch nông sản chất lượng cao. Cơ hội tiếp cận các công nghệ nông nghiệp Israel tiên tiến.",
        "required_skills": ["Smart Agriculture", "Nông nghiệp công nghệ cao", "VietGAP", "Irrigation Systems", "Pest Management"],
        "preferred_skills": ["IoT nông nghiệp", "GlobalGAP", "Thủy canh"]
    },
    {
        "id": "job-seed-50",
        "company_id": "comp-seed-15",
        "creator_id": "user-rec-seed-15",
        "title": "Environmental Project Coordinator",
        "category": "Agriculture & Environment",
        "job_type": "full_time",
        "location": "Cần Thơ",
        "salary_min": 14000000,
        "salary_max": 22000000,
        "currency": "VND",
        "experience_level": "junior",
        "status": "pending_approval",
        "description": "Điều phối các dự án bảo vệ môi trường, giảm phát thải khí nhà kính trong canh tác lúa gạo, theo dõi chứng chỉ tín chỉ carbon nông nghiệp và phối hợp với các tổ chức phi chính phủ (NGO) triển khai mô hình kinh tế tuần hoàn.",
        "requirements": "Tốt nghiệp ngành Quản lý Môi trường, Biến đổi Khí hậu hoặc Khoa học Đất. Có 1-3 năm kinh nghiệm điều phối dự án phát triển nông thôn hoặc môi trường. Kỹ năng giao tiếp cộng đồng và kỹ năng viết báo cáo tiến độ dự án bằng tiếng Anh tốt.",
        "benefits": "Làm việc với các chuyên gia quốc tế về biến đổi khí hậu. Trợ cấp đi lại công tác thực địa. Cơ hội tham gia hội nghị khí hậu COP khu vực.",
        "required_skills": ["Quản lý dự án môi trường", "Biến đổi khí hậu", "Báo cáo dự án", "Tiếng Anh", "Kinh tế tuần hoàn"],
        "preferred_skills": ["Tín chỉ Carbon", "GIS", "Phát triển bền vững"]
    }
]
# ==========================================
# 4. 30 CANDIDATE PROFILES & CV DEFINITIONS
# ==========================================
CANDIDATES_DATA = [
    # --- Case A: High Match (5 CVs) ---
    {
        "id": "cand-seed-01",
        "email": "candidate01@example.test",
        "full_name": "Nguyễn Đình Khang",
        "phone": "0901001001",
        "target_job_id": "job-seed-02",  # Senior React & TS
        "file_type": "pdf",
        "file_name": "CV01_Nguyen_Dinh_Khang_Senior_React.pdf",
        "test_case": "Case A - High Match",
        "title": "Senior React & TypeScript Developer",
        "summary": "Kỹ sư Frontend với hơn 5 năm kinh nghiệm chuyên sâu về React, TypeScript, Next.js và kiến trúc Design System quy mô lớn. Tối ưu hiệu năng Web Core Vitals và dẫn dắt đội ngũ kỹ thuật phát triển sản phẩm SaaS.",
        "education": [
            {
                "institution": "Đại học Bách Khoa Đà Nẵng",
                "degree": "Kỹ sư",
                "field_of_study": "Công nghệ Thông tin",
                "start_date": "2015",
                "end_date": "2020",
                "gpa": "3.5/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "FPT Software Đà Nẵng",
                "job_title": "Senior Frontend Engineer",
                "start_date": "06/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Chịu trách nhiệm kiến trúc Frontend sử dụng React, TypeScript và Next.js. Tối ưu hóa bundle size giảm 35%, tích hợp CI/CD tự động hóa kiểm thử bằng Jest và Cypress."
            },
            {
                "company_name": "Enclave Technology",
                "job_title": "Frontend Developer",
                "start_date": "01/2020",
                "end_date": "05/2021",
                "is_current": False,
                "description": "Phát triển giao diện ứng dụng web thương mại điện tử với ReactJS, Redux Toolkit, Tailwind CSS và RESTful API."
            }
        ],
        "hard_skills": ["React", "TypeScript", "Next.js", "Redux", "CI/CD", "Git", "Tailwind CSS"],
        "soft_skills": ["Lãnh đạo đội nhóm", "Giao tiếp tiếng Anh", "Tư duy giải quyết vấn đề"],
        "certifications": ["AWS Certified Cloud Practitioner", "Meta Front-End Developer Professional Certificate"],
        "expected_match_range": [85, 98],
        "expected_evaluation": "Rất phù hợp (High Match): Đầy đủ các kỹ năng cốt lõi React, TypeScript, Next.js, Redux, CI/CD và trên 5 năm kinh nghiệm thực tế."
    },
    {
        "id": "cand-seed-02",
        "email": "candidate02@example.test",
        "full_name": "Lê Hoàng Long",
        "phone": "0901001002",
        "target_job_id": "job-seed-03",  # Python Backend Developer
        "file_type": "docx",
        "file_name": "CV02_Le_Hoang_Long_Python_Backend.docx",
        "test_case": "Case A - High Match",
        "title": "Middle Python Backend Developer",
        "summary": "Lập trình viên Backend với 3 năm kinh nghiệm phát triển microservices hiệu năng cao sử dụng Python, FastAPI, PostgreSQL và Docker. Đam mê thiết kế cơ sở dữ liệu tối ưu và hệ thống xử lý bất đồng bộ.",
        "education": [
            {
                "institution": "Đại học Sư phạm Kỹ thuật TP.HCM",
                "degree": "Cử nhân",
                "field_of_study": "Khoa học Máy tính",
                "start_date": "2017",
                "end_date": "2021",
                "gpa": "3.3/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "KMS Technology",
                "job_title": "Python Backend Engineer",
                "start_date": "08/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Thiết kế RESTful APIs bằng FastAPI và SQLAlchemy. Tối ưu câu lệnh truy vấn PostgreSQL, cấu hình cache Redis tăng tốc độ phản hồi API lên 40%. Triển khai container hóa ứng dụng qua Docker."
            }
        ],
        "hard_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "Redis", "Git", "SQL"],
        "soft_skills": ["Làm việc nhóm", "Quản lý thời gian", "Chủ động học hỏi"],
        "certifications": ["Certified Entry-Level Python Programmer (PCEP)"],
        "expected_match_range": [85, 96],
        "expected_evaluation": "Rất phù hợp (High Match): Đáp ứng 100% kỹ năng bắt buộc Python, FastAPI, PostgreSQL, Docker, Redis và đúng cấp bậc kinh nghiệm."
    },
    {
        "id": "cand-seed-03",
        "email": "candidate03@example.test",
        "full_name": "Trần Thu Hà",
        "phone": "0901001003",
        "target_job_id": "job-seed-16",  # Kế toán tổng hợp
        "file_type": "pdf",
        "file_name": "CV03_Tran_Thu_Ha_Ke_Toan_Tong_Hop.pdf",
        "test_case": "Case A - High Match",
        "title": "Chuyên viên Kế toán tổng hợp",
        "summary": "Kế toán viên tổng hợp với hơn 4 năm kinh nghiệm làm việc tại doanh nghiệp dịch vụ tài chính. Thành thạo lập báo cáo tài chính, quyết toán thuế GTGT, TNDN, TNCN và sử dụng chuyên sâu phần mềm MISA, Excel.",
        "education": [
            {
                "institution": "Đại học Kinh tế TP.HCM (UEH)",
                "degree": "Cử nhân",
                "field_of_study": "Kế toán Doanh nghiệp",
                "start_date": "2016",
                "end_date": "2020",
                "gpa": "3.6/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty TNHH Đầu tư Tài chính Á Châu",
                "job_title": "Kế toán tổng hợp",
                "start_date": "10/2020",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Kiểm soát toàn bộ định khoản kế toán, lập báo cáo tài chính năm theo chuẩn mực VAS. Trực tiếp làm việc với cơ quan thuế quận 1 trong các kỳ quyết toán thuế định kỳ. Quản lý hệ thống chứng từ trên MISA SME."
            }
        ],
        "hard_skills": ["Kế toán tổng hợp", "Báo cáo tài chính", "Kế toán thuế", "MISA", "Excel", "VAS"],
        "soft_skills": ["Cẩn thận", "Trung thực", "Chính xác", "Chịu áp lực tốt"],
        "certifications": ["Chứng chỉ Kế toán trưởng", "Chứng chỉ Tin học văn phòng MOS Excel Expert"],
        "expected_match_range": [85, 98],
        "expected_evaluation": "Rất phù hợp (High Match): Đạt trọn vẹn yêu cầu Kế toán tổng hợp, Báo cáo tài chính, MISA, Kế toán thuế và có chứng chỉ chuyên môn cao."
    },
    {
        "id": "cand-seed-04",
        "email": "candidate04@example.test",
        "full_name": "Phạm Gia Bảo",
        "phone": "0901001004",
        "target_job_id": "job-seed-20",  # Digital Marketing Specialist
        "file_type": "docx",
        "file_name": "CV04_Pham_Gia_Bao_Digital_Marketing.docx",
        "test_case": "Case A - High Match",
        "title": "Digital Performance Marketing Specialist",
        "summary": "Chuyên viên Digital Marketing 3 năm kinh nghiệm thực chiến tối ưu hóa quảng cáo chuyển đổi trên Google Ads và Meta Ads. Quản trị ngân sách trên 500 triệu/tháng với ROAS trung bình 4.5.",
        "education": [
            {
                "institution": "Đại học Ngoại Thương Cơ sở 2",
                "degree": "Cử nhân",
                "field_of_study": "Marketing & Kinh doanh Quốc tế",
                "start_date": "2017",
                "end_date": "2021",
                "gpa": "3.4/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Ogilvy Vietnam Partner",
                "job_title": "Digital Marketing Executive",
                "start_date": "07/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Thiết lập và vận hành chiến dịch Google Search, GDN, Facebook Conversion Ads. Phân tích phễu chuyển đổi trên Google Analytics 4 và tối ưu hóa chi phí CPA."
            }
        ],
        "hard_skills": ["Digital Marketing", "Facebook Ads", "Google Ads", "Google Analytics", "SEM", "A/B Testing"],
        "soft_skills": ["Tư duy số liệu", "Sáng tạo thông điệp", "Quản lý ngân sách"],
        "certifications": ["Google Ads Search Certification", "Google Analytics (GA4) Certification"],
        "expected_match_range": [85, 96],
        "expected_evaluation": "Rất phù hợp (High Match): Đầy đủ công cụ Digital Marketing, Facebook Ads, Google Ads, GA4 và có kinh nghiệm thực tế tại Agency uy tín."
    },
    {
        "id": "cand-seed-05",
        "email": "candidate05@example.test",
        "full_name": "Đặng Thùy Dung",
        "phone": "0901001005",
        "target_job_id": "job-seed-25",  # UI/UX Designer
        "file_type": "pdf",
        "file_name": "CV05_Dang_Thuy_Dung_UI_UX_Designer.pdf",
        "test_case": "Case A - High Match",
        "title": "Product Designer (UI/UX)",
        "summary": "Nhà thiết kế sản phẩm số (UI/UX) với 3 năm kinh nghiệm thiết kế ứng dụng di động Fintech và Web App. Thành thạo quy trình Design Thinking từ User Research, Wireframing đến xây dựng Design System hoàn chỉnh trên Figma.",
        "education": [
            {
                "institution": "Đại học Kiến Trúc Đà Nẵng",
                "degree": "Cử nhân",
                "field_of_study": "Thiết kế Đồ họa & Mỹ thuật Đa phương tiện",
                "start_date": "2017",
                "end_date": "2021",
                "gpa": "3.5/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Paradox Vietnam",
                "job_title": "UI/UX Designer",
                "start_date": "08/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Chịu trách nhiệm thiết kế trải nghiệm người dùng cho ứng dụng quản trị nhân sự. Xây dựng bộ Design System với hơn 200 components đồng nhất trên Figma. Phối hợp chặt chẽ cùng kỹ sư Frontend."
            }
        ],
        "hard_skills": ["Figma", "UI/UX", "Wireframing", "Prototyping", "User Research", "Design System"],
        "soft_skills": ["Đồng cảm người dùng", "Trình bày giải pháp", "Phản biện thiết kế"],
        "certifications": ["Google UX Design Professional Certificate"],
        "expected_match_range": [85, 98],
        "expected_evaluation": "Rất phù hợp (High Match): Sở hữu toàn bộ kỹ năng Figma, Wireframing, Prototyping, Design System và chứng chỉ Google UX uy tín."
    },

    # --- Case B: Medium Match (5 CVs) ---
    {
        "id": "cand-seed-06",
        "email": "candidate06@example.test",
        "full_name": "Vũ Đức Thịnh",
        "phone": "0901001006",
        "target_job_id": "job-seed-07",  # AI Engineer
        "file_type": "pdf",
        "file_name": "CV06_Vu_Duc_Thinh_AI_Junior.pdf",
        "test_case": "Case B - Medium Match",
        "title": "Junior AI / Data Developer",
        "summary": "Kỹ sư AI triển vọng có nền tảng vững chắc về Python, Machine Learning truyền thống và phân tích dữ liệu. Đã tham gia các dự án nhận diện hình ảnh và xử lý dữ liệu bảng nhưng chưa có nhiều kinh nghiệm chuyên sâu với kiến trúc RAG và LLMs.",
        "education": [
            {
                "institution": "Đại học Quốc gia Hà Nội",
                "degree": "Cử nhân",
                "field_of_study": "Khoa học Dữ liệu",
                "start_date": "2019",
                "end_date": "2023",
                "gpa": "3.2/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Viettel AI Lab (Thực tập)",
                "job_title": "Junior Data / AI Intern",
                "start_date": "06/2023",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Tiền xử lý tập dữ liệu lớn, huấn luyện các mô hình Scikit-learn và cơ bản về PyTorch phân loại hình ảnh. Viết script trích xuất dữ liệu bằng Python."
            }
        ],
        "hard_skills": ["Python", "Machine Learning", "Scikit-learn", "SQL", "Pandas"],
        "soft_skills": ["Nhiệt tình", "Chăm chỉ", "Ham học hỏi"],
        "certifications": ["IBM Data Science Professional Certificate"],
        "expected_match_range": [50, 70],
        "expected_evaluation": "Phù hợp một phần (Medium Match): Có nền tảng Python và Machine Learning, nhưng thiếu các kỹ năng bắt buộc cao cấp như RAG, LLMs và kinh nghiệm chuyên sâu."
    },
    {
        "id": "cand-seed-07",
        "email": "candidate07@example.test",
        "full_name": "Ngô Bảo Ngọc",
        "phone": "0901001007",
        "target_job_id": "job-seed-34",  # Logistics Coordinator
        "file_type": "docx",
        "file_name": "CV07_Ngo_Bao_Ngoc_Logistics_Basic.docx",
        "test_case": "Case B - Medium Match",
        "title": "Nhân viên Giao nhận vận tải",
        "summary": "1.5 năm kinh nghiệm làm thủ tục giao nhận hàng hóa nội địa và xuất nhập khẩu tại kho bãi Cần Thơ. Nắm chắc Incoterms và chứng từ vận tải, tuy nhiên chưa có kinh nghiệm điều phối qua hệ thống phần mềm WMS chuyên nghiệp.",
        "education": [
            {
                "institution": "Đại học Cần Thơ",
                "degree": "Cử nhân",
                "field_of_study": "Kinh doanh Quốc tế",
                "start_date": "2018",
                "end_date": "2022",
                "gpa": "3.1/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty Giao nhận Vận tải Miền Tây",
                "job_title": "Nhân viên Điều vận",
                "start_date": "07/2022",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Lập lệnh điều xe tải chở nông sản, kiểm tra Packing List và Invoice, theo dõi thời gian giao nhận hàng tại các điểm tập kết."
            }
        ],
        "hard_skills": ["Logistics", "Xuất nhập khẩu", "Incoterms", "Chứng từ hàng hóa", "Excel"],
        "soft_skills": ["Giao tiếp", "Xử lý tình huống", "Linh hoạt"],
        "certifications": [],
        "expected_match_range": [55, 72],
        "expected_evaluation": "Phù hợp một phần (Medium Match): Có kỹ năng Logistics, Incoterms và chứng từ, nhưng thiếu phần mềm WMS và tiếng Anh thương mại lưu loát."
    },
    {
        "id": "cand-seed-08",
        "email": "candidate08@example.test",
        "full_name": "Đỗ Quang Huy",
        "phone": "0901001008",
        "target_job_id": "job-seed-12",  # DevOps Engineer
        "file_type": "pdf",
        "file_name": "CV08_Do_Quang_Huy_DevOps_Partial.pdf",
        "test_case": "Case B - Medium Match",
        "title": "Linux System Admin / DevOps Associate",
        "summary": "Kỹ trị viên hệ thống Linux với 2 năm kinh nghiệm quản trị server, ảo hóa và container hóa ứng dụng với Docker. Đang tự học Kubernetes và AWS nhưng chưa từng trực tiếp quản trị cụm Production K8s trên đám mây.",
        "education": [
            {
                "institution": "Đại học Bách Khoa Hà Nội",
                "degree": "Kỹ sư",
                "field_of_study": "Mạng máy tính & Truyền thông",
                "start_date": "2017",
                "end_date": "2022",
                "gpa": "3.0/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "NetNam Telecom",
                "job_title": "System Administrator",
                "start_date": "03/2022",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Quản trị máy chủ Ubuntu/CentOS, cài đặt Nginx, viết shell script sao lưu dữ liệu tự động. Đóng gói ứng dụng web vào Docker container."
            }
        ],
        "hard_skills": ["Linux", "Docker", "Bash Scripting", "Networking", "Git"],
        "soft_skills": ["Kiên nhẫn", "Cẩn thận", "Trực ca sự cố"],
        "certifications": ["Linux Professional Institute LPIC-1"],
        "expected_match_range": [50, 68],
        "expected_evaluation": "Phù hợp một phần (Medium Match): Thành thạo Linux, Docker nhưng thiếu Kubernetes, CI/CD pipeline hoàn chỉnh và AWS."
    },
    {
        "id": "cand-seed-09",
        "email": "candidate09@example.test",
        "full_name": "Hoàng Yến Nhi",
        "phone": "0901001009",
        "target_job_id": "job-seed-28",  # Recruitment Specialist
        "file_type": "docx",
        "file_name": "CV09_Hoang_Yen_Nhi_HR_Intern.docx",
        "test_case": "Case B - Medium Match",
        "title": "Chuyên viên Tuyển dụng tập sự",
        "summary": "Nhân viên nhân sự trẻ với 1 năm kinh nghiệm đăng tin tuyển dụng và tìm kiếm hồ sơ ứng viên khối ngành dịch vụ bán lẻ. Mong muốn chuyển hướng chuyên sâu sang mảng tuyển dụng nhân sự công nghệ.",
        "education": [
            {
                "institution": "Đại học Thương Mại",
                "degree": "Cử nhân",
                "field_of_study": "Quản trị Nhân lực",
                "start_date": "2019",
                "end_date": "2023",
                "gpa": "3.3/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty Dịch vụ Tiêu dùng Hà Nội",
                "job_title": "Nhân viên Tuyển dụng",
                "start_date": "08/2023",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Tiếp nhận nhu cầu tuyển dụng vị trí bán hàng, đăng tin trên các kênh tuyển dụng, liên hệ hẹn lịch phỏng vấn với ứng viên."
            }
        ],
        "hard_skills": ["Tuyển dụng", "Đăng tin", "Lọc hồ sơ", "Phỏng vấn sơ bộ", "Tin học văn phòng"],
        "soft_skills": ["Giao tiếp", "Lắng nghe", "Nhiệt tình"],
        "certifications": [],
        "expected_match_range": [50, 70],
        "expected_evaluation": "Phù hợp một phần (Medium Match): Có kỹ năng tuyển dụng cơ bản nhưng thiếu kinh nghiệm Headhunting chuyên sâu và kỹ năng sourcing qua LinkedIn."
    },
    {
        "id": "cand-seed-10",
        "email": "candidate10@example.test",
        "full_name": "Bùi Quốc Cường",
        "phone": "09010010010",
        "target_job_id": "job-seed-43",  # Kỹ sư xây dựng kết cấu
        "file_type": "pdf",
        "file_name": "CV10_Bui_Quoc_Cuong_Ky_Su_Giam_Sat.pdf",
        "test_case": "Case B - Medium Match",
        "title": "Kỹ sư Giám sát hiện trường",
        "summary": "Kỹ sư xây dựng có 3 năm kinh nghiệm giám sát thi công tại hiện trường công trình dân dụng. Đọc hiểu bản vẽ kết cấu và sử dụng AutoCAD thành thạo, nhưng chưa có nhiều kinh nghiệm lập mô hình tính toán tải trọng trên Etabs/SAP2000.",
        "education": [
            {
                "institution": "Đại học Xây dựng Hà Nội",
                "degree": "Kỹ sư",
                "field_of_study": "Xây dựng Dân dụng & Công nghiệp",
                "start_date": "2016",
                "end_date": "2021",
                "gpa": "3.1/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty Cổ phần Xây dựng Hải Phòng",
                "job_title": "Kỹ sư Giám sát công trường",
                "start_date": "06/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Giám sát công tác cốt thép, đổ bê tông sàn dầm, nghiệm thu khối lượng thi công thực tế theo bản vẽ thiết kế bằng AutoCAD."
            }
        ],
        "hard_skills": ["Kỹ sư xây dựng", "AutoCAD", "Bóc tách khối lượng", "Giám sát thi công", "TCVN"],
        "soft_skills": ["Chịu được áp lực hiện trường", "Quản lý tổ đội", "Quyết đoán"],
        "certifications": ["Chứng chỉ Hành nghề Giám sát Xây dựng hạng III"],
        "expected_match_range": [52, 70],
        "expected_evaluation": "Phù hợp một phần (Medium Match): Có bằng Kỹ sư xây dựng và AutoCAD, nhưng thiếu phần mềm tính toán kết cấu Etabs, SAFE, Revit Structure."
    },

    # --- Case C: Low Match / Cross-Industry (4 CVs) ---
    {
        "id": "cand-seed-11",
        "email": "candidate11@example.test",
        "full_name": "Mai Thanh Tùng",
        "phone": "09010010011",
        "target_job_id": "job-seed-03",  # Applying to Python Backend Developer with Graphic Designer profile!
        "file_type": "pdf",
        "file_name": "CV11_Mai_Thanh_Tung_Graphic_to_Python.pdf",
        "test_case": "Case C - Low Match / Cross-Industry",
        "title": "Chuyên viên Thiết kế đồ họa & Mỹ thuật số",
        "summary": "Thiết kế đồ họa 4 năm kinh nghiệm chuyên về tạo mẫu nhận diện thương hiệu, vẽ minh họa vector và xử lý hình ảnh sản phẩm. Đam mê nghệ thuật thị giác và sáng tạo không giới hạn.",
        "education": [
            {
                "institution": "Đại học Mỹ thuật TP.HCM",
                "degree": "Cử nhân",
                "field_of_study": "Thiết kế Đồ họa",
                "start_date": "2016",
                "end_date": "2020",
                "gpa": "3.6/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Leo Burnett Vietnam",
                "job_title": "Senior Graphic Designer",
                "start_date": "09/2020",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Thiết kế poster quảng cáo, bao bì nhãn mác sản phẩm và ấn phẩm truyền thông bằng Photoshop, Illustrator, InDesign."
            }
        ],
        "hard_skills": ["Photoshop", "Illustrator", "Thiết kế đồ họa", "Branding", "InDesign", "Typography"],
        "soft_skills": ["Thẩm mỹ thị giác", "Sáng tạo nghệ thuật", "Tỉ mỉ"],
        "certifications": ["Adobe Certified Professional in Visual Design"],
        "expected_match_range": [0, 25],
        "expected_evaluation": "Không phù hợp (Low Match): Ứng viên ngành Thiết kế đồ họa nộp cho vị trí Lập trình viên Backend Python; thiếu toàn bộ kỹ năng lập trình (Python, FastAPI, Database)."
    },
    {
        "id": "cand-seed-12",
        "email": "candidate12@example.test",
        "full_name": "Phan Thảo Vy",
        "phone": "09010010012",
        "target_job_id": "job-seed-43",  # Applying to Civil Engineer with Accountant profile!
        "file_type": "docx",
        "file_name": "CV12_Phan_Thao_Vy_Accountant_to_Civil.docx",
        "test_case": "Case C - Low Match / Cross-Industry",
        "title": "Kế toán viên Thuế & Doanh nghiệp",
        "summary": "Kế toán viên 3 năm kinh nghiệm phụ trách kê khai hóa đơn, hạch toán sổ sách chứng từ và làm việc với cơ quan thuế. Nắm vững phần mềm kế toán MISA và bảng tính Excel.",
        "education": [
            {
                "institution": "Đại học Tài chính - Marketing",
                "degree": "Cử nhân",
                "field_of_study": "Kế toán - Tài chính",
                "start_date": "2017",
                "end_date": "2021",
                "gpa": "3.3/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty TNHH Dịch vụ Kế toán Nam Việt",
                "job_title": "Nhân viên Kế toán thuế",
                "start_date": "08/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Nhập liệu hóa đơn đầu vào đầu ra trên MISA, làm tờ khai thuế GTGT, đối chiếu công nợ nhà cung cấp."
            }
        ],
        "hard_skills": ["Kế toán tổng hợp", "Kế toán thuế", "MISA", "Excel", "Báo cáo tài chính"],
        "soft_skills": ["Cẩn trọng", "Ngăn nắp", "Trung thực"],
        "certifications": [],
        "expected_match_range": [0, 20],
        "expected_evaluation": "Không phù hợp (Low Match): Ứng viên ngành Kế toán ứng tuyển kỹ sư kết cấu xây dựng; hoàn toàn không có kiến thức kỹ thuật công trình."
    },
    {
        "id": "cand-seed-13",
        "email": "candidate13@example.test",
        "full_name": "Đinh Trọng Nhân",
        "phone": "09010010013",
        "target_job_id": "job-seed-07",  # Applying to AI Engineer with Hotel Receptionist profile!
        "file_type": "pdf",
        "file_name": "CV13_Dinh_Trong_Nhan_Hotel_to_AI.pdf",
        "test_case": "Case C - Low Match / Cross-Industry",
        "title": "Nhân viên Lễ tân Khách sạn cao cấp",
        "summary": "Chuyên viên dịch vụ tiền sảnh khách sạn 5 sao với khả năng giao tiếp tiếng Anh trôi chảy và kỹ năng chăm sóc khách hàng lưu trú xuất sắc.",
        "education": [
            {
                "institution": "Đại học Ngoại ngữ Huế",
                "degree": "Cử nhân",
                "field_of_study": "Ngôn ngữ Anh & Du lịch",
                "start_date": "2018",
                "end_date": "2022",
                "gpa": "3.4/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Imperial Hotel Hue",
                "job_title": "Receptionist",
                "start_date": "05/2022",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Chào đón khách VIP, hỗ trợ check-in trên hệ thống Opera PMS, giới thiệu tour khám phá cố đô."
            }
        ],
        "hard_skills": ["Lễ tân", "Hospitality Management", "Tiếng Anh giao tiếp", "Customer Service", "Opera PMS"],
        "soft_skills": ["Thân thiện", "Khéo léo", "Ngoại giao"],
        "certifications": ["TOEIC 850"],
        "expected_match_range": [0, 20],
        "expected_evaluation": "Không phù hợp (Low Match): Ứng viên ngành Khách sạn nộp vào Kỹ sư Trí tuệ nhân tạo (AI Engineer)."
    },
    {
        "id": "cand-seed-14",
        "email": "candidate14@example.test",
        "full_name": "Cao Mỹ Duyên",
        "phone": "09010010014",
        "target_job_id": "job-seed-44",  # Applying to Mechanical Engineer with English Teacher profile!
        "file_type": "docx",
        "file_name": "CV14_Cao_My_Duyen_Teacher_to_Mechanical.docx",
        "test_case": "Case C - Low Match / Cross-Industry",
        "title": "Giáo viên tiếng Anh IELTS",
        "summary": "Giảng viên tiếng Anh với 3 năm kinh nghiệm giảng dạy ngữ pháp, từ vựng và luyện kỹ năng Speaking cho học viên chuẩn bị du học.",
        "education": [
            {
                "institution": "Đại học Sư phạm Hà Nội",
                "degree": "Cử nhân",
                "field_of_study": "Sư phạm Tiếng Anh",
                "start_date": "2017",
                "end_date": "2021",
                "gpa": "3.7/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Trung tâm Anh ngữ Quốc tế Ocean Edu",
                "job_title": "Giáo viên tiếng Anh",
                "start_date": "09/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Soạn giáo án điện tử, giảng dạy các lớp IELTS từ 5.0 - 6.5, chấm bài và hỗ trợ phát âm chuẩn IPA."
            }
        ],
        "hard_skills": ["English Teaching", "IELTS", "Soạn giáo án", "Quản lý lớp học", "TESOL"],
        "soft_skills": ["Truyền cảm hứng", "Sư phạm", "Kiên nhẫn"],
        "certifications": ["IELTS 8.0", "TESOL Certificate 120 hours"],
        "expected_match_range": [0, 20],
        "expected_evaluation": "Không phù hợp (Low Match): Giáo viên Tiếng Anh ứng tuyển Kỹ sư Cơ khí chế tạo; hoàn toàn khác biệt về lĩnh vực chuyên môn."
    },

    # --- Case D: Missing Critical Skills (3 CVs) ---
    {
        "id": "cand-seed-15",
        "email": "candidate15@example.test",
        "full_name": "Hồ Nhật Tân",
        "phone": "09010010015",
        "target_job_id": "job-seed-02",  # Senior React & TS (Missing React & TypeScript!)
        "file_type": "pdf",
        "file_name": "CV15_Ho_Nhat_Tan_Missing_React.pdf",
        "test_case": "Case D - Missing Critical Skills",
        "title": "Web Developer (HTML/CSS & PHP/WordPress)",
        "summary": "Lập trình viên Web với 4 năm kinh nghiệm xây dựng các website bán hàng và landing page bằng HTML5, CSS3, jQuery và PHP/WordPress. Chưa từng làm việc với ReactJS, TypeScript hay Next.js.",
        "education": [
            {
                "institution": "Cao đẳng Thực hành FPT Polytechnic",
                "degree": "Cử nhân Thực hành",
                "field_of_study": "Thiết kế Website",
                "start_date": "2016",
                "end_date": "2019",
                "gpa": "3.2/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Web Media Đà Nẵng",
                "job_title": "Web Designer & PHP Coder",
                "start_date": "10/2019",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Cắt HTML/CSS từ bản vẽ Photoshop, tích hợp theme WordPress bằng ngôn ngữ PHP và quản lý mã nguồn bằng Git."
            }
        ],
        "hard_skills": ["HTML", "CSS", "JavaScript", "PHP", "WordPress", "Git"],
        "soft_skills": ["Làm việc chăm chỉ", "Trách nhiệm"],
        "certifications": [],
        "expected_match_range": [30, 48],
        "expected_evaluation": "Thiếu kỹ năng cốt lõi (Missing Skills): Mặc dù có kinh nghiệm Web và HTML/CSS/Git, nhưng thiếu hoàn toàn kỹ năng bắt buộc số 1: React và TypeScript."
    },
    {
        "id": "cand-seed-16",
        "email": "candidate16@example.test",
        "full_name": "Trịnh Khánh Linh",
        "phone": "09010010016",
        "target_job_id": "job-seed-16",  # Kế toán tổng hợp (Missing MISA & Báo cáo tài chính!)
        "file_type": "docx",
        "file_name": "CV16_Trinh_Khanh_Linh_Admin_to_KeToan.docx",
        "test_case": "Case D - Missing Critical Skills",
        "title": "Nhân viên Hành chính - Văn thư",
        "summary": "Nhân viên văn phòng có kinh nghiệm quản lý văn phòng phẩm, hỗ trợ lưu trữ chứng từ chi phí và phụ trách các công việc hành chính tổng hợp. Chưa có chuyên môn về lập báo cáo tài chính hay phần mềm MISA.",
        "education": [
            {
                "institution": "Đại học Văn Hiến",
                "degree": "Cử nhân",
                "field_of_study": "Quản trị Văn phòng",
                "start_date": "2018",
                "end_date": "2022",
                "gpa": "3.0/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty TNHH Thương mại Phú Đạt",
                "job_title": "Nhân viên Hành chính",
                "start_date": "06/2022",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Quản lý hợp đồng hành chính, theo dõi thanh toán các hóa đơn điện nước văn phòng bằng Excel cơ bản."
            }
        ],
        "hard_skills": ["Excel", "Soạn thảo văn bản", "Lưu trữ hồ sơ", "Hành chính văn phòng"],
        "soft_skills": ["Cẩn thận", "Nhiệt tình", "Giao tiếp nội bộ"],
        "certifications": [],
        "expected_match_range": [25, 42],
        "expected_evaluation": "Thiếu kỹ năng cốt lõi: Chỉ có kỹ năng hành chính và Excel cơ bản, thiếu hoàn toàn MISA, Báo cáo tài chính và nghiệp vụ kế toán chuyên sâu."
    },
    {
        "id": "cand-seed-17",
        "email": "candidate17@example.test",
        "full_name": "Võ Thành Đạt",
        "phone": "09010010017",
        "target_job_id": "job-seed-21",  # SEO Specialist (Missing SEO & GA!)
        "file_type": "pdf",
        "file_name": "CV17_Vo_Thanh_Dat_Missing_SEO.pdf",
        "test_case": "Case D - Missing Critical Skills",
        "title": "Content Writer & Cộng tác viên viết bài",
        "summary": "Người viết lách tự do với 2 năm kinh nghiệm sáng tạo nội dung truyện ngắn và bài PR báo chí. Chưa từng thực hiện tối ưu hóa công cụ tìm kiếm (Technical SEO) hay sử dụng Google Analytics.",
        "education": [
            {
                "institution": "Đại học Khoa học Xã hội & Nhân văn TP.HCM",
                "degree": "Cử nhân",
                "field_of_study": "Văn học",
                "start_date": "2018",
                "end_date": "2022",
                "gpa": "3.5/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Tạp chí Văn hóa Trẻ",
                "job_title": "Cộng tác viên nội dung",
                "start_date": "09/2022",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Viết bài xã luận và tản văn theo chủ đề hàng tuần. Biên tập câu từ và kiểm tra lỗi chính tả."
            }
        ],
        "hard_skills": ["Sáng tạo nội dung", "Viết lách", "Biên tập văn bản"],
        "soft_skills": ["Cảm xúc ngôn từ", "Đúng hạn"],
        "certifications": [],
        "expected_match_range": [25, 45],
        "expected_evaluation": "Thiếu kỹ năng cốt lõi: Có khả năng viết nhưng thiếu hoàn toàn SEO On-page/Off-page, Google Analytics, Technical SEO."
    },

    # --- Case E: Junior vs Senior (3 CVs) ---
    {
        "id": "cand-seed-18",
        "email": "candidate18@example.test",
        "full_name": "Lâm Gia Huy",
        "phone": "09010010018",
        "target_job_id": "job-seed-04",  # Senior Java (Requires 5 yrs vs 6 months intern!)
        "file_type": "docx",
        "file_name": "CV18_Lam_Gia_Huy_Java_Intern_to_Senior.docx",
        "test_case": "Case E - Junior vs Senior",
        "title": "Sinh viên mới tốt nghiệp - Lập trình Java",
        "summary": "Sinh viên mới tốt nghiệp ngành CNTT loại Khá, nắm vững kiến thức lập trình hướng đối tượng với Java Core và đã làm đồ án tốt nghiệp với Spring Boot. Mong muốn tìm kiếm cơ hội học việc.",
        "education": [
            {
                "institution": "Học viện Công nghệ Bưu chính Viễn thông Hà Nội",
                "degree": "Kỹ sư",
                "field_of_study": "Công nghệ Phần mềm",
                "start_date": "2020",
                "end_date": "2024",
                "gpa": "3.1/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty Phần mềm Thiên Hà",
                "job_title": "Java Intern",
                "start_date": "02/2024",
                "end_date": "08/2024",
                "is_current": False,
                "description": "Thực tập 6 tháng hỗ trợ viết các câu lệnh truy vấn MySQL đơn giản và sửa lỗi nhỏ trong ứng dụng web Spring Boot."
            }
        ],
        "hard_skills": ["Java", "Spring Boot", "MySQL", "Git"],
        "soft_skills": ["Nhiệt huyết", "Cầu tiến", "Ham học"],
        "certifications": [],
        "expected_match_range": [42, 60],
        "expected_evaluation": "Lệch cấp bậc (Junior vs Senior): Có đúng công nghệ Java và Spring Boot nhưng chỉ có 6 tháng thực tập, hoàn toàn không đáp ứng yêu cầu 5 năm kinh nghiệm và kiến trúc phân tán Kafka."
    },
    {
        "id": "cand-seed-19",
        "email": "candidate19@example.test",
        "full_name": "Huỳnh Trúc Mai",
        "phone": "09010010019",
        "target_job_id": "job-seed-29",  # HRBP (Requires 5 yrs & leadership vs 1 yr junior!)
        "file_type": "pdf",
        "file_name": "CV19_Huynh_Truc_Mai_HR_Junior_to_HRBP.pdf",
        "test_case": "Case E - Junior vs Senior",
        "title": "Trợ lý Nhân sự (HR Assistant)",
        "summary": "Trợ lý nhân sự có 1 năm kinh nghiệm làm việc hỗ trợ lưu trữ hồ sơ nhân viên, tổ chức sự kiện sinh nhật nội bộ và đăng tin tuyển dụng. Chưa có kinh nghiệm xây dựng chiến lược nhân sự hay tư vấn C-level.",
        "education": [
            {
                "institution": "Đại học Lao động - Xã hội",
                "degree": "Cử nhân",
                "field_of_study": "Quản trị Nhân lực",
                "start_date": "2019",
                "end_date": "2023",
                "gpa": "3.2/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty TNHH Truyền thông Ánh Dương",
                "job_title": "HR Assistant",
                "start_date": "07/2023",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Hỗ trợ chấm công bằng phần mềm vân tay, chuẩn bị quà sinh nhật và soạn thảo thông báo nội bộ."
            }
        ],
        "hard_skills": ["Quản trị nhân lực", "Tuyển dụng", "Tin học văn phòng", "Soạn thảo văn bản"],
        "soft_skills": ["Giao tiếp", "Hòa đồng", "Chu đáo"],
        "certifications": [],
        "expected_match_range": [40, 58],
        "expected_evaluation": "Lệch cấp bậc (Junior vs Senior): Đúng chuyên ngành Nhân sự nhưng chỉ có 1 năm kinh nghiệm trợ lý, không đáp ứng vai trò chiến lược HRBP 5 năm kinh nghiệm."
    },
    {
        "id": "cand-seed-20",
        "email": "candidate20@example.test",
        "full_name": "Nguyễn Hữu Trí",
        "phone": "09010010020",
        "target_job_id": "job-seed-46",  # Production Supervisor (Requires 4 yrs & lead vs 8 mos tech!)
        "file_type": "docx",
        "file_name": "CV20_Nguyen_Huu_Tri_Tech_to_Supervisor.docx",
        "test_case": "Case E - Junior vs Senior",
        "title": "Kỹ thuật viên Vận hành máy",
        "summary": "Kỹ thuật viên có 8 tháng kinh nghiệm đứng máy gia công tại xưởng sản xuất, hiểu quy tắc 5S nhưng chưa từng quản lý con người hay điều hành ca sản xuất.",
        "education": [
            {
                "institution": "Cao đẳng Kỹ thuật Công nghiệp Hải Phòng",
                "degree": "Cao đẳng",
                "field_of_study": "Cơ khí",
                "start_date": "2020",
                "end_date": "2023",
                "gpa": "3.0/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Xưởng Gia công Cơ khí Đình Vũ",
                "job_title": "Công nhân kỹ thuật",
                "start_date": "10/2023",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Trực tiếp vận hành máy dập khuôn, vệ sinh khu vực làm việc theo tiêu chuẩn 5S."
            }
        ],
        "hard_skills": ["5S", "Vận hành máy", "Cơ khí cơ bản"],
        "soft_skills": ["Chăm chỉ", "Tuân thủ kỷ luật"],
        "certifications": [],
        "expected_match_range": [38, 55],
        "expected_evaluation": "Lệch cấp bậc (Junior vs Senior): Có hiểu biết 5S nhưng thiếu kỹ năng quản lý sản xuất, Lean Manufacturing và năng lực lãnh đạo ca sản xuất quy mô 100 người."
    },

    # --- Case F: Semantic Matching (4 CVs) ---
    {
        "id": "cand-seed-21",
        "email": "candidate21@example.test",
        "full_name": "Đoàn Minh Trí",
        "phone": "09010010021",
        "target_job_id": "job-seed-07",  # AI Engineer (Uses Vietnamese Synonyms!)
        "file_type": "pdf",
        "file_name": "CV21_Doan_Minh_Tri_Semantic_AI.pdf",
        "test_case": "Case F - Semantic Matching",
        "title": "Kỹ sư Trí tuệ Nhân tạo & Xử lý Ngôn ngữ",
        "summary": "Chuyên gia Trí tuệ nhân tạo có 4 năm kinh nghiệm nghiên cứu mô hình Học máy và Xử lý ngôn ngữ tự nhiên. Đã xây dựng các hệ thống khuyến nghị thông minh và truy xuất tăng cường cho bài toán phân tích tài liệu tự động.",
        "education": [
            {
                "institution": "Đại học Bách Khoa Hà Nội",
                "degree": "Kỹ sư Tài năng",
                "field_of_study": "Công nghệ Thông tin",
                "start_date": "2015",
                "end_date": "2020",
                "gpa": "3.7/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Viện Nghiên cứu Trí tuệ Nhân tạo VAST",
                "job_title": "Nghiên cứu viên Trí tuệ Nhân tạo",
                "start_date": "08/2020",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Huấn luyện các mạng nơ-ron sâu với PyTorch, phát triển giải pháp truy xuất tăng cường (RAG) và tối ưu hóa mô hình ngôn ngữ lớn (LLMs) cho ngữ cảnh tiếng Việt."
            }
        ],
        "hard_skills": ["Trí tuệ nhân tạo", "Học máy", "NLP", "PyTorch", "Python", "RAG", "LLMs"],
        "soft_skills": ["Nghiên cứu khoa học", "Tư duy phản biện", "Thuyết trình học thuật"],
        "certifications": ["DeepLearning.AI TensorFlow Developer Professional Certificate"],
        "expected_match_range": [82, 95],
        "expected_evaluation": "Tương đồng ngữ nghĩa (Semantic Matching): Sử dụng cách diễn đạt 'Trí tuệ nhân tạo', 'Học máy' đồng nghĩa với AI, Machine Learning, hệ thống nhận diện chính xác và cho điểm cao."
    },
    {
        "id": "cand-seed-22",
        "email": "candidate22@example.test",
        "full_name": "Tống Mỹ Linh",
        "phone": "09010010022",
        "target_job_id": "job-seed-17",  # Chuyên viên phân tích tài chính (Uses English Financial Synonyms!)
        "file_type": "docx",
        "file_name": "CV22_Tong_My_Linh_Semantic_Finance.docx",
        "test_case": "Case F - Semantic Matching",
        "title": "Senior Financial Planning & Analysis (FP&A)",
        "summary": "Chuyên gia hoạch định và phân tích tài chính doanh nghiệp với 4 năm kinh nghiệm xây dựng Financial Modeling, dự báo dòng tiền (Cash Flow Forecasting) và đánh giá danh mục vốn đầu tư.",
        "education": [
            {
                "institution": "RMIT University Vietnam",
                "degree": "Bachelor of Business",
                "field_of_study": "Economics and Finance",
                "start_date": "2016",
                "end_date": "2020",
                "gpa": "3.5/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "PwC Vietnam",
                "job_title": "Financial Advisory Senior Associate",
                "start_date": "10/2020",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Xây dựng mô hình định giá DCF, phân tích độ nhạy tài chính dự án, lập báo cáo thẩm định ngân sách và đánh giá dòng tiền cho các thương vụ M&A."
            }
        ],
        "hard_skills": ["Financial Analysis", "Financial Modeling", "Cash Flow Management", "Excel", "Báo cáo tài chính"],
        "soft_skills": ["Giao tiếp tiếng Anh chuẩn", "Tư duy chiến lược", "Đàm phán"],
        "certifications": ["CFA Charterholder Candidate (Passed Level II)"],
        "expected_match_range": [85, 96],
        "expected_evaluation": "Tương đồng ngữ nghĩa (Semantic Matching): Sử dụng thuật ngữ tiếng Anh chuẩn FP&A, Cash Flow Management, Financial Modeling tương đương với Phân tích tài chính và Quản trị dòng tiền."
    },
    {
        "id": "cand-seed-23",
        "email": "candidate23@example.test",
        "full_name": "Lưu Vĩnh Phú",
        "phone": "09010010023",
        "target_job_id": "job-seed-35",  # Supply Chain Analyst (Uses Vietnamese Supply Chain Synonyms!)
        "file_type": "pdf",
        "file_name": "CV23_Luu_Vinh_Phu_Semantic_SupplyChain.pdf",
        "test_case": "Case F - Semantic Matching",
        "title": "Chuyên viên Hoạch định Chuỗi cung ứng",
        "summary": "3 năm kinh nghiệm trong quản trị chuỗi cung ứng, chuyên trách phân tích luân chuyển hàng hóa, điều phối kho lạnh và cân bằng tồn kho an toàn cho ngành hàng thực phẩm xuất khẩu.",
        "education": [
            {
                "institution": "Đại học Giao thông Vận tải TP.HCM",
                "degree": "Kỹ sư",
                "field_of_study": "Quản trị Chuỗi cung ứng & Logistics",
                "start_date": "2017",
                "end_date": "2021",
                "gpa": "3.4/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "CP Vietnam Corporation",
                "job_title": "Supply Chain Planner",
                "start_date": "08/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Phân tích số liệu xuất nhập tồn bằng Excel và hệ thống ERP. Lập kế hoạch cung ứng nguyên liệu sản xuất, giảm 15% chi phí lưu kho."
            }
        ],
        "hard_skills": ["Chuỗi cung ứng", "Quản lý tồn kho", "Phân tích dữ liệu", "Excel", "ERP"],
        "soft_skills": ["Lập kế hoạch", "Tư duy logic", "Giải quyết vấn đề"],
        "certifications": ["APICS Certified Supply Chain Professional (CSCP)"],
        "expected_match_range": [82, 95],
        "expected_evaluation": "Tương đồng ngữ nghĩa (Semantic Matching): Thuật ngữ 'Chuỗi cung ứng' khớp nối với 'Supply Chain', ERP và Quản trị tồn kho đáp ứng xuất sắc."
    },
    {
        "id": "cand-seed-24",
        "email": "candidate24@example.test",
        "full_name": "Phùng Hải Yến",
        "phone": "09010010024",
        "target_job_id": "job-seed-22",  # Content Marketing (Uses Synonyms: Copywriting, Sáng tạo nội dung)
        "file_type": "docx",
        "file_name": "CV24_Phung_Hai_Yen_Semantic_Content.docx",
        "test_case": "Case F - Semantic Matching",
        "title": "Senior Copywriter & Creative Content Producer",
        "summary": "Cây bút sáng tạo nội dung với 3 năm kinh nghiệm viết lời quảng cáo (Copywriting), xây dựng kịch bản video viral và dẫn dắt chiến dịch truyền thông đa kênh cho thương hiệu mỹ phẩm và F&B.",
        "education": [
            {
                "institution": "Đại học Khoa học Xã hội & Nhân văn Hà Nội",
                "degree": "Cử nhân",
                "field_of_study": "Báo chí & Truyền thông",
                "start_date": "2017",
                "end_date": "2021",
                "gpa": "3.6/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Dentsu Redder Vietnam",
                "job_title": "Copywriter",
                "start_date": "09/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Sáng tạo thông điệp chiến dịch (Key Message), viết bài PR báo chí, biên kịch nội dung video ngắn cho TikTok và quản trị nội dung mạng xã hội."
            }
        ],
        "hard_skills": ["Copywriting", "Sáng tạo nội dung", "Storytelling", "Social Media", "Kịch bản Video"],
        "soft_skills": ["Tư duy thẩm mỹ từ ngữ", "Nắm bắt tâm lý", "Làm việc độc lập"],
        "certifications": [],
        "expected_match_range": [82, 94],
        "expected_evaluation": "Tương đồng ngữ nghĩa (Semantic Matching): Các từ khóa 'Copywriting', 'Sáng tạo nội dung', 'Storytelling' tương đồng với Content Marketing."
    },

    # --- Case G: Negative Skills (3 CVs) ---
    {
        "id": "cand-seed-25",
        "email": "candidate25@example.test",
        "full_name": "Kiều Quốc Anh",
        "phone": "09010010025",
        "target_job_id": "job-seed-12",  # DevOps (Mentions: Chưa có kinh nghiệm Docker, chưa biết Kubernetes!)
        "file_type": "pdf",
        "file_name": "CV25_Kieu_Quoc_Anh_Negative_Docker.pdf",
        "test_case": "Case G - Negative Skills",
        "title": "Quản trị mạng văn phòng",
        "summary": "Quản trị viên mạng nội bộ có 2 năm kinh nghiệm bảo trì hệ thống máy tính, cấu hình mạng LAN và máy chủ Linux. Lưu ý: Chưa có kinh nghiệm sử dụng Docker. Chưa từng làm việc với Kubernetes hay triển khai ứng dụng đám mây.",
        "education": [
            {
                "institution": "Đại học Giao thông Vận tải Hà Nội",
                "degree": "Kỹ sư",
                "field_of_study": "Công nghệ Thông tin",
                "start_date": "2018",
                "end_date": "2022",
                "gpa": "3.1/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty Cổ phần Tin học Thủ Đô",
                "job_title": "IT Helpdesk & Network Admin",
                "start_date": "07/2022",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Bảo trì thiết bị mạng nội bộ Cisco. Cài đặt hệ điều hành Linux Ubuntu Server. Đang tìm hiểu công nghệ mới nhưng chưa từng triển khai Docker và Kubernetes trên thực tế."
            }
        ],
        "hard_skills": ["Linux", "Networking", "VPN", "Bash Scripting"],
        "soft_skills": ["Nhiệt tình", "Kỷ luật"],
        "negative_skills": ["Docker", "Kubernetes"],
        "certifications": ["CCNA"],
        "expected_match_range": [28, 48],
        "expected_evaluation": "Kiểm tra kỹ năng phủ định (Negative Skills): Ứng viên ghi rõ 'Chưa có kinh nghiệm sử dụng Docker. Chưa từng làm việc với Kubernetes', AI bắt buộc KHÔNG ĐƯỢC tính điểm cho Docker và Kubernetes."
    },
    {
        "id": "cand-seed-26",
        "email": "candidate26@example.test",
        "full_name": "Tạ Hồng Nhung",
        "phone": "09010010026",
        "target_job_id": "job-seed-16",  # Kế toán (Mentions: Không thành thạo MISA, chưa có kinh nghiệm lập Báo cáo tài chính!)
        "file_type": "docx",
        "file_name": "CV26_Ta_Hong_Nhung_Negative_MISA.docx",
        "test_case": "Case G - Negative Skills",
        "title": "Thực tập sinh Kế toán",
        "summary": "Sinh viên mới tốt nghiệp có kiến thức kế toán căn bản. Cần lưu ý: Chưa có kinh nghiệm lập Báo cáo tài chính thực tế và không thành thạo MISA do trước đây chỉ học lý thuyết tại trường.",
        "education": [
            {
                "institution": "Đại học Sài Gòn",
                "degree": "Cử nhân",
                "field_of_study": "Kế toán",
                "start_date": "2020",
                "end_date": "2024",
                "gpa": "3.0/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Cửa hàng Tiện lợi An Khang (Bán thời gian)",
                "job_title": "Thu ngân & Thu chi nội bộ",
                "start_date": "01/2024",
                "end_date": "06/2024",
                "is_current": False,
                "description": "Kiểm đếm tiền mặt, nhập số liệu bán hàng vào Excel. Chưa từng làm việc với phần mềm kế toán chuyên dụng MISA hay lập Báo cáo tài chính năm."
            }
        ],
        "hard_skills": ["Excel", "Kế toán cơ bản"],
        "soft_skills": ["Cẩn thận", "Trung thực"],
        "negative_skills": ["MISA", "Báo cáo tài chính"],
        "certifications": [],
        "expected_match_range": [25, 45],
        "expected_evaluation": "Kiểm tra kỹ năng phủ định (Negative Skills): Câu 'Không thành thạo MISA, chưa có kinh nghiệm lập Báo cáo tài chính' phải bị loại trừ, không cộng điểm kỹ năng."
    },
    {
        "id": "cand-seed-27",
        "email": "candidate27@example.test",
        "full_name": "Văn Đức Thành",
        "phone": "09010010027",
        "target_job_id": "job-seed-20",  # Digital Marketing (Mentions: Chưa từng chạy Facebook Ads, chưa biết Google Analytics!)
        "file_type": "pdf",
        "file_name": "CV27_Van_Duc_Thanh_Negative_Ads.pdf",
        "test_case": "Case G - Negative Skills",
        "title": "Nhân viên Telesales & Chăm sóc khách hàng",
        "summary": "Chuyên viên tư vấn bán hàng có 2 năm kinh nghiệm gọi điện thoại thuyết phục khách hàng. Cần ghi chú rõ: Chưa từng chạy Facebook Ads và chưa biết sử dụng Google Analytics; mong muốn được đào tạo thêm về mảng Marketing số.",
        "education": [
            {
                "institution": "Đại học Mở TP.HCM",
                "degree": "Cử nhân",
                "field_of_study": "Quản trị Kinh doanh",
                "start_date": "2018",
                "end_date": "2022",
                "gpa": "3.1/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Công ty Bảo hiểm Nhân thọ Prudential Agency",
                "job_title": "Telesales Executive",
                "start_date": "08/2022",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Tư vấn hợp đồng bảo hiểm qua điện thoại. Không phụ trách marketing trực tuyến và chưa từng chạy Facebook Ads."
            }
        ],
        "hard_skills": ["Telesales", "Customer Service", "Giao tiếp"],
        "soft_skills": ["Thuyết phục", "Kiên trì"],
        "negative_skills": ["Facebook Ads", "Google Analytics"],
        "certifications": [],
        "expected_match_range": [20, 38],
        "expected_evaluation": "Kiểm tra kỹ năng phủ định (Negative Skills): 'Chưa từng chạy Facebook Ads và chưa biết sử dụng Google Analytics' phải được nhận diện là kỹ năng thiếu."
    },

    # --- Additional Diverse Sector CVs (3 CVs) ---
    {
        "id": "cand-seed-28",
        "email": "candidate28@example.test",
        "full_name": "Lương Bích Trâm",
        "phone": "09010010028",
        "target_job_id": "job-seed-47",  # Điều phối y tế
        "file_type": "docx",
        "file_name": "CV28_Luong_Bich_Tram_Y_Te.docx",
        "test_case": "Case A - High Match (Healthcare)",
        "title": "Cử nhân Y tế Công cộng - Điều phối y tế",
        "summary": "3 năm kinh nghiệm trong vai trò điều phối khám chữa bệnh và hướng dẫn bệnh nhân tại phòng khám đa khoa quốc tế. Nắm vững quy trình khám bệnh, thuật ngữ y khoa và phần mềm hồ sơ bệnh viện (HIS).",
        "education": [
            {
                "institution": "Đại học Y Dược TP.HCM",
                "degree": "Cử nhân",
                "field_of_study": "Y tế Công cộng",
                "start_date": "2017",
                "end_date": "2021",
                "gpa": "3.5/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Phòng khám Quốc tế Victoria Healthcare",
                "job_title": "Nhân viên Điều phối Y tế",
                "start_date": "09/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Sắp xếp lịch hẹn khám của bệnh nhân, hướng dẫn làm các xét nghiệm cận lâm sàng và bảo lãnh viện phí bảo hiểm sức khỏe trên hệ thống HIS."
            }
        ],
        "hard_skills": ["Clinical Coordination", "Điều phối y tế", "Chăm sóc bệnh nhân", "Thuật ngữ y khoa", "HIS", "Bảo hiểm y tế"],
        "soft_skills": ["Ân cần", "Giao tiếp y khoa", "Bình tĩnh trước áp lực"],
        "certifications": ["Chứng chỉ Sơ cấp cứu hồi sinh tim phổi (CPR/BLS)"],
        "expected_match_range": [85, 96],
        "expected_evaluation": "Rất phù hợp (High Match): Đầy đủ các tiêu chuẩn điều phối y tế, chăm sóc bệnh nhân và thuật ngữ chuyên môn."
    },
    {
        "id": "cand-seed-29",
        "email": "candidate29@example.test",
        "full_name": "Chu Văn An",
        "phone": "09010010029",
        "target_job_id": "job-seed-40",  # Giáo viên IELTS
        "file_type": "pdf",
        "file_name": "CV29_Chu_Van_An_Giao_Vien_IELTS.pdf",
        "test_case": "Case A - High Match (Education)",
        "title": "Giảng viên tiếng Anh IELTS 8.0",
        "summary": "Giảng viên tiếng Anh 4 năm kinh nghiệm luyện thi IELTS cho hơn 500 học viên đạt mục tiêu 6.5 - 7.5. Sở hữu chứng chỉ IELTS 8.0 và chứng chỉ giảng dạy quốc tế CELTA loại Xuất sắc.",
        "education": [
            {
                "institution": "Đại học Hà Nội (HANU)",
                "degree": "Cử nhân",
                "field_of_study": "Ngôn ngữ Anh",
                "start_date": "2016",
                "end_date": "2020",
                "gpa": "3.7/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Học viện Ngôn ngữ The IELTS Workshop",
                "job_title": "Giáo viên tiếng Anh IELTS",
                "start_date": "10/2020",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Giảng dạy các khóa học IELTS mục tiêu 6.5 - 7.5, biên soạn giáo trình bổ trợ Speaking & Writing, tổ chức thi thử hàng tháng."
            }
        ],
        "hard_skills": ["English Teaching", "IELTS", "CELTA", "TESOL", "Soạn giáo án", "Quản lý lớp học"],
        "soft_skills": ["Sư phạm truyền cảm", "Tận tâm", "Truyền động lực"],
        "certifications": ["IELTS Academic 8.0 (2023)", "Cambridge CELTA Pass A"],
        "expected_match_range": [88, 98],
        "expected_evaluation": "Rất phù hợp (High Match): Điểm IELTS 8.0, chứng chỉ CELTA chuẩn Cambridge và có 4 năm kinh nghiệm giảng dạy thực tế."
    },
    {
        "id": "cand-seed-30",
        "email": "candidate30@example.test",
        "full_name": "Nông Quốc Tuấn",
        "phone": "09010010030",
        "target_job_id": "job-seed-49",  # Nông nghiệp công nghệ cao
        "file_type": "docx",
        "file_name": "CV30_Nong_Quoc_Tuan_Nong_Nghiep.docx",
        "test_case": "Case A - High Match (Agriculture)",
        "title": "Kỹ sư Nông nghiệp Công nghệ cao",
        "summary": "Kỹ sư Nông nghiệp 3 năm kinh nghiệm vận hành hệ thống nhà màng thông minh, thiết lập chế độ tưới tự động qua cảm biến và quy trình canh tác rau quả chuẩn VietGAP tại ĐBSCL.",
        "education": [
            {
                "institution": "Đại học Cần Thơ",
                "degree": "Kỹ sư",
                "field_of_study": "Nông nghiệp Công nghệ cao",
                "start_date": "2017",
                "end_date": "2021",
                "gpa": "3.5/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Trang trại Sinh thái Nông nghiệp Cần Thơ",
                "job_title": "Kỹ sư Canh tác thông minh",
                "start_date": "08/2021",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Quản trị hệ thống tưới nhỏ giọt Israel tự động hóa, theo dõi dịch hại theo IPM và đảm bảo quy chuẩn an toàn thực phẩm VietGAP xuất khẩu."
            }
        ],
        "hard_skills": ["Smart Agriculture", "Nông nghiệp công nghệ cao", "VietGAP", "Irrigation Systems", "Pest Management", "IoT nông nghiệp"],
        "soft_skills": ["Chịu khó thực địa", "Nghiên cứu ứng dụng", "Trách nhiệm cao"],
        "certifications": ["Chứng chỉ Đánh giá viên VietGAP"],
        "expected_match_range": [85, 96],
        "expected_evaluation": "Rất phù hợp (High Match): Đầy đủ kiến thức Smart Agriculture, VietGAP, hệ thống tưới và kinh nghiệm thực tiễn phong phú."
    }
]

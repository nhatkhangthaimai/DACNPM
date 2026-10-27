import { Job, Company, CV, Application } from '../types';

export const INITIAL_COMPANIES: Company[] = [
  {
    id: 'comp-1',
    name: 'VNG Corporation',
    slug: 'vng-corp',
    logoUrl: 'https://images.unsplash.com/photo-1549923746-c502d488b3ea?w=128&auto=format&fit=crop&q=80',
    website: 'https://vng.com.vn',
    industry: 'Technology & Gaming',
    companySize: '1000+ nhân viên',
    address: 'Z06 Đường số 13, Tân Thuận Đông, Quận 7, TP.HCM',
    description: 'Kỳ lân công nghệ đầu tiên tại Việt Nam, tiên phong trong mảng game trực tuyến, thanh toán số ZaloPay và nền tảng AI.',
    status: 'approved',
  },
  {
    id: 'comp-2',
    name: 'FPT Software',
    slug: 'fpt-software',
    logoUrl: 'https://images.unsplash.com/photo-1572021335469-31706a17aaef?w=128&auto=format&fit=crop&q=80',
    website: 'https://fptsoftware.com',
    industry: 'IT Services & Consulting',
    companySize: '500+ nhân viên',
    address: 'Khu Công Nghệ Cao, TP. Thủ Đức, TP.HCM',
    description: 'Tập đoàn công nghệ hàng đầu khu vực, cung cấp giải pháp chuyển đổi số toàn cầu và AI Lab chuyên sâu.',
    status: 'approved',
  },
  {
    id: 'comp-3',
    name: 'MoMo (M-Service)',
    slug: 'momo',
    logoUrl: 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=128&auto=format&fit=crop&q=80',
    website: 'https://momo.vn',
    industry: 'Fintech',
    companySize: '500+ nhân viên',
    address: 'Tòa nhà Phú Mỹ Hưng, Quận 7, TP.HCM',
    description: 'Siêu ứng dụng thanh toán và tài chính số hàng đầu Việt Nam phục vụ hơn 30 triệu người dùng.',
    status: 'approved',
  }
];

export const INITIAL_JOBS: Job[] = [
  {
    id: 'job-1',
    companyId: 'comp-1',
    companyName: 'VNG Corporation',
    companyLogo: 'https://images.unsplash.com/photo-1549923746-c502d488b3ea?w=128&auto=format&fit=crop&q=80',
    title: 'Senior AI / Machine Learning Engineer (LLMs & RAG)',
    description: 'Phát triển hệ thống AI Agent thông minh ứng dụng LLMs, mô hình Embedding, và cơ chế RAG phục vụ hàng triệu người dùng. Tối ưu inference latency và xây dựng pipeline trích xuất dữ liệu đa phương thức.',
    requirements: 'Tối thiểu 3 năm kinh nghiệm với Python, PyTorch, Hugging Face, LangChain. Có kiến thức sâu về LLMs, Vector Databases (pgvector, Milvus), Prompt Engineering và API Optimization.',
    benefits: 'Lương thưởng cạnh tranh up to 60.000.000 VND. Bảo hiểm sức khỏe quốc tế cao cấp, thưởng KPI hàng quý, môi trường hybrid linh hoạt.',
    jobType: 'hybrid',
    location: 'Quận 7, TP.HCM',
    salaryMin: 45000000,
    salaryMax: 65000000,
    currency: 'VND',
    experienceLevel: 'senior',
    status: 'published',
    requiredSkills: ['Python', 'LLMs', 'PyTorch', 'Vector Databases', 'pgvector', 'FastAPI'],
    preferredSkills: ['Docker', 'LangChain', 'Kubernetes', 'CI/CD'],
    createdAt: '2026-10-20T08:00:00Z',
  },
  {
    id: 'job-2',
    companyId: 'comp-2',
    companyName: 'FPT Software',
    companyLogo: 'https://images.unsplash.com/photo-1572021335469-31706a17aaef?w=128&auto=format&fit=crop&q=80',
    title: 'Full-Stack Developer (ReactJS + Python/FastAPI)',
    description: 'Tham gia xây dựng sản phẩm SaaS tuyển dụng thế hệ mới. Trực tiếp phát triển giao diện responsive hiện đại, tối ưu trải nghiệm người dùng và kết nối hệ thống Microservices backend.',
    requirements: 'Thành thạo ReactJS, TypeScript, Tailwind CSS. Kinh nghiệm thực chiến với Python, FastAPI, PostgreSQL và RESTful API. Khả năng tư duy sản phẩm và clean code.',
    benefits: 'Thưởng gia nhập lên đến 20M, cơ hội on-site Nhật Bản / Singapore, gói chăm sóc sức khỏe FPT Care cho bản thân và gia đình.',
    jobType: 'full_time',
    location: 'Khu CNC, TP. Thủ Đức, TP.HCM',
    salaryMin: 25000000,
    salaryMax: 40000000,
    currency: 'VND',
    experienceLevel: 'mid',
    status: 'published',
    requiredSkills: ['ReactJS', 'TypeScript', 'Tailwind CSS', 'Python', 'FastAPI', 'PostgreSQL'],
    preferredSkills: ['Docker', 'Next.js', 'Redux', 'Git'],
    createdAt: '2026-10-22T09:30:00Z',
  },
  {
    id: 'job-3',
    companyId: 'comp-3',
    companyName: 'MoMo (M-Service)',
    companyLogo: 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=128&auto=format&fit=crop&q=80',
    title: 'Lead Frontend Architect (Design System & Micro-frontends)',
    description: 'Chủ trì thiết kế kiến trúc Frontend Core cho toàn bộ ứng dụng web đối tác. Xây dựng bộ Design System Signal đạt chuẩn quốc tế, đảm bảo hiệu năng 60fps và khả năng mở rộng.',
    requirements: 'Ít nhất 5 năm kinh nghiệm Frontend, thành thạo React, Webpack/Vite, Design System, CSS Architecture. Kỹ năng leadership và giao tiếp xuất sắc.',
    benefits: 'Thu nhập hấp dẫn + Cổ phiếu thưởng ESOP. Môi trường làm việc cởi mở, trang bị Macbook Pro M-series cao cấp.',
    jobType: 'full_time',
    location: 'Quận 7, TP.HCM',
    salaryMin: 50000000,
    salaryMax: 80000000,
    currency: 'VND',
    experienceLevel: 'lead',
    status: 'published',
    requiredSkills: ['React', 'TypeScript', 'Design Systems', 'Micro-frontends', 'Performance Optimization'],
    preferredSkills: ['Figma Tokens', 'Tailwind CSS', 'Jest', 'Storybook'],
    createdAt: '2026-10-24T14:15:00Z',
  },
  {
    id: 'job-4',
    companyId: 'comp-1',
    companyName: 'VNG Corporation',
    companyLogo: 'https://images.unsplash.com/photo-1549923746-c502d488b3ea?w=128&auto=format&fit=crop&q=80',
    title: 'Junior Data Analyst / AI Operations',
    description: 'Hỗ trợ kiểm định chất lượng dữ liệu huấn luyện mô hình, theo dõi KPI các tác vụ AI và phân tích hành vi người dùng.',
    requirements: 'Tốt nghiệp ĐH chuyên ngành CNTT/Toán tin. Kỹ năng SQL, Python pandas/numpy và trực quan hóa dữ liệu (Tableau/PowerBI/Recharts).',
    benefits: 'Chương trình đào tạo chuyên sâu bởi các chuyên gia AI hàng đầu. Cơ hội trở thành Data Scientist chính thức sau 6 tháng.',
    jobType: 'full_time',
    location: 'Quận 7, TP.HCM',
    salaryMin: 12000000,
    salaryMax: 18000000,
    currency: 'VND',
    experienceLevel: 'junior',
    status: 'pending_approval',
    requiredSkills: ['Python', 'SQL', 'Data Analysis', 'Data Visualization'],
    preferredSkills: ['PowerBI', 'Tableau', 'Machine Learning basics'],
    createdAt: '2026-10-26T11:00:00Z',
  }
];

export const INITIAL_CVS: CV[] = [
  {
    id: 'cv-1',
    candidateId: 'user-cand-1',
    fileName: 'Nguyen_Van_An_Senior_AI_Engineer.pdf',
    fileUrl: '/uploads/Nguyen_Van_An_CV.pdf',
    fileSize: 1024 * 480, // 480 KB
    isPrimary: true,
    extractionStatus: 'completed',
    parsedData: {
      fullName: 'Nguyễn Văn An',
      email: 'nguyenvanan.ai@gmail.com',
      phone: '0908 123 456',
      summary: 'Kỹ sư AI với hơn 3 năm nghiên cứu và triển khai thực chiến các hệ thống LLM, RAG và mô hình Embedding phục vụ sản phẩm tuyển dụng và tài chính.',
      hardSkills: ['Python', 'FastAPI', 'PyTorch', 'LLMs', 'Vector Databases', 'pgvector', 'Docker', 'SQLAlchemy'],
      softSkills: ['Giải quyết vấn đề', 'Giao tiếp nhóm', 'Tư duy phản biện', 'Quản lý thời gian'],
      education: [
        {
          institution: 'Đại học Bách Khoa TP.HCM',
          degree: 'Kỹ sư',
          fieldOfStudy: 'Khoa học Máy tính & AI',
          startDate: '2019',
          endDate: '2023',
          gpa: '3.6/4.0'
        }
      ],
      experience: [
        {
          companyName: 'AI Solution Lab',
          jobTitle: 'AI Research & Deployment Engineer',
          startDate: '2023',
          endDate: 'Hiện tại',
          isCurrent: true,
          description: 'Xây dựng pipeline RAG tự động xử lý hơn 10.000 hồ sơ ứng viên mỗi ngày với độ chính xác trích xuất đạt 94%.'
        },
        {
          companyName: 'TechVision Vietnam',
          jobTitle: 'Junior Python Developer',
          startDate: '2022',
          endDate: '2023',
          isCurrent: false,
          description: 'Phát triển REST API với FastAPI và PostgreSQL cho ứng dụng phân tích dữ liệu thị trường.'
        }
      ],
      certifications: ['DeepLearning.AI Generative AI Specialization', 'AWS Certified Machine Learning - Specialty'],
      languages: ['Tiếng Việt (Bản ngữ)', 'Tiếng Anh (IELTS 7.5)'],
      missingFields: []
    },
    createdAt: '2026-10-25T10:00:00Z'
  }
];

export const INITIAL_APPLICATIONS: Application[] = [
  {
    id: 'app-1',
    jobId: 'job-1',
    jobTitle: 'Senior AI / Machine Learning Engineer (LLMs & RAG)',
    companyName: 'VNG Corporation',
    candidateId: 'user-cand-1',
    candidateName: 'Nguyễn Văn An',
    candidateEmail: 'nguyenvanan.ai@gmail.com',
    cvId: 'cv-1',
    status: 'reviewing',
    coverLetter: 'Tôi rất ấn tượng với định hướng phát triển AI Agent tại VNG. Với kinh nghiệm chuyên sâu về LLMs, Vector Databases và pgvector, tôi tin mình sẽ đóng góp giá trị ngay từ ngày đầu tiên.',
    internalNotes: 'Ứng viên có nền tảng học thuật vững chắc tại Bách Khoa, CV đạt độ tương thích cao 92% với JD.',
    matchScore: 92,
    matchBreakdown: {
      overallScore: 92,
      hardSkillsScore: 95,
      semanticScore: 90,
      experienceScore: 88,
      matchedSkills: ['Python', 'FastAPI', 'PyTorch', 'LLMs', 'Vector Databases', 'pgvector', 'Docker'],
      missingRequiredSkills: [],
      missingPreferredSkills: ['Kubernetes', 'CI/CD'],
      aiExplanation: 'Ứng viên đáp ứng 100% các kỹ năng bắt buộc (Python, LLMs, PyTorch, pgvector). Độ tương đồng ngữ nghĩa giữa kinh nghiệm thực tế và mô tả công việc đạt mức Xuất sắc.',
      recommendations: [
        'Bổ sung chứng chỉ hoặc dự án thực tế về Kubernetes để tối ưu triển khai production.',
        'Thực hành thêm về CI/CD pipeline cho mô hình AI (MLOps).'
      ]
    },
    createdAt: '2026-10-25T15:30:00Z'
  }
];

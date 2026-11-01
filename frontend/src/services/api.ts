import axios from 'axios';
import { Job, CV, Application, Company, MatchScoreBreakdown } from '../types';
import { INITIAL_JOBS, INITIAL_CVS, INITIAL_APPLICATIONS, INITIAL_COMPANIES } from './mockData';

const rawApiUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1').trim();
const API_BASE_URL = rawApiUrl.endsWith('/api/v1')
  ? rawApiUrl
  : `${rawApiUrl.replace(/\/+$/, '')}/api/v1`;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('hiresense_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Local persistence helpers
const getStored = <T>(key: string, fallback: T): T => {
  const val = localStorage.getItem(key);
  if (!val) {
    localStorage.setItem(key, JSON.stringify(fallback));
    return fallback;
  }
  try {
    return JSON.parse(val);
  } catch {
    return fallback;
  }
};

const setStored = <T>(key: string, val: T): void => {
  localStorage.setItem(key, JSON.stringify(val));
};

export function mapServerJob(raw: any): Job {
  if (!raw) return raw;
  return {
    id: raw.id,
    companyId: raw.company_id || raw.companyId || 'comp-1',
    companyName: raw.company_name || raw.companyName || 'Đối tác',
    companyLogo: raw.company_logo || raw.companyLogo,
    title: raw.title || '',
    description: raw.description || '',
    requirements: raw.requirements || '',
    benefits: raw.benefits || '',
    jobType: raw.job_type || raw.jobType || 'full_time',
    location: raw.location || 'TP.HCM',
    salaryMin: raw.salary_min !== undefined ? raw.salary_min : raw.salaryMin,
    salaryMax: raw.salary_max !== undefined ? raw.salary_max : raw.salaryMax,
    currency: raw.currency || 'VND',
    experienceLevel: raw.experience_level || raw.experienceLevel || 'mid',
    status: raw.status || 'published',
    requiredSkills: Array.isArray(raw.required_skills)
      ? raw.required_skills
      : Array.isArray(raw.requiredSkills)
      ? raw.requiredSkills
      : [],
    preferredSkills: Array.isArray(raw.preferred_skills)
      ? raw.preferred_skills
      : Array.isArray(raw.preferredSkills)
      ? raw.preferredSkills
      : [],
    createdAt: raw.created_at || raw.createdAt || new Date().toISOString(),
  };
}

export function mapServerCV(raw: any): CV {
  if (!raw) return raw;
  const isFailed = raw.extraction_status === 'extraction_failed' || raw.extraction_status === 'failed' || raw.extractionStatus === 'extraction_failed' || raw.extractionStatus === 'failed';
  const parsed = raw.parsed_data || raw.parsedData;
  return {
    id: raw.id,
    candidateId: raw.candidate_id || raw.candidateId || 'user-cand-1',
    fileName: raw.file_name || raw.fileName || 'CV.pdf',
    fileUrl: raw.file_url || raw.fileUrl || '',
    fileSize: raw.file_size || raw.fileSize || 0,
    isPrimary: raw.is_primary !== undefined ? raw.is_primary : (raw.isPrimary ?? false),
    extractionStatus: raw.extraction_status || raw.extractionStatus || (isFailed ? 'extraction_failed' : 'completed'),
    extractionError: raw.extraction_error || raw.extractionError,
    contentValidated: raw.content_validated !== undefined ? raw.content_validated : (raw.contentValidated ?? false),
    userConfirmed: raw.user_confirmed !== undefined ? raw.user_confirmed : (raw.userConfirmed ?? false),
    parsedData: parsed && !parsed.error ? {
      fullName: parsed.full_name || parsed.fullName || '',
      email: parsed.email || '',
      phone: parsed.phone || '',
      address: parsed.address || '',
      summary: parsed.summary || '',
      yearsOfExperience: parsed.years_of_experience !== undefined ? parsed.years_of_experience : (parsed.yearsOfExperience ?? 0),
      education: parsed.education || [],
      experience: parsed.experience || parsed.work_experience || [],
      hardSkills: Array.isArray(parsed.hard_skills) ? parsed.hard_skills : (Array.isArray(parsed.hardSkills) ? parsed.hardSkills : []),
      softSkills: Array.isArray(parsed.soft_skills) ? parsed.soft_skills : (Array.isArray(parsed.softSkills) ? parsed.softSkills : []),
      projects: parsed.projects || [],
      certifications: parsed.certifications || [],
      languages: parsed.languages || [],
      missingFields: parsed.missing_fields || parsed.missingFields || [],
    } : (isFailed ? {
      fullName: 'Lỗi trích xuất',
      email: '',
      phone: '',
      address: '',
      summary: raw.extraction_error || raw.extractionError || 'Không thể đọc nội dung CV.',
      yearsOfExperience: 0,
      education: [],
      experience: [],
      hardSkills: [],
      softSkills: [],
      projects: [],
      certifications: [],
      languages: [],
      missingFields: [raw.extraction_error || raw.extractionError || 'Lỗi trích xuất']
    } : undefined),
    createdAt: raw.created_at || raw.createdAt || new Date().toISOString(),
  };
}

export const apiService = {
  // JOBS
  async getJobs(filters?: { search?: string; location?: string; jobType?: string }): Promise<Job[]> {
    try {
      const res = await apiClient.get('/jobs', { params: filters });
      return Array.isArray(res.data) ? res.data.map(mapServerJob) : [];
    } catch {
      // Fallback to local storage
      let jobs = getStored<Job[]>('hiresense_jobs', INITIAL_JOBS).map(mapServerJob);
      if (filters?.search) {
        const q = filters.search.toLowerCase();
        jobs = jobs.filter(j => j.title.toLowerCase().includes(q) || (j.requiredSkills || []).some(s => s.toLowerCase().includes(q)));
      }
      if (filters?.location && filters.location !== 'all') {
        jobs = jobs.filter(j => j.location.toLowerCase().includes(filters.location!.toLowerCase()));
      }
      if (filters?.jobType && filters.jobType !== 'all') {
        jobs = jobs.filter(j => j.jobType === filters.jobType);
      }
      return jobs;
    }
  },

  async getJobById(id: string): Promise<Job | null> {
    try {
      const res = await apiClient.get(`/jobs/${id}`);
      return res.data ? mapServerJob(res.data) : null;
    } catch {
      const jobs = getStored<Job[]>('hiresense_jobs', INITIAL_JOBS).map(mapServerJob);
      return jobs.find(j => j.id === id) || null;
    }
  },

  async createJob(jobData: Partial<Job>): Promise<Job> {
    try {
      const res = await apiClient.post('/jobs', jobData);
      return res.data;
    } catch {
      const jobs = getStored<Job[]>('hiresense_jobs', INITIAL_JOBS);
      const newJob: Job = {
        id: `job-${Date.now()}`,
        companyId: 'comp-1',
        companyName: 'VNG Corporation',
        title: jobData.title || 'Untitled Role',
        description: jobData.description || '',
        requirements: jobData.requirements || '',
        benefits: jobData.benefits || '',
        jobType: jobData.jobType || 'full_time',
        location: jobData.location || 'TP.HCM',
        salaryMin: jobData.salaryMin,
        salaryMax: jobData.salaryMax,
        currency: 'VND',
        experienceLevel: jobData.experienceLevel || 'mid',
        status: jobData.status || 'published',
        requiredSkills: jobData.requiredSkills || [],
        preferredSkills: jobData.preferredSkills || [],
        createdAt: new Date().toISOString(),
      };
      const updated = [newJob, ...jobs];
      setStored('hiresense_jobs', updated);
      return newJob;
    }
  },

  async updateJobStatus(jobId: string, status: Job['status'], reason?: string): Promise<Job> {
    const jobs = getStored<Job[]>('hiresense_jobs', INITIAL_JOBS);
    const updated = jobs.map(j => {
      if (j.id === jobId) {
        return { ...j, status, rejectionReason: reason };
      }
      return j;
    });
    setStored('hiresense_jobs', updated);
    return updated.find(j => j.id === jobId)!;
  },

  // CVS
  async getCandidateCVs(candidateId: string): Promise<CV[]> {
    let serverCvs: CV[] = [];
    try {
      const res = await apiClient.get(`/cvs?candidate_id=${candidateId}`);
      if (Array.isArray(res.data)) {
        serverCvs = res.data.map(mapServerCV);
      }
    } catch {
      // offline fallback
    }

    const localCvs = getStored<CV[]>('hiresense_cvs', []).map(mapServerCV);
    const combinedMap = new Map<string, CV>();
    for (const cv of serverCvs) {
      combinedMap.set(cv.id, cv);
    }
    for (const cv of localCvs) {
      if (!combinedMap.has(cv.id)) {
        combinedMap.set(cv.id, cv);
      }
    }
    return Array.from(combinedMap.values());
  },

  async uploadAndAnalyzeCV(file: File, candidateId: string = 'user-cand-1'): Promise<CV> {
    // 1. Try real backend API first
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('candidate_id', candidateId);

      const res = await apiClient.post('/cvs/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const serverCV = res.data;
      const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
      const isFailed = serverCV.extraction_status === 'extraction_failed' || serverCV.extraction_status === 'failed';

      const cv: CV = {
        id: serverCV.id,
        candidateId: serverCV.candidate_id,
        fileName: serverCV.file_name,
        fileUrl: serverCV.file_url || URL.createObjectURL(file),
        fileSize: serverCV.file_size,
        isPrimary: cvs.length === 0 || serverCV.is_primary,
        extractionStatus: serverCV.extraction_status,
        extractionError: serverCV.extraction_error,
        contentValidated: serverCV.content_validated,
        parsedData: serverCV.parsed_data ? {
          fullName: serverCV.parsed_data.full_name || 'Không xác định',
          email: serverCV.parsed_data.email || '',
          phone: serverCV.parsed_data.phone || '',
          summary: serverCV.parsed_data.summary || '',
          hardSkills: serverCV.parsed_data.hard_skills || [],
          softSkills: serverCV.parsed_data.soft_skills || [],
          education: serverCV.parsed_data.education || [],
          experience: serverCV.parsed_data.experience || [],
          certifications: serverCV.parsed_data.certifications || [],
          languages: serverCV.parsed_data.languages || [],
          missingFields: serverCV.parsed_data.missing_fields || [],
        } : (isFailed ? {
          fullName: 'Lỗi trích xuất',
          email: '',
          phone: '',
          summary: serverCV.extraction_error || 'Không thể đọc nội dung CV. Vui lòng tải lên file PDF/DOCX hợp lệ hoặc thử một file khác.',
          hardSkills: [],
          softSkills: [],
          education: [],
          experience: [],
          certifications: [],
          languages: [],
          missingFields: [serverCV.extraction_error || 'Không đọc được file'],
        } : undefined),
        createdAt: serverCV.created_at,
      };

      setStored('hiresense_cvs', [cv, ...cvs]);
      return cv;
    } catch (apiErr: any) {
      console.warn('Backend API upload returned error or is offline, running client parser with validation:', apiErr);

      if (apiErr.response?.data?.detail) {
        const detailMsg = typeof apiErr.response.data.detail === 'string'
          ? apiErr.response.data.detail
          : apiErr.response.data.detail.message || 'Tệp không hợp lệ';
        const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
        const failedCv: CV = {
          id: `cv-${Date.now()}`,
          candidateId,
          fileName: file.name,
          fileUrl: URL.createObjectURL(file),
          fileSize: file.size,
          isPrimary: cvs.length === 0,
          extractionStatus: 'failed',
          extractionError: detailMsg,
          contentValidated: false,
          parsedData: {
            fullName: 'Lỗi định dạng',
            email: '',
            phone: '',
            summary: detailMsg,
            hardSkills: [],
            softSkills: [],
            education: [],
            experience: [],
            certifications: [],
            languages: [],
            missingFields: [detailMsg]
          },
          createdAt: new Date().toISOString(),
        };
        setStored('hiresense_cvs', [failedCv, ...cvs]);
        return failedCv;
      }
    }

    // 2. Client-side fallback with strict validation against raw binary PDF
    return new Promise((resolve) => {
      const reader = new FileReader();

      reader.onload = (event) => {
        const rawText = (event.target?.result as string) || '';
        const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);

        // Quality check: Reject raw binary PDF leaks (%PDF- or /Type /Pages)
        const isBinaryPdf = rawText.startsWith('%PDF-') || rawText.includes('/Type') || rawText.includes('/Pages') || rawText.includes('endobj');
        if (isBinaryPdf) {
          const failedCv: CV = {
            id: `cv-${Date.now()}`,
            candidateId,
            fileName: file.name,
            fileUrl: URL.createObjectURL(file),
            fileSize: file.size,
            isPrimary: cvs.length === 0,
            extractionStatus: 'failed',
            extractionError: 'Tệp PDF dạng binary không có text layer hoặc chưa qua parser backend.',
            contentValidated: false,
            parsedData: {
              fullName: 'Lỗi đọc tệp',
              email: '',
              phone: '',
              summary: 'Không thể đọc nội dung CV. Vui lòng tải lên file PDF có văn bản hoặc file DOCX.',
              hardSkills: [],
              softSkills: [],
              education: [],
              experience: [],
              certifications: [],
              languages: [],
              missingFields: ['Tệp PDF dạng binary']
            },
            createdAt: new Date().toISOString(),
          };
          setStored('hiresense_cvs', [failedCv, ...cvs]);
          resolve(failedCv);
          return;
        }

        // --- Bóc tách thông tin từ văn bản thực tế ---
        const lines = rawText.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
        const allText = rawText;

        // Tìm Email
        const emailMatch = allText.match(/[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}/);
        const extractedEmail = emailMatch ? emailMatch[0] : '';

        // Tìm số điện thoại (VN format)
        const phoneMatch = allText.match(/(?:0|\+84)[0-9\s]{8,11}/);
        const extractedPhone = phoneMatch ? phoneMatch[0].trim() : '';

        // Tìm tên (dòng đầu tiên có chữ thường là tên, hoặc dòng sau "Họ tên" / "Họ và tên")
        let extractedName = '';
        const namePatterns = [
          /(?:Họ(?:\s+và)?\s+tên|Full\s*Name|Candidate|Ứng viên)[:\s]+([^\n\r]+)/i,
        ];
        for (const pat of namePatterns) {
          const m = allText.match(pat);
          if (m) { extractedName = m[1].trim(); break; }
        }
        // Nếu không tìm được, dùng dòng đầu tiên (thường là tên trong CV)
        if (!extractedName && lines.length > 0) {
          // Lấy dòng đầu không phải email/sđt/url
          for (const line of lines.slice(0, 5)) {
            if (!line.includes('@') && !line.match(/^\d/) && !line.match(/^http/i) && line.length > 3 && line.length < 80) {
              extractedName = line;
              break;
            }
          }
        }

        // Tóm tắt / Bio
        const bioPatterns = [
          /(?:Đôi nét về bản thân|Giới thiệu|Mục tiêu|Objective|Summary|About me)[:\s]*\n?([\s\S]{20,400}?)(?:\n\n|\n(?=[A-ZĐÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂẮẰẶẲẴỔỒỐỔỔỘỘỢỜỜỚ]))/i
        ];
        let extractedSummary = '';
        for (const pat of bioPatterns) {
          const m = allText.match(pat);
          if (m) { extractedSummary = m[1].replace(/\r?\n/g, ' ').trim().slice(0, 400); break; }
        }

        // Kỹ năng cứng - tìm phần Kỹ năng / Skills
        const skillKeywords = [
          'Python','JavaScript','TypeScript','ReactJS','React','NodeJS','Node.js',
          'FastAPI','Django','Flask','Java','C++','C#','PHP','Ruby','Go','Rust','Swift',
          'PostgreSQL','MySQL','MongoDB','Redis','Elasticsearch',
          'Docker','Kubernetes','AWS','Azure','GCP','Git','CI/CD',
          'Machine Learning','Deep Learning','TensorFlow','PyTorch','LLMs','AI',
          'HTML','CSS','Tailwind','Vue','Angular','NextJS',
          'Tiếng Anh','English','Photoshop','Figma','Excel','Word','PowerPoint',
          'Housekeeping','Dealer','Quản lý','Lễ tân','Du lịch','Khách sạn',
          'Nhà hàng','Phục vụ','Marketing','Sales','Kế toán','Kinh doanh',
          'Giao tiếp','Teamwork','Leadership','Problem solving',
        ];
        const foundHardSkills = skillKeywords.filter(sk =>
          new RegExp('\\b' + sk.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i').test(allText)
        );

        // Kỹ năng mềm - tìm trong nội dung
        const softKeywordMap: Record<string, string> = {
          'giao tiếp': 'Giao tiếp',
          'teamwork': 'Làm việc nhóm',
          'làm việc nhóm': 'Làm việc nhóm',
          'tự chủ': 'Tự chủ trong công việc',
          'tiếp thu': 'Tiếp thu nhanh',
          'thích ứng': 'Thích ứng nhanh',
          'chịu áp lực': 'Chịu áp lực tốt',
          'sáng tạo': 'Sáng tạo',
          'tư duy': 'Tư duy phản biện',
          'trách nhiệm': 'Có trách nhiệm',
          'cẩn thận': 'Cẩn thận, tỉ mỉ',
          'nhiệt tình': 'Nhiệt tình',
          'năng động': 'Năng động',
        };
        const foundSoftSkills: string[] = [];
        const lowerText = allText.toLowerCase();
        for (const [kw, label] of Object.entries(softKeywordMap)) {
          if (lowerText.includes(kw) && !foundSoftSkills.includes(label)) {
            foundSoftSkills.push(label);
          }
        }

        // Kinh nghiệm - tìm các đoạn có năm/tháng kèm tên công ty
        const expBlocks: { companyName: string; jobTitle: string; startDate: string; endDate: string; isCurrent: boolean; description: string }[] = [];
        // Pattern: "Từ MM/YYYY - MM/YYYY" hoặc "YYYY - YYYY"
        const expPattern = /(?:Từ\s+)?(\d{1,2}\/\d{4}|\d{4})\s*[-–]\s*(\d{1,2}\/\d{4}|\d{4}|Hiện tại|nay|present|current)([\s\S]{0,600}?)(?=(?:Từ\s+)?\d{1,2}\/\d{4}|\d{4}\s*[-–]|$)/gi;
        let expMatch;
        while ((expMatch = expPattern.exec(allText)) !== null && expBlocks.length < 5) {
          const block = expMatch[3] || '';
          const blockLines = block.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
          // Tìm công ty và vị trí trong block
          const companyLine = blockLines.find(l => /công ty|company|resort|hotel|club|service|corp|co\.|ltd/i.test(l)) || blockLines[0] || '';
          const positionLine = blockLines.find(l => /vị trí|position|nhân viên|staff|engineer|developer|manager|supervisor|leader/i.test(l)) || blockLines[1] || '';
          const desc = blockLines.slice(2, 6).join(' ').trim();
          const isCurrent = /hiện tại|nay|present|current/i.test(expMatch[2]);
          expBlocks.push({
            companyName: companyLine.replace(/^[-•*]\s*(?:Công ty:|Company:)?\s*/i, '').trim() || 'Chưa xác định',
            jobTitle: positionLine.replace(/^[-•*]\s*(?:Vị trí:|Position:)?\s*/i, '').trim() || 'Nhân viên',
            startDate: expMatch[1],
            endDate: isCurrent ? 'Hiện tại' : expMatch[2],
            isCurrent,
            description: desc,
          });
        }

        // Học vấn
        const eduBlocks: { institution: string; degree: string; fieldOfStudy: string; startDate: string; endDate: string; gpa?: string }[] = [];
        const eduPattern = /(?:Trường|University|College|Học viện|Cao đẳng|Đại học)[^\n]{0,100}/gi;
        let eduMatch;
        while ((eduMatch = eduPattern.exec(allText)) !== null && eduBlocks.length < 3) {
          const eduLine = eduMatch[0].trim();
          // Tìm ngành trong 3 dòng tiếp theo
          const afterIdx = allText.indexOf(eduLine) + eduLine.length;
          const afterText = allText.slice(afterIdx, afterIdx + 300);
          const majorMatch = afterText.match(/(?:Ngành|Chuyên ngành|Major|Field)[:\s]+([^\n\r.]+)/i);
          const yearMatch = afterText.match(/(\d{4})\s*[-–]\s*(\d{4})/);
          const gpaMatch = afterText.match(/GPA[:\s]+([\d.]+)/i);
          const degreeMatch = afterText.match(/(?:Bằng|Degree|Cử nhân|Kỹ sư|Tốt nghiệp)[^\n]{0,60}/i);
          eduBlocks.push({
            institution: eduLine,
            degree: degreeMatch ? degreeMatch[0].trim() : 'Tốt nghiệp',
            fieldOfStudy: majorMatch ? majorMatch[1].trim() : '',
            startDate: yearMatch ? yearMatch[1] : '',
            endDate: yearMatch ? yearMatch[2] : '',
            gpa: gpaMatch ? gpaMatch[1] : undefined,
          });
        }

        const fileName = file.name;
        const newCv: CV = {
          id: `cv-${Date.now()}`,
          candidateId: 'user-cand-1',
          fileName: fileName,
          fileUrl: URL.createObjectURL(file),
          fileSize: file.size,
          isPrimary: cvs.length === 0,
          extractionStatus: 'completed',
          parsedData: {
            fullName: extractedName || fileName.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' '),
            email: extractedEmail,
            phone: extractedPhone,
            summary: extractedSummary,
            hardSkills: foundHardSkills.slice(0, 15),
            softSkills: foundSoftSkills.slice(0, 8),
            education: eduBlocks.length > 0 ? eduBlocks : [],
            experience: expBlocks.length > 0 ? expBlocks : [],
            certifications: [],
            languages: allText.match(/tiếng anh/i) ? ['Tiếng Anh'] : [],
            missingFields: [
              ...(!extractedName ? ['Họ tên'] : []),
              ...(!extractedEmail ? ['Email'] : []),
              ...(!extractedPhone ? ['Số điện thoại'] : []),
              ...(expBlocks.length === 0 ? ['Kinh nghiệm làm việc'] : []),
            ]
          },
          createdAt: new Date().toISOString(),
        };
        const updated = [newCv, ...cvs];
        setStored('hiresense_cvs', updated);
        resolve(newCv);
      };

      reader.onerror = () => {
        // Fallback nếu không đọc được file
        const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
        const newCv: CV = {
          id: `cv-${Date.now()}`,
          candidateId: 'user-cand-1',
          fileName: file.name,
          fileUrl: URL.createObjectURL(file),
          fileSize: file.size,
          isPrimary: cvs.length === 0,
          extractionStatus: 'failed',
          parsedData: {
            fullName: file.name.replace(/\.[^/.]+$/, ''),
            email: '',
            phone: '',
            summary: 'Không thể đọc nội dung file. Vui lòng tải lên file .pdf có text layer hoặc file .txt.',
            hardSkills: [],
            softSkills: [],
            education: [],
            experience: [],
            certifications: [],
            languages: [],
            missingFields: ['Không đọc được file']
          },
          createdAt: new Date().toISOString(),
        };
        setStored('hiresense_cvs', [newCv, ...cvs]);
        resolve(newCv);
      };

      // Đọc file dưới dạng text (hỗ trợ PDF text layer và .txt)
      reader.readAsText(file, 'UTF-8');
    });
  },


  async deleteCV(cvId: string): Promise<boolean> {
    try {
      await apiClient.delete(`/cvs/${cvId}`);
    } catch (err: any) {
      console.warn('Backend delete CV error or offline:', err?.message);
    }
    const cvs = getStored<CV[]>('hiresense_cvs', []);
    const updated = cvs.filter(c => c.id !== cvId);
    setStored('hiresense_cvs', updated);

    // Also clear from any user-specific storage keys
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith('hiresense_cvs')) {
          const items = JSON.parse(localStorage.getItem(key) || '[]');
          if (Array.isArray(items)) {
            const filtered = items.filter((c: any) => c.id !== cvId);
            localStorage.setItem(key, JSON.stringify(filtered));
          }
        }
      }
    } catch {}
    return true;
  },

  async setPrimaryCV(cvId: string): Promise<boolean> {
    try {
      await apiClient.put(`/cvs/${cvId}/primary`);
    } catch (err: any) {
      console.warn('Backend set primary CV error or offline:', err?.message);
    }
    const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
    const updated = cvs.map(c => ({
      ...c,
      isPrimary: c.id === cvId
    }));
    setStored('hiresense_cvs', updated);
    return true;
  },

  // MATCHING
  calculateMatchScore(cv: CV, job: Job): MatchScoreBreakdown {
    // If CV extraction failed or is invalid, BLOCK calculation and return 0
    if (cv.extractionStatus === 'failed' || cv.extractionStatus === 'extraction_failed' || !cv.parsedData) {
      return {
        overallScore: 0,
        hardSkillsScore: 0,
        semanticScore: 0,
        experienceScore: 0,
        matchedSkills: [],
        missingRequiredSkills: job.requiredSkills || [],
        missingPreferredSkills: job.preferredSkills || [],
        aiExplanation: 'Không thể tính điểm do dữ liệu CV chưa được trích xuất chính xác hoặc bị lỗi.',
        recommendations: ['Vui lòng tải lên file CV hợp lệ để hệ thống phân tích.'],
      };
    }

    const cvSkills = cv.parsedData.hardSkills.map(s => s.toLowerCase());
    const reqSkills = (job.requiredSkills || []).map(s => s.toLowerCase());
    const prefSkills = (job.preferredSkills || []).map(s => s.toLowerCase());

    const matchedReq = (job.requiredSkills || []).filter(s => cvSkills.includes(s.toLowerCase()));
    const missingReq = (job.requiredSkills || []).filter(s => !cvSkills.includes(s.toLowerCase()));
    const matchedPref = (job.preferredSkills || []).filter(s => cvSkills.includes(s.toLowerCase()));
    const missingPref = (job.preferredSkills || []).filter(s => !cvSkills.includes(s.toLowerCase()));

    const hardSkillRatio = reqSkills.length > 0 ? (matchedReq.length / reqSkills.length) : 0;
    const prefRatio = prefSkills.length > 0 ? (matchedPref.length / prefSkills.length) : 0;

    const hardSkillsScore = Math.round(hardSkillRatio * 100);

    // Realistic semantic score: NO arbitrary 82 baseline!
    let semanticScore = 0;
    if (hardSkillsScore > 0) {
      semanticScore = Math.min(100, Math.round(40 + (hardSkillsScore * 0.4) + (matchedPref.length * 5)));
    } else if (matchedPref.length > 0) {
      semanticScore = Math.min(25, matchedPref.length * 8);
    } else {
      semanticScore = 0;
    }

    // Realistic experience score: NO arbitrary 85 baseline!
    const hasExp = (cv.parsedData.experience || []).length > 0;
    let experienceScore = 0;
    if (!hasExp && hardSkillsScore === 0) {
      experienceScore = 0;
    } else if (!hasExp) {
      experienceScore = Math.round(hardSkillsScore * 0.25);
    } else if (hardSkillsScore === 0) {
      experienceScore = Math.min(15, Math.round(prefRatio * 20));
    } else {
      experienceScore = Math.min(100, Math.round(55 + (prefRatio * 25) + (hardSkillsScore * 0.2)));
    }

    // Hybrid formula
    const overallScore = Math.min(100, Math.round((hardSkillsScore * 0.5) + (semanticScore * 0.3) + (experienceScore * 0.2)));

    let aiExplanation = '';
    if (overallScore >= 80) {
      aiExplanation = `Hồ sơ có độ tương thích cao (${overallScore}%). Ứng viên đáp ứng ${matchedReq.length}/${job.requiredSkills.length} kỹ năng bắt buộc và có kinh nghiệm thực tế phù hợp.`;
    } else if (overallScore >= 45) {
      aiExplanation = `Hồ sơ tương thích một phần (${overallScore}%). Ứng viên đáp ứng ${matchedReq.length}/${job.requiredSkills.length} kỹ năng cốt lõi. Cần bổ sung thêm kỹ năng chuyên sâu.`;
    } else {
      aiExplanation = `Hồ sơ tương thích thấp (${overallScore}%). Thiếu ${missingReq.length} kỹ năng bắt buộc cho vị trí này.`;
    }

    if (missingReq.length > 0) {
      aiExplanation += ` Cần chú ý đánh giá thêm kỹ năng còn thiếu: ${missingReq.join(', ')}.`;
    }

    const recommendations = missingReq.map(skill => `Bổ sung dự án thực tế hoặc chứng chỉ liên quan đến ${skill}.`);
    if (missingPref.length > 0) {
      recommendations.push(`Tìm hiểu thêm về ${missingPref.slice(0, 2).join(', ')} để nâng cao tính cạnh tranh so với các ứng viên khác.`);
    }

    return {
      overallScore,
      hardSkillsScore,
      semanticScore,
      experienceScore,
      matchedSkills: [...matchedReq, ...matchedPref],
      missingRequiredSkills: missingReq,
      missingPreferredSkills: missingPref,
      aiExplanation,
      recommendations,
    };
  },

  async calculateMatchViaBackend(cvId: string, jobId: string): Promise<MatchScoreBreakdown> {
    const res = await apiClient.post('/matching/calculate', {
      cv_id: cvId,
      job_id: jobId,
    });
    return res.data;
  },

  // APPLICATIONS
  async applyToJob(jobId: string, cvId: string, coverLetter?: string): Promise<Application> {
    const jobs = getStored<Job[]>('hiresense_jobs', INITIAL_JOBS);
    const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
    const apps = getStored<Application[]>('hiresense_applications', INITIAL_APPLICATIONS);

    const job = jobs.find(j => j.id === jobId);
    const cv = cvs.find(c => c.id === cvId) || cvs[0];

    const breakdown = job && cv ? this.calculateMatchScore(cv, job) : undefined;

    const newApp: Application = {
      id: `app-${Date.now()}`,
      jobId,
      jobTitle: job?.title || 'Công việc đã ứng tuyển',
      companyName: job?.companyName || 'Công ty đối tác',
      candidateId: 'user-cand-1',
      candidateName: cv?.parsedData?.fullName || 'Nguyễn Văn An',
      candidateEmail: cv?.parsedData?.email || 'nguyenvanan.ai@gmail.com',
      cvId,
      status: 'submitted',
      coverLetter,
      matchScore: breakdown?.overallScore || 85,
      matchBreakdown: breakdown,
      createdAt: new Date().toISOString(),
    };

    const updated = [newApp, ...apps];
    setStored('hiresense_applications', updated);
    return newApp;
  },

  async getApplications(role: 'candidate' | 'recruiter' | 'admin'): Promise<Application[]> {
    const rawApps = getStored<Application[]>('hiresense_applications', INITIAL_APPLICATIONS);
    const apps = rawApps.map(a => ({
      ...a,
      matchScore: a.matchScore ?? 0,
      matchBreakdown: a.matchBreakdown ? {
        ...a.matchBreakdown,
        matchedSkills: Array.isArray(a.matchBreakdown.matchedSkills) ? a.matchBreakdown.matchedSkills : [],
        missingRequiredSkills: Array.isArray(a.matchBreakdown.missingRequiredSkills) ? a.matchBreakdown.missingRequiredSkills : [],
        missingPreferredSkills: Array.isArray(a.matchBreakdown.missingPreferredSkills) ? a.matchBreakdown.missingPreferredSkills : [],
      } : undefined
    }));
    if (role === 'candidate') {
      return apps.filter(a => a.candidateId === 'user-cand-1');
    }
    return apps;
  },

  async updateApplicationStatus(appId: string, status: Application['status'], notes?: string): Promise<Application> {
    const apps = getStored<Application[]>('hiresense_applications', INITIAL_APPLICATIONS);
    const updated = apps.map(a => {
      if (a.id === appId) {
        return {
          ...a,
          status,
          internalNotes: notes !== undefined ? notes : a.internalNotes,
        };
      }
      return a;
    });
    setStored('hiresense_applications', updated);
    return updated.find(a => a.id === appId)!;
  },

  // COMPANIES
  async getCompanies(): Promise<Company[]> {
    return getStored<Company[]>('hiresense_companies', INITIAL_COMPANIES);
  }
};

import axios from 'axios';
import { Job, CV, Application, Company, MatchScoreBreakdown } from '../types';
import { INITIAL_JOBS, INITIAL_CVS, INITIAL_APPLICATIONS, INITIAL_COMPANIES } from './mockData';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
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

export const apiService = {
  // JOBS
  async getJobs(filters?: { search?: string; location?: string; jobType?: string }): Promise<Job[]> {
    try {
      const res = await apiClient.get('/jobs', { params: filters });
      return res.data;
    } catch {
      // Fallback to local storage
      let jobs = getStored<Job[]>('hiresense_jobs', INITIAL_JOBS);
      if (filters?.search) {
        const q = filters.search.toLowerCase();
        jobs = jobs.filter(j => j.title.toLowerCase().includes(q) || j.requiredSkills.some(s => s.toLowerCase().includes(q)));
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
      return res.data;
    } catch {
      const jobs = getStored<Job[]>('hiresense_jobs', INITIAL_JOBS);
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
    try {
      const res = await apiClient.get(`/cvs?candidate_id=${candidateId}`);
      return res.data;
    } catch {
      return getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
    }
  },

  async uploadAndAnalyzeCV(file: File): Promise<CV> {
    // Simulate Gemini LLM extraction pipeline with accurate structured breakdown
    return new Promise((resolve) => {
      setTimeout(() => {
        const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
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
            fullName: 'Ứng viên ' + fileName.replace(/\.[^/.]+$/, ""),
            email: 'candidate.ai@hiresense.vn',
            phone: '0901 234 567',
            summary: 'Chuyên gia phần mềm và AI định hướng sản phẩm với khả năng thích ứng công nghệ mới và tư duy giải quyết vấn đề xuất sắc.',
            hardSkills: ['Python', 'FastAPI', 'ReactJS', 'TypeScript', 'PostgreSQL', 'Docker', 'Machine Learning', 'Git'],
            softSkills: ['Làm việc nhóm', 'Thuyết trình kỹ thuật', 'Tư duy phản biện', 'Tiếng Anh giao tiếp'],
            education: [
              {
                institution: 'Đại học Quốc Gia TP.HCM',
                degree: 'Cử nhân CNTT',
                fieldOfStudy: 'Kỹ thuật Phần mềm',
                startDate: '2020',
                endDate: '2024',
                gpa: '3.5/4.0'
              }
            ],
            experience: [
              {
                companyName: 'FPT Software / AI Team',
                jobTitle: 'Software Engineer',
                startDate: '2024',
                endDate: 'Hiện tại',
                isCurrent: true,
                description: 'Tham gia xây dựng kiến trúc web ứng dụng LLM và tối ưu hiệu suất truy vấn dữ liệu lớn.'
              }
            ],
            certifications: ['AWS Certified Cloud Practitioner', 'Google Cloud AI Specialization'],
            languages: ['Tiếng Việt', 'Tiếng Anh (B2+)'],
            missingFields: []
          },
          createdAt: new Date().toISOString(),
        };
        const updated = [newCv, ...cvs];
        setStored('hiresense_cvs', updated);
        resolve(newCv);
      }, 1500);
    });
  },

  async deleteCV(cvId: string): Promise<boolean> {
    const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
    const updated = cvs.filter(c => c.id !== cvId);
    setStored('hiresense_cvs', updated);
    return true;
  },

  async setPrimaryCV(cvId: string): Promise<boolean> {
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
    const cvSkills = cv.parsedData?.hardSkills.map(s => s.toLowerCase()) || [];
    const reqSkills = job.requiredSkills.map(s => s.toLowerCase());
    const prefSkills = job.preferredSkills.map(s => s.toLowerCase());

    const matchedReq = job.requiredSkills.filter(s => cvSkills.includes(s.toLowerCase()));
    const missingReq = job.requiredSkills.filter(s => !cvSkills.includes(s.toLowerCase()));
    const matchedPref = job.preferredSkills.filter(s => cvSkills.includes(s.toLowerCase()));
    const missingPref = job.preferredSkills.filter(s => !cvSkills.includes(s.toLowerCase()));

    const hardSkillRatio = reqSkills.length > 0 ? (matchedReq.length / reqSkills.length) : 1;
    const prefRatio = prefSkills.length > 0 ? (matchedPref.length / prefSkills.length) : 0.8;

    const hardSkillsScore = Math.round(hardSkillRatio * 100);
    const semanticScore = Math.round(82 + (matchedReq.length * 2.5));
    const experienceScore = Math.round(85 + (matchedPref.length * 3));
    
    // Hybrid weighted formulation
    const overallScore = Math.min(99, Math.round((hardSkillsScore * 0.5) + (semanticScore * 0.3) + (experienceScore * 0.2)));

    let aiExplanation = `Hồ sơ có độ tương thích cao (${overallScore}%). Ứng viên đáp ứng ${matchedReq.length}/${job.requiredSkills.length} kỹ năng bắt buộc và có kinh nghiệm thực tế liên quan mật thiết đến yêu cầu công việc.`;
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
      semanticScore: Math.min(100, semanticScore),
      experienceScore: Math.min(100, experienceScore),
      matchedSkills: [...matchedReq, ...matchedPref],
      missingRequiredSkills: missingReq,
      missingPreferredSkills: missingPref,
      aiExplanation,
      recommendations,
    };
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
    const apps = getStored<Application[]>('hiresense_applications', INITIAL_APPLICATIONS);
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

import axios from 'axios';
import { Job, CV, Application, Company, MatchScoreBreakdown } from '../types';
import { INITIAL_JOBS, INITIAL_CVS, INITIAL_APPLICATIONS, INITIAL_COMPANIES } from './mockData';

const rawApiUrl = (import.meta.env.VITE_API_URL || '').trim();
let resolvedBaseUrl = '/api/v1';
if (rawApiUrl) {
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1' && rawApiUrl.includes('localhost')) {
    resolvedBaseUrl = '/api/v1';
  } else {
    resolvedBaseUrl = rawApiUrl.endsWith('/api/v1') ? rawApiUrl : `${rawApiUrl.replace(/\/+$/, '')}/api/v1`;
  }
}
const API_BASE_URL = resolvedBaseUrl;

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60s for AI extraction pipeline
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
    let parsed = JSON.parse(val);
    // Auto-clean stale error items from previous client-side reader bug
    if (key === 'hiresense_cvs' && Array.isArray(parsed)) {
      parsed = parsed.filter((c: any) => 
        c.extractionError !== 'Tệp PDF dạng binary không có text layer hoặc chưa qua parser backend.'
      );
      localStorage.setItem(key, JSON.stringify(parsed));
    }
    return parsed;
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

      const res = await apiClient.post('/cvs/upload', formData);

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
      console.error('Lỗi khi tải lên và phân tích CV:', apiErr);

      let detailMsg = 'Không thể kết nối đến máy chủ Backend AI. Vui lòng kiểm tra lại dịch vụ Backend.';
      if (apiErr.code === 'ECONNABORTED' || apiErr.message?.includes('timeout')) {
        detailMsg = 'Hệ thống AI xử lý tệp quá thời gian chờ (timeout). Vui lòng thử lại.';
      } else if (apiErr.response?.data?.detail) {
        detailMsg = typeof apiErr.response.data.detail === 'string'
          ? apiErr.response.data.detail
          : (apiErr.response.data.detail.message || JSON.stringify(apiErr.response.data.detail));
      } else if (apiErr.message) {
        detailMsg = `Lỗi kết nối máy chủ: ${apiErr.message}`;
      }

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
          fullName: 'Lỗi tải lên',
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
  },

  // MOBILE AVATAR & LOGO UPLOAD
  async uploadAvatar(file: File, userId?: string): Promise<string> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (userId) formData.append('user_id', userId);
      const res = await apiClient.post('/cvs/upload-avatar', formData);
      return res.data.file_url;
    } catch (err) {
      console.warn('Backend upload-avatar failed, fallback to local object URL:', err);
      return URL.createObjectURL(file);
    }
  },

  async uploadCompanyLogo(file: File, companyId?: string): Promise<string> {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (companyId) formData.append('company_id', companyId);
      const res = await apiClient.post('/cvs/upload-logo', formData);
      return res.data.logo_url;
    } catch (err) {
      console.warn('Backend upload-logo failed, fallback to local object URL:', err);
      return URL.createObjectURL(file);
    }
  },

  // CANDIDATE REVIEW & EDIT CV PARSED DATA
  async updateCVParsedData(cvId: string, updatedData: any): Promise<CV> {
    try {
      const res = await apiClient.put(`/cvs/${cvId}/parsed-data`, updatedData);
      const serverCV = res.data;
      const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
      const idx = cvs.findIndex(c => c.id === cvId);
      const updated: CV = {
        ...cvs[idx],
        contentValidated: serverCV.content_validated,
        extractionStatus: serverCV.extraction_status,
        parsedData: serverCV.parsed_data ? {
          fullName: serverCV.parsed_data.full_name,
          email: serverCV.parsed_data.email,
          phone: serverCV.parsed_data.phone,
          summary: serverCV.parsed_data.summary,
          hardSkills: serverCV.parsed_data.hard_skills || [],
          softSkills: serverCV.parsed_data.soft_skills || [],
          education: serverCV.parsed_data.education || [],
          experience: serverCV.parsed_data.experience || [],
          projects: serverCV.parsed_data.projects || [],
          certifications: serverCV.parsed_data.certifications || [],
          languages: serverCV.parsed_data.languages || [],
          missingFields: serverCV.parsed_data.missing_fields || [],
        } : cvs[idx]?.parsedData,
      };
      if (idx !== -1) {
        cvs[idx] = updated;
        setStored('hiresense_cvs', cvs);
      }
      return updated;
    } catch {
      // Offline fallback
      const cvs = getStored<CV[]>('hiresense_cvs', INITIAL_CVS);
      const idx = cvs.findIndex(c => c.id === cvId);
      if (idx !== -1) {
        cvs[idx] = {
          ...cvs[idx],
          contentValidated: true,
          parsedData: {
            ...cvs[idx].parsedData,
            ...updatedData,
          } as any,
        };
        setStored('hiresense_cvs', cvs);
        return cvs[idx];
      }
      throw new Error('CV not found');
    }
  }
};

export type UserRole = 'candidate' | 'recruiter' | 'admin';

export interface User {
  id: string;
  email: string;
  fullName: string;
  phone?: string;
  role: UserRole;
  isActive: boolean;
  isVerified: boolean;
  createdAt: string;
}

export interface CandidateProfile {
  id: string;
  userId: string;
  title: string;
  bio: string;
  location: string;
  yearsOfExperience: number;
  expectedSalary?: number;
  githubUrl?: string;
  linkedinUrl?: string;
  portfolioUrl?: string;
}

export interface Company {
  id: string;
  name: string;
  slug: string;
  logoUrl?: string;
  website?: string;
  industry: string;
  companySize: string;
  address: string;
  description: string;
  status: 'pending' | 'approved' | 'rejected';
}

export type JobType = 'full_time' | 'part_time' | 'remote' | 'hybrid' | 'internship';
export type JobStatus = 'draft' | 'pending_approval' | 'published' | 'closed' | 'rejected';
export type ExperienceLevel = 'entry' | 'junior' | 'mid' | 'senior' | 'lead';

export interface Job {
  id: string;
  companyId: string;
  companyName: string;
  companyLogo?: string;
  title: string;
  description: string;
  requirements: string;
  benefits?: string;
  jobType: JobType;
  location: string;
  salaryMin?: number;
  salaryMax?: number;
  currency: string;
  experienceLevel: ExperienceLevel;
  status: JobStatus;
  requiredSkills: string[];
  preferredSkills: string[];
  createdAt: string;
  rejectionReason?: string;
}

export interface EducationItem {
  institution: string;
  degree?: string;
  fieldOfStudy?: string;
  startDate?: string;
  endDate?: string;
  gpa?: string;
}

export interface ExperienceItem {
  companyName: string;
  jobTitle: string;
  startDate?: string;
  endDate?: string;
  isCurrent: boolean;
  description?: string;
}

export interface CVExtractedData {
  fullName?: string;
  email?: string;
  phone?: string;
  summary?: string;
  hardSkills: string[];
  softSkills: string[];
  education: EducationItem[];
  experience: ExperienceItem[];
  certifications: string[];
  languages: string[];
  missingFields: string[];
}

export interface CV {
  id: string;
  candidateId: string;
  fileName: string;
  fileUrl: string;
  fileSize: number;
  isPrimary: boolean;
  extractionStatus: 'pending' | 'processing' | 'completed' | 'failed';
  parsedData?: CVExtractedData;
  createdAt: string;
}

export type ApplicationStatus = 
  | 'submitted'
  | 'reviewing'
  | 'shortlisted'
  | 'interviewed'
  | 'offered'
  | 'rejected'
  | 'withdrawn';

export interface MatchScoreBreakdown {
  overallScore: number; // 0 - 100
  hardSkillsScore: number;
  semanticScore: number;
  experienceScore: number;
  matchedSkills: string[];
  missingRequiredSkills: string[];
  missingPreferredSkills: string[];
  aiExplanation: string;
  recommendations: string[];
}

export interface Application {
  id: string;
  jobId: string;
  jobTitle: string;
  companyName: string;
  candidateId: string;
  candidateName: string;
  candidateEmail: string;
  cvId: string;
  status: ApplicationStatus;
  coverLetter?: string;
  internalNotes?: string;
  matchScore?: number;
  matchBreakdown?: MatchScoreBreakdown;
  createdAt: string;
}

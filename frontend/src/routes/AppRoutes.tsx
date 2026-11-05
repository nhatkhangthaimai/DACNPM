import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from '../components/layout/DashboardLayout';
import { LoadingFallback } from '../components/ui/LoadingFallback';

// Public pages - Lazy Loaded for Bundle Size Optimization
const LandingPage = lazy(() => import('../pages/public/LandingPage').then(m => ({ default: m.LandingPage })));
const LoginPage = lazy(() => import('../pages/auth/LoginPage').then(m => ({ default: m.LoginPage })));
const RegisterCandidatePage = lazy(() => import('../pages/auth/RegisterCandidatePage').then(m => ({ default: m.RegisterCandidatePage })));
const RegisterRecruiterPage = lazy(() => import('../pages/auth/RegisterRecruiterPage').then(m => ({ default: m.RegisterRecruiterPage })));
const NotFoundPage = lazy(() => import('../pages/public/NotFoundPage').then(m => ({ default: m.NotFoundPage })));
const PrivacyPolicyPage = lazy(() => import('../pages/public/PrivacyPolicyPage').then(m => ({ default: m.PrivacyPolicyPage })));
const TermsOfServicePage = lazy(() => import('../pages/public/TermsOfServicePage').then(m => ({ default: m.TermsOfServicePage })));

// Candidate pages - Lazy Loaded
const CandidateDashboard = lazy(() => import('../pages/candidate/CandidateDashboard').then(m => ({ default: m.CandidateDashboard })));
const JobDiscovery = lazy(() => import('../pages/candidate/JobDiscovery').then(m => ({ default: m.JobDiscovery })));
const CVManagement = lazy(() => import('../pages/candidate/CVManagement').then(m => ({ default: m.CVManagement })));
const JobMatchingCenter = lazy(() => import('../pages/candidate/JobMatchingCenter').then(m => ({ default: m.JobMatchingCenter })));
const CandidateApplications = lazy(() => import('../pages/candidate/CandidateApplications').then(m => ({ default: m.CandidateApplications })));
const CandidateProfilePage = lazy(() => import('../pages/candidate/CandidateProfilePage').then(m => ({ default: m.CandidateProfilePage })));

// Recruiter pages - Lazy Loaded
const RecruiterDashboard = lazy(() => import('../pages/recruiter/RecruiterDashboard').then(m => ({ default: m.RecruiterDashboard })));
const JobManagement = lazy(() => import('../pages/recruiter/JobManagement').then(m => ({ default: m.JobManagement })));
const CreateJobPage = lazy(() => import('../pages/recruiter/CreateJobPage').then(m => ({ default: m.CreateJobPage })));
const CandidateRanking = lazy(() => import('../pages/recruiter/CandidateRanking').then(m => ({ default: m.CandidateRanking })));
const CompanyProfilePage = lazy(() => import('../pages/recruiter/CompanyProfilePage').then(m => ({ default: m.CompanyProfilePage })));

// Admin pages - Lazy Loaded
const AdminDashboard = lazy(() => import('../pages/admin/AdminDashboard').then(m => ({ default: m.AdminDashboard })));
const JobModeration = lazy(() => import('../pages/admin/JobModeration').then(m => ({ default: m.JobModeration })));
const UserManagement = lazy(() => import('../pages/admin/UserManagement').then(m => ({ default: m.UserManagement })));
const AdminCompanies = lazy(() => import('../pages/admin/AdminCompanies').then(m => ({ default: m.AdminCompanies })));
const SystemReports = lazy(() => import('../pages/admin/SystemReports').then(m => ({ default: m.SystemReports })));

export const AppRoutes: React.FC = () => {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register/candidate" element={<RegisterCandidatePage />} />
        <Route path="/register/recruiter" element={<RegisterRecruiterPage />} />
        <Route path="/privacy" element={<PrivacyPolicyPage />} />
        <Route path="/terms" element={<TermsOfServicePage />} />

        {/* Candidate Portal */}
        <Route path="/candidate" element={<DashboardLayout />}>
          <Route index element={<Navigate to="/candidate/dashboard" replace />} />
          <Route path="dashboard" element={<CandidateDashboard />} />
          <Route path="jobs" element={<JobDiscovery />} />
          <Route path="cvs" element={<CVManagement />} />
          <Route path="matching" element={<JobMatchingCenter />} />
          <Route path="applications" element={<CandidateApplications />} />
          <Route path="profile" element={<CandidateProfilePage />} />
        </Route>

        {/* Recruiter Portal */}
        <Route path="/recruiter" element={<DashboardLayout />}>
          <Route index element={<Navigate to="/recruiter/dashboard" replace />} />
          <Route path="dashboard" element={<RecruiterDashboard />} />
          <Route path="jobs" element={<JobManagement />} />
          <Route path="jobs/new" element={<CreateJobPage />} />
          <Route path="applications" element={<CandidateRanking />} />
          <Route path="company" element={<CompanyProfilePage />} />
        </Route>

        {/* Admin Portal */}
        <Route path="/admin" element={<DashboardLayout />}>
          <Route index element={<Navigate to="/admin/dashboard" replace />} />
          <Route path="dashboard" element={<AdminDashboard />} />
          <Route path="moderation" element={<JobModeration />} />
          <Route path="users" element={<UserManagement />} />
          <Route path="companies" element={<AdminCompanies />} />
          <Route path="reports" element={<SystemReports />} />
        </Route>

        {/* Fallback 404 */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
};

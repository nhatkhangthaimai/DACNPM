import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from '../components/layout/DashboardLayout';

// Public pages
import { LandingPage } from '../pages/public/LandingPage';
import { LoginPage } from '../pages/auth/LoginPage';
import { RegisterCandidatePage } from '../pages/auth/RegisterCandidatePage';
import { RegisterRecruiterPage } from '../pages/auth/RegisterRecruiterPage';
import { NotFoundPage } from '../pages/public/NotFoundPage';

// Candidate pages
import { CandidateDashboard } from '../pages/candidate/CandidateDashboard';
import { JobDiscovery } from '../pages/candidate/JobDiscovery';
import { CVManagement } from '../pages/candidate/CVManagement';
import { JobMatchingCenter } from '../pages/candidate/JobMatchingCenter';
import { CandidateApplications } from '../pages/candidate/CandidateApplications';
import { CandidateProfilePage } from '../pages/candidate/CandidateProfilePage';

// Recruiter pages
import { RecruiterDashboard } from '../pages/recruiter/RecruiterDashboard';
import { JobManagement } from '../pages/recruiter/JobManagement';
import { CreateJobPage } from '../pages/recruiter/CreateJobPage';
import { CandidateRanking } from '../pages/recruiter/CandidateRanking';
import { CompanyProfilePage } from '../pages/recruiter/CompanyProfilePage';

// Admin pages
import { AdminDashboard } from '../pages/admin/AdminDashboard';
import { JobModeration } from '../pages/admin/JobModeration';
import { UserManagement } from '../pages/admin/UserManagement';
import { AdminCompanies } from '../pages/admin/AdminCompanies';
import { SystemReports } from '../pages/admin/SystemReports';

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register/candidate" element={<RegisterCandidatePage />} />
      <Route path="/register/recruiter" element={<RegisterRecruiterPage />} />

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

      {/* 404 Fallback */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
};

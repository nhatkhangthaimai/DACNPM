import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import { Application, Job } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { MatchScoreRing } from '../../components/ui/MatchScoreRing';
import { StatusBadge, SkillBadge } from '../../components/ui/SkillBadge';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { SkillGapPanel } from '../../components/ui/SkillGapPanel';
import { Users, Sparkles, Filter, CheckCircle2, XCircle, FileText, ChevronRight } from 'lucide-react';

export const CandidateRanking: React.FC = () => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJobFilter, setSelectedJobFilter] = useState<string>('all');
  const [selectedAppForReport, setSelectedAppForReport] = useState<Application | null>(null);
  const [internalNotesEdit, setInternalNotesEdit] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = () => {
    Promise.all([
      apiService.getApplications('recruiter'),
      apiService.getJobs(),
    ]).then(([appsData, jobsData]) => {
      setApplications(appsData);
      setJobs(jobsData);
    });
  };

  const handleUpdateStatus = async (appId: string, status: Application['status']) => {
    await apiService.updateApplicationStatus(appId, status);
    loadData();
  };

  const handleSaveNotes = async () => {
    if (!selectedAppForReport) return;
    await apiService.updateApplicationStatus(selectedAppForReport.id, selectedAppForReport.status, internalNotesEdit);
    setSelectedAppForReport(prev => prev ? { ...prev, internalNotes: internalNotesEdit } : null);
    loadData();
  };

  const filteredApps = applications
    .filter(a => selectedJobFilter === 'all' || a.jobId === selectedJobFilter)
    .sort((a, b) => (b.matchScore || 0) - (a.matchScore || 0));

  return (
    <div className="space-y-6">
      <PageHeader
        title="Bảng Xếp hạng Ứng viên Thông minh (AI Candidate Ranking)"
        subtitle="Hệ thống tự động chấm điểm và xếp hạng ứng viên dựa trên độ khớp kỹ năng thực tế và mô hình ngữ nghĩa Gemini."
        badge="Live AI Scoring"
      />

      {/* Filter by Job */}
      <div className="bg-white p-4 sm:p-5 rounded-3xl border border-slate-200/80 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <span className="text-xs font-semibold uppercase text-signal-slate">Lọc theo JD:</span>
          <select
            value={selectedJobFilter}
            onChange={(e) => setSelectedJobFilter(e.target.value)}
            className="bg-signal-offwhite text-sm font-semibold rounded-xl px-4 py-2 border border-slate-200 focus:outline-none focus:border-signal-navy"
          >
            <option value="all">Tất cả vị trí tuyển dụng</option>
            {jobs.map((j) => (
              <option key={j.id} value={j.id}>
                {j.title}
              </option>
            ))}
          </select>
        </div>

        <span className="text-xs text-signal-slate font-medium">
          Tìm thấy {filteredApps.length} ứng viên đã nộp đơn
        </span>
      </div>

      {/* Candidate Ranking List */}
      <div className="space-y-4">
        {filteredApps.map((app, index) => (
          <div
            key={app.id}
            className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm hover:shadow-md transition-all flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6"
          >
            <div className="flex items-start gap-5">
              {/* Rank Position Chip & Score Ring */}
              <div className="flex items-center gap-3 shrink-0">
                <div className="w-8 h-8 rounded-full bg-signal-navy text-white flex items-center justify-center font-heading font-bold text-sm">
                  #{index + 1}
                </div>
                <MatchScoreRing score={app.matchScore || 85} size={76} strokeWidth={6} />
              </div>

              <div>
                <div className="flex items-center gap-2.5 mb-1">
                  <h4 className="font-heading font-bold text-lg text-signal-navy">
                    {app.candidateName}
                  </h4>
                  <StatusBadge status={app.status} />
                </div>
                <span className="text-xs text-signal-slate block mb-2">
                  Ứng tuyển: <strong className="text-signal-navy">{app.jobTitle}</strong> · Email: {app.candidateEmail}
                </span>

                {app.matchBreakdown && (
                  <div className="flex flex-wrap items-center gap-1.5 text-xs">
                    <span className="text-emerald-700 font-semibold mr-1">
                      Kỹ năng khớp: {app.matchBreakdown.matchedSkills.slice(0, 4).join(', ')}
                    </span>
                    {app.matchBreakdown.missingRequiredSkills.length > 0 && (
                      <span className="text-rose-600 font-semibold">
                        · Thiếu: {app.matchBreakdown.missingRequiredSkills.join(', ')}
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Status change and actions */}
            <div className="flex flex-wrap items-center gap-2.5 w-full lg:w-auto justify-end pt-4 lg:pt-0 border-t lg:border-t-0 border-slate-100">
              <Button
                variant="outline"
                size="sm"
                icon={<Sparkles className="w-3.5 h-3.5 text-signal-navy" />}
                onClick={() => {
                  setSelectedAppForReport(app);
                  setInternalNotesEdit(app.internalNotes || '');
                }}
              >
                Báo cáo AI & Ghi chú
              </Button>

              <select
                value={app.status}
                onChange={(e) => handleUpdateStatus(app.id, e.target.value as any)}
                className="bg-signal-offwhite text-xs font-semibold rounded-xl px-3 py-2 border border-slate-200 focus:outline-none focus:border-signal-navy"
              >
                <option value="submitted">Mới nộp</option>
                <option value="reviewing">Đang duyệt hồ sơ</option>
                <option value="shortlisted">Lọt phỏng vấn</option>
                <option value="interviewed">Đã phỏng vấn</option>
                <option value="offered">Mời nhận việc (Offer)</option>
                <option value="rejected">Từ chối hồ sơ</option>
              </select>
            </div>
          </div>
        ))}
      </div>

      {/* AI Report & Recruiter Review Modal */}
      <Modal
        isOpen={!!selectedAppForReport}
        onClose={() => setSelectedAppForReport(null)}
        title={`Đánh giá Ứng viên: ${selectedAppForReport?.candidateName}`}
        subtitle={`Vị trí: ${selectedAppForReport?.jobTitle}`}
        maxWidth="2xl"
      >
        {selectedAppForReport && (
          <div className="space-y-6">
            {selectedAppForReport.matchBreakdown ? (
              <SkillGapPanel
                breakdown={selectedAppForReport.matchBreakdown}
                jobTitle={selectedAppForReport.jobTitle}
                candidateName={selectedAppForReport.candidateName}
              />
            ) : (
              <div className="p-6 bg-slate-50 rounded-2xl text-center text-sm text-slate-500">
                Đang nạp báo cáo chi tiết...
              </div>
            )}

            {/* Internal Notes Box */}
            <div className="bg-signal-offwhite rounded-2xl p-5 border border-slate-200">
              <label className="block text-xs font-bold uppercase text-signal-navy mb-2">
                Ghi chú đánh giá nội bộ (Internal Notes)
              </label>
              <textarea
                rows={3}
                value={internalNotesEdit}
                onChange={(e) => setInternalNotesEdit(e.target.value)}
                placeholder="Thêm đánh giá về thái độ, lương kỳ vọng, câu hỏi phỏng vấn vòng 1..."
                className="w-full bg-white text-xs rounded-xl p-3 border border-slate-200 focus:outline-none focus:border-signal-navy mb-3"
              />
              <div className="flex justify-end">
                <Button variant="primary" size="sm" onClick={handleSaveNotes}>
                  Lưu ghi chú đánh giá
                </Button>
              </div>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

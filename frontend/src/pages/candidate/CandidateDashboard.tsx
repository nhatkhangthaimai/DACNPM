import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { apiService } from '../../services/api';
import { Job, CV, Application } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { StatCard } from '../../components/ui/StatCard';
import { JobCard } from '../../components/ui/JobCard';
import { MatchScoreRing } from '../../components/ui/MatchScoreRing';
import { Button } from '../../components/ui/Button';
import { SkillBadge } from '../../components/ui/SkillBadge';
import {
  Briefcase,
  FileText,
  Send,
  Sparkles,
  ArrowRight,
  TrendingUp,
  AlertCircle,
  CheckCircle2,
  UploadCloud
} from 'lucide-react';

export const CandidateDashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [cvs, setCvs] = useState<CV[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);

  useEffect(() => {
    apiService.getJobs().then(setJobs);
    apiService.getCandidateCVs('user-cand-1').then(setCvs);
    apiService.getApplications('candidate').then(setApplications);
  }, []);

  const primaryCV = cvs.find(c => c.isPrimary) || cvs[0];
  const topJob = jobs[0];

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <PageHeader
        title={`Chào mừng trở lại, ${user?.fullName || 'Ứng viên'}!`}
        subtitle="Hệ thống AI vừa quét thêm 3 việc làm mới có độ tương thích cao trên 85% với hồ sơ của bạn."
        badge="AI Active"
        actions={
          <Button
            variant="lime"
            icon={<Sparkles className="w-4 h-4 text-signal-navy" />}
            onClick={() => navigate('/candidate/matching')}
          >
            Trung tâm So khớp AI
          </Button>
        }
      />

      {/* Top 4 Stat Cards in Bento Style */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Việc làm AI gợi ý"
          value={jobs.length}
          subtitle="Dựa trên kỹ năng CV của bạn"
          icon={Briefcase}
          trend={{ value: '+4 tuần này', isPositive: true }}
          variant="white"
        />
        <StatCard
          title="Độ phù hợp cao nhất"
          value="94%"
          subtitle="Tại VNG Corporation"
          icon={Sparkles}
          variant="lime"
        />
        <StatCard
          title="Hồ sơ CV đã tải lên"
          value={cvs.length}
          subtitle={primaryCV ? `CV chính: ${primaryCV.fileName}` : 'Chưa có CV chính'}
          icon={FileText}
          variant="white"
        />
        <StatCard
          title="Đơn đã ứng tuyển"
          value={applications.length}
          subtitle="1 đơn đang được xem xét"
          icon={Send}
          variant="navy"
        />
      </div>

      {/* Bento Middle Section: High-Match Spotlight & Primary CV status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: AI Best Match Spotlight Card */}
        <div className="lg:col-span-2 bg-signal-navy text-white rounded-3xl p-6 sm:p-8 border border-signal-navy-border relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-80 h-80 bg-signal-lime/10 rounded-full blur-3xl pointer-events-none" />

          <div>
            <div className="flex items-center justify-between pb-4 border-b border-signal-navy-border mb-6">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-signal-lime animate-pulse" />
                <span className="text-xs font-mono font-bold text-signal-lime uppercase tracking-wider">
                  Top Recommended AI Match
                </span>
              </div>
              <span className="text-xs text-slate-400">Cập nhật hôm nay</span>
            </div>

            {topJob && (
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
                <div>
                  <span className="text-xs text-signal-mint font-semibold uppercase tracking-wider block mb-1">
                    {topJob.companyName}
                  </span>
                  <h3 className="font-heading text-2xl font-bold text-white mb-2">
                    {topJob.title}
                  </h3>
                  <p className="text-sm text-slate-300 max-w-lg mb-4 line-clamp-2">
                    {topJob.description}
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {topJob.requiredSkills.slice(0, 4).map((s, idx) => (
                      <span key={idx} className="px-2.5 py-1 rounded-full text-xs font-medium bg-signal-navy-light text-slate-200 border border-signal-navy-border">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="shrink-0 flex flex-col items-center justify-center p-4 rounded-2xl bg-signal-navy-light border border-signal-navy-border text-center">
                  <MatchScoreRing score={92} size={96} strokeWidth={8} />
                  <span className="text-xs font-bold text-signal-lime mt-2">Tuyệt vời</span>
                </div>
              </div>
            )}
          </div>

          <div className="flex items-center justify-between pt-6 border-t border-signal-navy-border mt-6">
            <span className="text-xs text-slate-400">
              Bạn đáp ứng 5/5 kỹ năng bắt buộc và phù hợp 90% về ngữ nghĩa kinh nghiệm.
            </span>
            <Button
              variant="lime"
              size="sm"
              onClick={() => navigate('/candidate/jobs')}
              icon={<ArrowRight className="w-3.5 h-3.5 text-signal-navy" />}
            >
              Xem chi tiết JD
            </Button>
          </div>
        </div>

        {/* Right 1 Col: Current CV Health & Gap Quick Advice */}
        <div className="bg-white rounded-3xl p-6 sm:p-7 border border-slate-200/80 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h4 className="font-heading font-bold text-lg text-signal-navy">
                Tình trạng Hồ sơ AI
              </h4>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-signal-mint/20 text-[#1b7a66]">
                Hoàn thiện 90%
              </span>
            </div>

            {primaryCV ? (
              <div className="space-y-4">
                <div className="p-3.5 rounded-2xl bg-signal-offwhite border border-slate-200/70">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-xl bg-white text-signal-navy border border-slate-200 shadow-sm">
                      <FileText className="w-5 h-5 text-signal-navy" />
                    </div>
                    <div className="overflow-hidden">
                      <span className="font-semibold text-xs text-signal-navy block truncate">
                        {primaryCV.fileName}
                      </span>
                      <span className="text-[11px] text-signal-slate">
                        Trích xuất thành công bởi Gemini AI
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <span className="text-xs font-semibold text-signal-slate uppercase tracking-wider block mb-2">
                    Kỹ năng nổi trội đã xác thực:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {primaryCV.parsedData?.hardSkills.slice(0, 5).map((sk, i) => (
                      <SkillBadge key={i} name={sk} variant="matched" size="sm" />
                    ))}
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-signal-lavender/15 border border-signal-lavender/30 text-xs text-signal-navy">
                  <div className="flex items-center gap-1.5 font-bold mb-1 text-[#5942be]">
                    <Sparkles className="w-3.5 h-3.5" />
                    Gợi ý nâng cao hồ sơ:
                  </div>
                  <p className="text-slate-600 leading-relaxed">
                    Bổ sung chứng chỉ Cloud (AWS / GCP) hoặc Docker để tăng thêm 8% điểm tương thích các vị trí Senior.
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-center py-6">
                <UploadCloud className="w-10 h-10 text-slate-300 mx-auto mb-2" />
                <p className="text-xs text-signal-slate mb-4">Bạn chưa tải lên CV nào.</p>
                <Button variant="lime" size="sm" onClick={() => navigate('/candidate/cvs')}>
                  Tải CV ngay
                </Button>
              </div>
            )}
          </div>

          <div className="pt-4 border-t border-slate-100 mt-4">
            <button
              onClick={() => navigate('/candidate/cvs')}
              className="w-full text-center text-xs font-semibold text-signal-navy hover:text-signal-navy-light py-1"
            >
              Quản lý danh sách CV →
            </button>
          </div>
        </div>
      </div>

      {/* Suggested Jobs Carousel / Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-heading text-xl font-bold text-signal-navy">
            Việc làm gợi ý riêng cho bạn
          </h3>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/candidate/jobs')}
          >
            Xem tất cả ({jobs.length})
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {jobs.slice(0, 3).map((job) => (
            <JobCard
              key={job.id}
              job={job}
              matchScore={job.id === 'job-1' ? 92 : job.id === 'job-2' ? 86 : 80}
              onApply={() => navigate('/candidate/jobs')}
              onViewDetails={() => navigate('/candidate/jobs')}
              onCheckMatch={() => navigate('/candidate/matching')}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

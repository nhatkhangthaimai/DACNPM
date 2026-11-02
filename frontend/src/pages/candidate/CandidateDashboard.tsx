import React, { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { apiService } from '../../services/api';
import { Job, CV, Application, MatchScoreBreakdown } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { StatCard } from '../../components/ui/StatCard';
import { JobCard } from '../../components/ui/JobCard';
import { MatchScoreRing } from '../../components/ui/MatchScoreRing';
import { Button } from '../../components/ui/Button';
import { SkillBadge } from '../../components/ui/SkillBadge';
import { Modal } from '../../components/ui/Modal';
import { SkillGapPanel } from '../../components/ui/SkillGapPanel';
import {
  Briefcase,
  FileText,
  Send,
  Sparkles,
  ArrowRight,
  TrendingUp,
  AlertCircle,
  CheckCircle2,
  UploadCloud,
  ChevronDown,
  Layers,
  XCircle,
  CheckCircle
} from 'lucide-react';

export const CandidateDashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [cvs, setCvs] = useState<CV[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Controlled Selection States
  const [selectedCvId, setSelectedCvId] = useState<string>('');
  const [selectedJobId, setSelectedJobId] = useState<string>('auto');

  // Modal for Skill Gap Analysis
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);

  useEffect(() => {
    setIsLoading(true);
    Promise.all([
      apiService.getJobs(),
      apiService.getCandidateCVs(user?.id || 'user-cand-1'),
      apiService.getApplications('candidate')
    ]).then(([jobsData, cvsData, appsData]) => {
      setJobs(jobsData);
      setCvs(cvsData);
      setApplications(appsData);

      const primary = cvsData.find(c => c.isPrimary) || cvsData[0];
      if (primary) {
        setSelectedCvId(primary.id);
      }
      setIsLoading(false);
    }).catch(() => {
      setIsLoading(false);
    });
  }, [user?.id]);

  // Active CV based on candidate's selection
  const selectedCV = useMemo(() => {
    if (!cvs.length) return null;
    return cvs.find(c => c.id === selectedCvId) || cvs.find(c => c.isPrimary) || cvs[0];
  }, [cvs, selectedCvId]);

  // Compute real match scores for ALL jobs against the chosen CV
  const jobScores = useMemo(() => {
    if (!selectedCV || jobs.length === 0) {
      return jobs.map(j => ({ job: j, breakdown: null as MatchScoreBreakdown | null, score: 0 }));
    }
    return jobs.map(job => {
      try {
        const breakdown = apiService.calculateMatchScore(selectedCV, job);
        return { job, breakdown, score: breakdown.overallScore };
      } catch {
        return { job, breakdown: null as MatchScoreBreakdown | null, score: 0 };
      }
    }).sort((a, b) => b.score - a.score);
  }, [selectedCV, jobs]);

  // Highest match job across the entire database for this CV
  const topRecommended = jobScores[0] || null;

  // Active job in the Spotlight Card: Auto (highest match) OR user's manual selection
  const activeJob = useMemo(() => {
    if (selectedJobId === 'auto') {
      return topRecommended?.job || jobs[0] || null;
    }
    return jobs.find(j => j.id === selectedJobId) || topRecommended?.job || jobs[0] || null;
  }, [selectedJobId, topRecommended, jobs]);

  // Real-time match breakdown between currently selected CV and active Job
  const activeBreakdown = useMemo(() => {
    if (!selectedCV || !activeJob) return null;
    return apiService.calculateMatchScore(selectedCV, activeJob);
  }, [selectedCV, activeJob]);

  const activeScore = activeBreakdown ? activeBreakdown.overallScore : 0;

  // Status text & style based on score
  const getScoreVerdict = (score: number) => {
    if (score >= 80) return { label: 'Rất phù hợp (Tuyệt vời)', color: 'text-signal-lime', bg: 'bg-signal-lime/20', border: 'border-signal-lime/30' };
    if (score >= 50) return { label: 'Phù hợp một phần', color: 'text-amber-300', bg: 'bg-amber-400/20', border: 'border-amber-400/30' };
    return { label: 'Độ tương thích thấp', color: 'text-rose-400', bg: 'bg-rose-500/20', border: 'border-rose-500/30' };
  };

  const verdict = getScoreVerdict(activeScore);

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <PageHeader
        title={`Chào mừng trở lại, ${user?.fullName || 'Nguyễn Văn An'}!`}
        subtitle={
          topRecommended && topRecommended.score >= 70
            ? `Hệ thống AI vừa quét thấy vị trí ${topRecommended.job.title} tại ${topRecommended.job.companyName} có độ tương thích cao (${topRecommended.score}%) với hồ sơ của bạn.`
            : "Hệ thống AI tự động đối soát kỹ năng và liên tục xếp hạng việc làm tương thích với hồ sơ của bạn."
        }
        badge="AI Active"
        actions={
          <div className="flex items-center gap-2.5">
            {cvs.length > 0 && (
              <div className="flex items-center gap-2 bg-white px-3 py-1.5 rounded-2xl border border-slate-200 shadow-sm text-xs">
                <span className="font-semibold text-signal-slate uppercase text-[10px]">CV Đang chọn:</span>
                <select
                  value={selectedCvId}
                  onChange={(e) => setSelectedCvId(e.target.value)}
                  className="bg-transparent font-bold text-signal-navy focus:outline-none cursor-pointer max-w-[160px] truncate"
                >
                  {cvs.map(c => (
                    <option key={c.id} value={c.id}>
                      {c.fileName} {c.isPrimary ? '★ (Chính)' : ''}
                    </option>
                  ))}
                </select>
              </div>
            )}
            <Button
              variant="lime"
              icon={<Sparkles className="w-4 h-4 text-signal-navy" />}
              onClick={() => navigate('/candidate/matching')}
            >
              Trung tâm So khớp AI
            </Button>
          </div>
        }
      />

      {/* Top 4 Stat Cards in Bento Style */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Việc làm AI gợi ý"
          value={jobs.length}
          subtitle={`Dựa trên: ${selectedCV ? selectedCV.fileName : 'CV của bạn'}`}
          icon={Briefcase}
          trend={{ value: '+4 việc mới', isPositive: true }}
          variant="white"
        />
        <StatCard
          title="Độ phù hợp cao nhất"
          value={topRecommended ? `${topRecommended.score}%` : '0%'}
          subtitle={topRecommended ? `Tại ${topRecommended.job.companyName}` : 'Chưa có việc làm'}
          icon={Sparkles}
          variant="lime"
        />
        <StatCard
          title="Hồ sơ CV đã tải lên"
          value={cvs.length}
          subtitle={selectedCV ? `Đang chọn: ${selectedCV.fileName}` : 'Chưa có CV'}
          icon={FileText}
          variant="white"
        />
        <StatCard
          title="Đơn đã ứng tuyển"
          value={applications.length}
          subtitle={applications.length > 0 ? `${applications.length} đơn đang xem xét` : 'Chưa nộp đơn nào'}
          icon={Send}
          variant="navy"
        />
      </div>

      {/* Bento Middle Section: High-Match Spotlight & Primary CV status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Dynamic AI Match Spotlight Card */}
        <div className="lg:col-span-2 bg-signal-navy text-white rounded-3xl p-6 sm:p-8 border border-signal-navy-border relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 w-80 h-80 bg-signal-lime/10 rounded-full blur-3xl pointer-events-none" />

          <div>
            {/* Top Bar with Selectors */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-signal-navy-border mb-6 gap-3">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-signal-lime animate-pulse" />
                <span className="text-xs font-mono font-bold text-signal-lime uppercase tracking-wider">
                  {selectedJobId === 'auto' ? 'Top Recommended AI Match' : 'So khớp trực tiếp theo JD'}
                </span>
              </div>

              {/* JD Selector dropdown */}
              <div className="flex items-center gap-2 text-xs">
                <span className="text-slate-400 font-medium">Vị trí so khớp:</span>
                <select
                  value={selectedJobId}
                  onChange={(e) => setSelectedJobId(e.target.value)}
                  className="bg-signal-navy-light text-white text-xs font-semibold rounded-xl px-3 py-1.5 border border-signal-navy-border focus:outline-none focus:border-signal-lime cursor-pointer max-w-[280px] truncate"
                >
                  {topRecommended && (
                    <option value="auto">
                      ★ [AI Đề xuất cao nhất] {topRecommended.job.title} ({topRecommended.score}% Match)
                    </option>
                  )}
                  {jobs.map((j) => (
                    <option key={j.id} value={j.id}>
                      {j.title} · {j.companyName}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Active Job Information & Real-time AI Match Ring */}
            {activeJob ? (
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs text-signal-mint font-semibold uppercase tracking-wider">
                      {activeJob.companyName}
                    </span>
                    <span className="text-slate-500 text-xs">·</span>
                    <span className="text-xs text-slate-300">{activeJob.location}</span>
                  </div>

                  <h3 className="font-heading text-2xl font-bold text-white mb-2">
                    {activeJob.title}
                  </h3>

                  <p className="text-sm text-slate-300 max-w-lg mb-4 line-clamp-2 leading-relaxed">
                    {activeJob.description}
                  </p>

                  {/* Skills overview: Matched vs Missing */}
                  <div className="space-y-2">
                    <div className="flex flex-wrap items-center gap-1.5">
                      <span className="text-[11px] font-bold uppercase text-slate-400 mr-1">Yêu cầu:</span>
                      {(activeJob.requiredSkills || []).slice(0, 5).map((s, idx) => {
                        const isMatched = activeBreakdown?.matchedSkills.some(
                          ms => ms.toLowerCase() === s.toLowerCase()
                        );
                        return (
                          <span
                            key={idx}
                            className={`px-2.5 py-0.5 rounded-full text-xs font-medium border flex items-center gap-1 ${
                              isMatched
                                ? 'bg-emerald-950/60 text-emerald-300 border-emerald-500/40'
                                : 'bg-rose-950/60 text-rose-300 border-rose-500/40'
                            }`}
                          >
                            {isMatched ? '✓' : '✕'} {s}
                          </span>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Match Score Ring (Calculated dynamically) */}
                <div className="shrink-0 flex flex-col items-center justify-center p-5 rounded-2xl bg-signal-navy-light border border-signal-navy-border text-center min-w-[130px]">
                  <MatchScoreRing score={activeScore} size={96} strokeWidth={8} />
                  <span className={`text-xs font-bold mt-2 ${verdict.color}`}>
                    {verdict.label}
                  </span>
                </div>
              </div>
            ) : (
              <div className="py-8 text-center text-slate-400">
                Đang tải dữ liệu việc làm...
              </div>
            )}
          </div>

          {/* Footer diagnostic message & CTA */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between pt-6 border-t border-signal-navy-border mt-6 gap-3">
            <div className="text-xs text-slate-300 max-w-xl">
              {activeBreakdown ? (
                <span>
                  {activeScore >= 50 ? (
                    <span className="text-emerald-300 font-semibold mr-1">✓ Phù hợp:</span>
                  ) : (
                    <span className="text-rose-300 font-semibold mr-1">✕ Chú ý:</span>
                  )}
                  {activeBreakdown.aiExplanation}
                </span>
              ) : (
                <span className="text-slate-400">Đang tính toán tương thích AI...</span>
              )}
            </div>

            <div className="flex items-center gap-2.5 shrink-0">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsDetailModalOpen(true)}
              >
                Chi tiết so khớp
              </Button>
              <Button
                variant="lime"
                size="sm"
                onClick={() => navigate('/candidate/jobs')}
                icon={<ArrowRight className="w-3.5 h-3.5 text-signal-navy" />}
              >
                Khám phá JD
              </Button>
            </div>
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
                {selectedCV?.parsedData ? 'Đã trích xuất' : 'Chưa hoàn tất'}
              </span>
            </div>

            {selectedCV ? (
              <div className="space-y-4">
                <div className="p-3.5 rounded-2xl bg-signal-offwhite border border-slate-200/70">
                  <div className="flex items-center gap-3">
                    <div className="p-2.5 rounded-xl bg-white text-signal-navy border border-slate-200 shadow-sm">
                      <FileText className="w-5 h-5 text-signal-navy" />
                    </div>
                    <div className="overflow-hidden">
                      <span className="font-semibold text-xs text-signal-navy block truncate" title={selectedCV.fileName}>
                        {selectedCV.fileName}
                      </span>
                      <span className="text-[11px] text-signal-slate">
                        Ứng viên: {selectedCV.parsedData?.fullName || 'Nguyễn Văn An'}
                      </span>
                    </div>
                  </div>
                </div>

                <div>
                  <span className="text-xs font-semibold text-signal-slate uppercase tracking-wider block mb-2">
                    Kỹ năng nổi trội đã xác thực:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {(selectedCV.parsedData?.hardSkills || []).slice(0, 6).map((sk, i) => (
                      <SkillBadge key={i} name={sk} variant="matched" size="sm" />
                    ))}
                    {(!selectedCV.parsedData?.hardSkills || selectedCV.parsedData.hardSkills.length === 0) && (
                      <span className="text-xs text-slate-400 italic">Chưa phát hiện kỹ năng</span>
                    )}
                  </div>
                </div>

                <div className="p-3.5 rounded-xl bg-signal-lavender/15 border border-signal-lavender/30 text-xs text-signal-navy">
                  <div className="flex items-center gap-1.5 font-bold mb-1 text-[#5942be]">
                    <Sparkles className="w-3.5 h-3.5" />
                    Gợi ý nâng cao hồ sơ:
                  </div>
                  <p className="text-slate-600 leading-relaxed text-xs">
                    {activeBreakdown?.recommendations?.[0] || 'Bổ sung thêm chứng chỉ chuyên sâu về công nghệ đám mây để nâng cao tính cạnh tranh.'}
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-center py-6">
                <UploadCloud className="w-10 h-10 text-slate-300 mx-auto mb-2" />
                <p className="text-xs text-signal-slate mb-4">Bạn chưa có CV nào trong hồ sơ.</p>
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
          <div>
            <h3 className="font-heading text-xl font-bold text-signal-navy">
              Việc làm AI gợi ý riêng cho bạn
            </h3>
            <p className="text-xs text-signal-slate mt-0.5">
              Được tự động sắp xếp theo điểm số tương thích thực tế với {selectedCV ? selectedCV.fileName : 'CV của bạn'}
            </p>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/candidate/jobs')}
          >
            Xem tất cả ({jobs.length})
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {jobScores.slice(0, 3).map(({ job, score }) => (
            <JobCard
              key={job.id}
              job={job}
              matchScore={score}
              onApply={() => navigate('/candidate/jobs')}
              onViewDetails={() => {
                setSelectedJobId(job.id);
                setIsDetailModalOpen(true);
              }}
              onCheckMatch={() => {
                setSelectedJobId(job.id);
              }}
            />
          ))}
        </div>
      </div>

      {/* Detail Skill Gap Modal */}
      <Modal
        isOpen={isDetailModalOpen}
        onClose={() => setIsDetailModalOpen(false)}
        title="Chi tiết So khớp & Phân tích Khoảng cách Kỹ năng"
        subtitle={`Vị trí: ${activeJob?.title} · ${activeJob?.companyName}`}
        maxWidth="2xl"
      >
        {activeBreakdown && activeJob && (
          <div className="space-y-6">
            <SkillGapPanel
              breakdown={activeBreakdown}
              jobTitle={activeJob.title}
              candidateName={selectedCV?.parsedData?.fullName || user?.fullName}
            />
            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
              <Button variant="outline" onClick={() => setIsDetailModalOpen(false)}>
                Đóng
              </Button>
              <Button
                variant="lime"
                onClick={() => {
                  setIsDetailModalOpen(false);
                  navigate('/candidate/jobs');
                }}
              >
                Xem chi tiết tin tuyển dụng
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

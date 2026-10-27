import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import { Job, CV, MatchScoreBreakdown } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { SkillGapPanel } from '../../components/ui/SkillGapPanel';
import { Button } from '../../components/ui/Button';
import { Sparkles, ArrowRight, CheckCircle2, Cpu, FileText, Briefcase } from 'lucide-react';

export const JobMatchingCenter: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [cvs, setCvs] = useState<CV[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<string>('');
  const [selectedCvId, setSelectedCvId] = useState<string>('');
  const [isMatching, setIsMatching] = useState(false);
  const [matchResult, setMatchResult] = useState<MatchScoreBreakdown | null>(null);

  useEffect(() => {
    Promise.all([
      apiService.getJobs(),
      apiService.getCandidateCVs('user-cand-1'),
    ]).then(([jobsData, cvsData]) => {
      setJobs(jobsData);
      setCvs(cvsData);
      if (jobsData.length > 0) setSelectedJobId(jobsData[0].id);
      if (cvsData.length > 0) setSelectedCvId(cvsData[0].id);

      // Auto compute initial match
      if (jobsData.length > 0 && cvsData.length > 0) {
        const initialResult = apiService.calculateMatchScore(cvsData[0], jobsData[0]);
        setMatchResult(initialResult);
      }
    });
  }, []);

  const handleRunMatch = () => {
    const job = jobs.find(j => j.id === selectedJobId);
    const cv = cvs.find(c => c.id === selectedCvId);

    if (!job || !cv) return;

    setIsMatching(true);
    setTimeout(() => {
      const result = apiService.calculateMatchScore(cv, job);
      setMatchResult(result);
      setIsMatching(false);
    }, 600);
  };

  const currentJob = jobs.find(j => j.id === selectedJobId);
  const currentCv = cvs.find(c => c.id === selectedCvId);

  return (
    <div className="space-y-8">
      <PageHeader
        title="Trung tâm So khớp AI & Phân tích Khoảng cách Kỹ năng"
        subtitle="Chọn bất kỳ CV nào trong hồ sơ của bạn và một tin tuyển dụng mục tiêu để chạy mô hình Hybrid Matching đa tiêu chí."
        badge="Gemini Hybrid Engine"
      />

      {/* Selector Control Panel */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/80 shadow-sm space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* CV Selector */}
          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-2 flex items-center gap-1.5">
              <FileText className="w-4 h-4 text-signal-navy" />
              Chọn CV của bạn để so khớp
            </label>
            {cvs.length > 0 ? (
              <select
                value={selectedCvId}
                onChange={(e) => setSelectedCvId(e.target.value)}
                className="w-full bg-signal-offwhite text-sm font-semibold rounded-2xl px-4 py-3 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
              >
                {cvs.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.fileName} {c.isPrimary ? '(CV Chính)' : ''}
                  </option>
                ))}
              </select>
            ) : (
              <p className="text-xs text-rose-600">Chưa có CV nào được tải lên.</p>
            )}
          </div>

          {/* Job Selector */}
          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-2 flex items-center gap-1.5">
              <Briefcase className="w-4 h-4 text-signal-navy" />
              Chọn Vị trí tuyển dụng mục tiêu (Target JD)
            </label>
            <select
              value={selectedJobId}
              onChange={(e) => setSelectedJobId(e.target.value)}
              className="w-full bg-signal-offwhite text-sm font-semibold rounded-2xl px-4 py-3 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
            >
              {jobs.map((j) => (
                <option key={j.id} value={j.id}>
                  {j.companyName} – {j.title}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center justify-between pt-4 border-t border-slate-100">
          <div className="flex items-center gap-2 text-xs text-signal-slate">
            <Cpu className="w-4 h-4 text-signal-lime-dark" />
            <span>Trọng số: Hard Skills (50%) · Semantic Cosine (30%) · Kinh nghiệm (20%)</span>
          </div>

          <Button
            variant="lime"
            size="md"
            isLoading={isMatching}
            onClick={handleRunMatch}
            icon={<Sparkles className="w-4 h-4 text-signal-navy" />}
          >
            Chạy Phân tích So khớp AI
          </Button>
        </div>
      </div>

      {/* Match Result Output */}
      {matchResult && (
        <SkillGapPanel
          breakdown={matchResult}
          jobTitle={currentJob?.title}
          candidateName={currentCv?.parsedData?.fullName || 'Nguyễn Văn An'}
        />
      )}
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import { Job, CV, MatchScoreBreakdown } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { SkillGapPanel } from '../../components/ui/SkillGapPanel';
import { Button } from '../../components/ui/Button';
import { Sparkles, AlertTriangle, Cpu, FileText, Briefcase, RefreshCw } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const JobMatchingCenter: React.FC = () => {
  const { user } = useAuth();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [cvs, setCvs] = useState<CV[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<string>('');
  const [selectedCvId, setSelectedCvId] = useState<string>('');
  const [isMatching, setIsMatching] = useState(false);
  const [matchResult, setMatchResult] = useState<MatchScoreBreakdown | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      apiService.getJobs(),
      apiService.getCandidateCVs(user?.id || 'user-cand-1'),
    ]).then(([jobsData, cvsData]) => {
      setJobs(jobsData);
      setCvs(cvsData);
      if (jobsData.length > 0) setSelectedJobId(jobsData[0].id);
      if (cvsData.length > 0) setSelectedCvId(cvsData[0].id);

      // Only compute initial match if the first CV is verified completed
      if (jobsData.length > 0 && cvsData.length > 0) {
        const firstCv = cvsData[0];
        if (firstCv.extractionStatus === 'completed' && firstCv.parsedData) {
          const initialResult = apiService.calculateMatchScore(firstCv, jobsData[0]);
          setMatchResult(initialResult);
        } else {
          setMatchResult(null);
        }
      }
    });
  }, [user?.id]);

  const currentJob = jobs.find(j => j.id === selectedJobId);
  const currentCv = cvs.find(c => c.id === selectedCvId);

  const isCvValid = currentCv?.extractionStatus === 'completed' && Boolean(currentCv?.parsedData);
  const isCvFailed = currentCv?.extractionStatus === 'failed' || currentCv?.extractionStatus === 'extraction_failed';
  const isCvProcessing = currentCv?.extractionStatus === 'processing' || currentCv?.extractionStatus === 'pending';

  const handleRunMatch = async () => {
    if (!currentJob || !currentCv) return;

    if (!isCvValid) {
      setErrorMessage("Không thể tính điểm do dữ liệu CV chưa được trích xuất chính xác hoặc bị lỗi.");
      setMatchResult(null);
      return;
    }

    setIsMatching(true);
    setErrorMessage(null);

    try {
      // Try backend endpoint first
      const result = await apiService.calculateMatchViaBackend(currentCv.id, currentJob.id);
      setMatchResult(result);
    } catch (err: any) {
      console.warn("Backend match call returned error or offline, fallback to honest local calculation:", err);
      if (err.response?.data?.detail?.status === 'blocked') {
        setErrorMessage(err.response.data.detail.message || "Quá trình so khớp bị chặn do dữ liệu CV không hợp lệ.");
        setMatchResult(null);
      } else {
        // Honest local calculation
        const localResult = apiService.calculateMatchScore(currentCv, currentJob);
        setMatchResult(localResult);
      }
    } finally {
      setIsMatching(false);
    }
  };

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
                onChange={(e) => {
                  setSelectedCvId(e.target.value);
                  setErrorMessage(null);
                  setMatchResult(null);
                }}
                className="w-full bg-signal-offwhite text-sm font-semibold rounded-2xl px-4 py-3 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
              >
                {cvs.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.fileName} {c.isPrimary ? '(CV Chính)' : ''} {c.extractionStatus !== 'completed' ? `[${c.extractionStatus}]` : ''}
                  </option>
                ))}
              </select>
            ) : (
              <p className="text-xs text-rose-600">Chưa có CV nào được tải lên trong hồ sơ.</p>
            )}

            {/* CV Validity Indicator */}
            {currentCv && (
              <div className="mt-2.5">
                {isCvValid ? (
                  <span className="text-xs text-emerald-700 font-semibold flex items-center gap-1">
                    ✓ CV đã được phân tích thành công ({currentCv.parsedData?.hardSkills.length || 0} kỹ năng)
                  </span>
                ) : isCvFailed ? (
                  <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-700 flex items-start gap-2">
                    <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                    <div>
                      <p className="font-bold">CV chưa được trích xuất chính xác hoặc bị lỗi định dạng.</p>
                      <p className="mt-0.5 text-rose-600">Hệ thống chặn tính điểm để tránh tạo ra kết quả giả mạo. Vui lòng tải lại CV hợp lệ.</p>
                    </div>
                  </div>
                ) : isCvProcessing ? (
                  <span className="text-xs text-amber-700 font-semibold flex items-center gap-1">
                    ⏳ CV đang được xử lý bởi AI, vui lòng đợi hoàn tất...
                  </span>
                ) : null}
              </div>
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
              onChange={(e) => {
                setSelectedJobId(e.target.value);
                setErrorMessage(null);
                setMatchResult(null);
              }}
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

        {/* Global Error Banner */}
        {errorMessage && (
          <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-sm text-rose-800 flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-4 border-t border-slate-100">
          <div className="flex items-center gap-2 text-xs text-signal-slate">
            <Cpu className="w-4 h-4 text-signal-lime-dark" />
            <span>Trọng số chuẩn: Hard Skills (50%) · Semantic Cosine (30%) · Kinh nghiệm (20%)</span>
          </div>

          <Button
            variant="lime"
            size="md"
            isLoading={isMatching}
            disabled={!isCvValid || isMatching}
            onClick={handleRunMatch}
            icon={<Sparkles className="w-4 h-4 text-signal-navy" />}
          >
            {isMatching ? 'Đang so khớp đa tiêu chí...' : 'Chạy Phân tích So khớp AI'}
          </Button>
        </div>
      </div>

      {/* Match Result Output - Only render when valid result exists */}
      {matchResult && isCvValid && (
        <SkillGapPanel
          breakdown={matchResult}
          jobTitle={currentJob?.title}
          candidateName={currentCv?.parsedData?.fullName || user?.fullName || 'Ứng viên'}
        />
      )}
    </div>
  );
};

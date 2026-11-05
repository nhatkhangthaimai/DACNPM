import React, { useState, useEffect, useMemo, useRef } from 'react';
import { apiService } from '../../services/api';
import { Job, CV, MatchScoreBreakdown } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { JobCard } from '../../components/ui/JobCard';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { SkillBadge, StatusBadge } from '../../components/ui/SkillBadge';
import { MatchScoreRing } from '../../components/ui/MatchScoreRing';
import { useAuth } from '../../context/AuthContext';
import { useJobs, useCandidateCVs, useInvalidateQueries } from '../../hooks/useQueries';
import {
  Search,
  MapPin,
  Briefcase,
  DollarSign,
  GraduationCap,
  Layers,
  ArrowUpDown,
  Filter,
  CheckCircle2,
  Sparkles,
  Building2,
  X,
  FileText,
  AlertCircle
} from 'lucide-react';

export const JobDiscovery: React.FC = () => {
  const { user } = useAuth();
  const { invalidateJobs } = useInvalidateQueries();

  // Filter States
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [industryFilter, setIndustryFilter] = useState('all');
  const [locationFilter, setLocationFilter] = useState('all');
  const [jobTypeFilter, setJobTypeFilter] = useState('all');
  const [experienceFilter, setExperienceFilter] = useState('all');
  const [salaryFilter, setSalaryFilter] = useState('all');
  const [sortBy, setSortBy] = useState('newest');

  // Modal States
  const [selectedJobForDetail, setSelectedJobForDetail] = useState<Job | null>(null);
  const [selectedJobForApply, setSelectedJobForApply] = useState<Job | null>(null);
  const [selectedCvId, setSelectedCvId] = useState<string>('');
  const [coverLetter, setCoverLetter] = useState<string>('');
  const [isApplying, setIsApplying] = useState(false);
  const [applySuccess, setApplySuccess] = useState(false);
  const [isSeeding, setIsSeeding] = useState(false);

  const hasAutoSeeded = useRef(false);

  // Debounce search input (350ms) to avoid request storms
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(searchQuery);
    }, 350);
    return () => clearTimeout(handler);
  }, [searchQuery]);

  // Compute structured filters for useJobs query
  const queryFilters = useMemo(() => {
    let minSalary: number | undefined;
    let maxSalary: number | undefined;
    if (salaryFilter === '<15') {
      maxSalary = 15000000;
    } else if (salaryFilter === '15-30') {
      minSalary = 15000000;
      maxSalary = 30000000;
    } else if (salaryFilter === '30-50') {
      minSalary = 30000000;
      maxSalary = 50000000;
    } else if (salaryFilter === '>50') {
      minSalary = 50000000;
    }

    return {
      search: debouncedSearch.trim() || undefined,
      location: locationFilter !== 'all' ? locationFilter : undefined,
      jobType: jobTypeFilter !== 'all' ? jobTypeFilter : undefined,
      industry: industryFilter !== 'all' ? industryFilter : undefined,
      experienceLevel: experienceFilter !== 'all' ? experienceFilter : undefined,
      minSalary,
      maxSalary,
      sortBy: sortBy === 'match' ? 'newest' : sortBy,
      limit: 100,
    };
  }, [debouncedSearch, locationFilter, jobTypeFilter, industryFilter, experienceFilter, salaryFilter, sortBy]);

  // Use TanStack Query hooks (cached 3 mins, AbortController support)
  const { data: jobs = [], isLoading: isJobsLoading } = useJobs(queryFilters);
  const { data: cvs = [] } = useCandidateCVs(user?.id);

  // Sync selected CV for apply modal
  useEffect(() => {
    if (cvs.length > 0 && !selectedCvId) {
      const primary = cvs.find(c => c.isPrimary) || cvs[0];
      setSelectedCvId(primary.id);
    }
  }, [cvs, selectedCvId]);

  // Auto-seed check if DB is empty on first visit
  useEffect(() => {
    if (!isJobsLoading && jobs.length <= 2 && !debouncedSearch && industryFilter === 'all' && !hasAutoSeeded.current) {
      hasAutoSeeded.current = true;
      apiService.seedMultiIndustryJobs()
        .then(() => invalidateJobs())
        .catch(err => console.warn('Auto-seed check notice:', err));
    }
  }, [jobs.length, isJobsLoading, debouncedSearch, industryFilter, invalidateJobs]);

  const primaryCv = useMemo(() => {
    return cvs.find(c => c.isPrimary) || cvs[0] || null;
  }, [cvs]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setDebouncedSearch(searchQuery);
  };

  const handleResetFilters = () => {
    setSearchQuery('');
    setDebouncedSearch('');
    setIndustryFilter('all');
    setLocationFilter('all');
    setJobTypeFilter('all');
    setExperienceFilter('all');
    setSalaryFilter('all');
    setSortBy('newest');
  };

  // Pre-calculate match scores for all loaded jobs against candidate's primary CV
  const jobMatchMap = useMemo(() => {
    const map = new Map<string, MatchScoreBreakdown>();
    if (!primaryCv) return map;
    for (const job of jobs) {
      try {
        const breakdown = apiService.calculateMatchScore(primaryCv, job);
        map.set(job.id, breakdown);
      } catch {
        // silent catch
      }
    }
    return map;
  }, [jobs, primaryCv]);

  // Client-side sorting & secondary filtering if needed
  const displayJobs = useMemo(() => {
    let list = [...jobs];

    if (sortBy === 'match' && primaryCv) {
      list.sort((a, b) => {
        const scoreA = jobMatchMap.get(a.id)?.overallScore || 0;
        const scoreB = jobMatchMap.get(b.id)?.overallScore || 0;
        return scoreB - scoreA;
      });
    } else if (sortBy === 'salary_desc') {
      list.sort((a, b) => (b.salaryMax || 0) - (a.salaryMax || 0));
    } else if (sortBy === 'salary_asc') {
      list.sort((a, b) => (a.salaryMin || 0) - (b.salaryMin || 0));
    }

    return list;
  }, [jobs, sortBy, primaryCv, jobMatchMap]);

  const handleApplySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedJobForApply || !selectedCvId) return;

    setIsApplying(true);
    await apiService.applyToJob(selectedJobForApply.id, selectedCvId, coverLetter);
    setIsApplying(false);
    setApplySuccess(true);
    setTimeout(() => {
      setApplySuccess(false);
      setSelectedJobForApply(null);
      setCoverLetter('');
    }, 1800);
  };

  const selectedJobBreakdown = selectedJobForDetail
    ? jobMatchMap.get(selectedJobForDetail.id)
    : null;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Khám phá Cơ hội Việc làm Đa ngành"
        subtitle="Hệ thống tổng hợp hơn 50 vị trí thuộc 14 lĩnh vực trọng điểm, tự động phân tích và xếp hạng độ tương thích AI theo hồ sơ của bạn."
        badge={`${displayJobs.length} Việc làm đang mở`}
      />

      {/* Primary CV Notification Banner */}
      {primaryCv && (
        <div className="bg-gradient-to-r from-signal-navy/5 via-signal-lime/10 to-signal-navy/5 rounded-2xl p-4 border border-signal-lime/30 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-signal-navy text-signal-lime flex items-center justify-center shrink-0">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-semibold text-signal-navy">
                Đang ghép nối tự động với CV chính: <span className="font-bold text-signal-navy">{primaryCv.fileName}</span>
              </p>
              <p className="text-xs text-signal-slate">
                Ứng viên: {primaryCv.parsedData?.fullName || 'Ứng viên'} · {primaryCv.parsedData?.hardSkills?.slice(0, 4).join(', ') || 'Đã sẵn sàng phân tích'}
              </p>
            </div>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setSortBy('match');
            }}
          >
            Sắp xếp theo độ phù hợp AI
          </Button>
        </div>
      )}

      {/* Advanced Search & Multi-Filter Bar */}
      <form onSubmit={handleSearchSubmit} className="bg-white p-5 rounded-3xl border border-slate-200/80 shadow-sm space-y-4">
        {/* Row 1: Search query & Search button */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-5 h-5 text-slate-400 absolute left-4 top-3.5" />
            <input
              type="text"
              placeholder="Tìm kiếm theo chức danh (Frontend, AI Engineer, Kế toán...), từ khóa kỹ năng..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-signal-offwhite text-sm rounded-2xl border border-slate-200 focus:outline-none focus:border-signal-navy focus:bg-white transition-colors"
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="absolute right-4 top-3.5 text-slate-400 hover:text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          <Button type="submit" variant="primary" size="md" isLoading={isJobsLoading}>
            Tìm việc làm
          </Button>
        </div>

        {/* Row 2: Dropdown Filters */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2.5 pt-2 border-t border-slate-100">
          {/* Industry Filter */}
          <div>
            <label className="block text-[11px] font-bold uppercase text-signal-slate mb-1">Ngành nghề</label>
            <select
              value={industryFilter}
              onChange={(e) => {
                setIndustryFilter(e.target.value);
              }}
              className="w-full bg-signal-offwhite text-xs font-medium rounded-xl px-3 py-2 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
            >
              <option value="all">Tất cả ngành</option>
              <option value="Công nghệ">Công nghệ phần mềm</option>
              <option value="AI">AI & Phân tích dữ liệu</option>
              <option value="Cloud">Cloud & DevOps</option>
              <option value="Tài chính">Tài chính - Fintech</option>
              <option value="Marketing">Marketing & Media</option>
              <option value="Thiết kế">Thiết kế đồ họa</option>
              <option value="Nhân sự">Nhân sự (HR)</option>
              <option value="Bán lẻ">Bán lẻ & Thương mại</option>
              <option value="Logistics">Logistics & Chuỗi cung ứng</option>
              <option value="Du lịch">Du lịch & Khách sạn</option>
              <option value="Giáo dục">Giáo dục & Đào tạo</option>
              <option value="Xây dựng">Xây dựng & Kỹ thuật</option>
              <option value="Sản xuất">Sản xuất công nghiệp</option>
              <option value="Chăm sóc sức khỏe">Y tế & Sức khỏe</option>
              <option value="Nông nghiệp">Nông nghiệp công nghệ</option>
            </select>
          </div>

          {/* Location Filter */}
          <div>
            <label className="block text-[11px] font-bold uppercase text-signal-slate mb-1">Địa điểm</label>
            <select
              value={locationFilter}
              onChange={(e) => setLocationFilter(e.target.value)}
              className="w-full bg-signal-offwhite text-xs font-medium rounded-xl px-3 py-2 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
            >
              <option value="all">Tất cả địa điểm</option>
              <option value="Đà Nẵng">Đà Nẵng</option>
              <option value="Hà Nội">Hà Nội</option>
              <option value="TP.HCM">TP. Hồ Chí Minh</option>
              <option value="Cần Thơ">Cần Thơ</option>
              <option value="Hải Phòng">Hải Phòng</option>
              <option value="Huế">Huế</option>
            </select>
          </div>

          {/* Job Type Filter */}
          <div>
            <label className="block text-[11px] font-bold uppercase text-signal-slate mb-1">Hình thức</label>
            <select
              value={jobTypeFilter}
              onChange={(e) => setJobTypeFilter(e.target.value)}
              className="w-full bg-signal-offwhite text-xs font-medium rounded-xl px-3 py-2 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
            >
              <option value="all">Mọi hình thức</option>
              <option value="full_time">Toàn thời gian</option>
              <option value="hybrid">Linh hoạt (Hybrid)</option>
              <option value="remote">Làm từ xa (Remote)</option>
              <option value="part_time">Bán thời gian</option>
              <option value="internship">Thực tập</option>
            </select>
          </div>

          {/* Experience Filter */}
          <div>
            <label className="block text-[11px] font-bold uppercase text-signal-slate mb-1">Cấp bậc</label>
            <select
              value={experienceFilter}
              onChange={(e) => setExperienceFilter(e.target.value)}
              className="w-full bg-signal-offwhite text-xs font-medium rounded-xl px-3 py-2 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
            >
              <option value="all">Mọi cấp bậc</option>
              <option value="entry">Intern / Entry</option>
              <option value="junior">Junior</option>
              <option value="mid">Middle</option>
              <option value="senior">Senior</option>
              <option value="lead">Lead / Quản lý</option>
            </select>
          </div>

          {/* Salary Filter */}
          <div>
            <label className="block text-[11px] font-bold uppercase text-signal-slate mb-1">Mức lương</label>
            <select
              value={salaryFilter}
              onChange={(e) => setSalaryFilter(e.target.value)}
              className="w-full bg-signal-offwhite text-xs font-medium rounded-xl px-3 py-2 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
            >
              <option value="all">Tất cả mức lương</option>
              <option value="<15">Dưới 15 triệu</option>
              <option value="15-30">15 - 30 triệu</option>
              <option value="30-50">30 - 50 triệu</option>
              <option value=">50">Trên 50 triệu</option>
            </select>
          </div>

          {/* Sorting */}
          <div>
            <label className="block text-[11px] font-bold uppercase text-signal-slate mb-1">Sắp xếp theo</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="w-full bg-signal-offwhite text-xs font-semibold rounded-xl px-3 py-2 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
            >
              <option value="newest">Mới nhất</option>
              <option value="match">Độ phù hợp AI</option>
              <option value="salary_desc">Lương cao nhất</option>
              <option value="salary_asc">Lương tăng dần</option>
            </select>
          </div>
        </div>

        {/* Quick active filters reset button */}
        {(searchQuery || industryFilter !== 'all' || locationFilter !== 'all' || jobTypeFilter !== 'all' || experienceFilter !== 'all' || salaryFilter !== 'all' || sortBy !== 'newest') && (
          <div className="flex items-center justify-between pt-2 text-xs">
            <span className="text-signal-slate">
              Đang áp dụng bộ lọc: <span className="font-semibold text-signal-navy">{displayJobs.length} kết quả</span>
            </span>
            <button
              type="button"
              onClick={handleResetFilters}
              className="text-signal-navy font-semibold hover:underline flex items-center gap-1"
            >
              <X className="w-3.5 h-3.5" /> Xóa toàn bộ bộ lọc
            </button>
          </div>
        )}
      </form>

      {/* Results Header */}
      <div className="flex items-center justify-between text-xs text-signal-slate px-1">
        <span>Hiển thị <strong className="text-signal-navy">{displayJobs.length}</strong> việc làm tuyển dụng</span>
        <div className="flex items-center gap-2">
          <span>Hệ thống tuyển dụng trực tuyến (PostgreSQL + Gemini AI)</span>
          {jobs.length <= 2 && (
            <button
              type="button"
              disabled={isSeeding}
              onClick={async () => {
                setIsSeeding(true);
                try {
                  await apiService.seedMultiIndustryJobs();
                  invalidateJobs();
                } catch (e) {
                  console.error('Seed error:', e);
                } finally {
                  setIsSeeding(false);
                }
              }}
              className="text-signal-navy hover:underline font-semibold ml-2 disabled:opacity-50"
            >
              {isSeeding ? '(Đang đồng bộ...)' : '(Đồng bộ 50 việc làm)'}
            </button>
          )}
        </div>
      </div>

      {/* Job Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {isJobsLoading && jobs.length === 0 ? (
          // Fast pulse skeletons
          Array.from({ length: 6 }).map((_, idx) => (
            <div key={idx} className="bg-white rounded-3xl border border-slate-200/80 p-6 space-y-4 animate-pulse">
              <div className="flex items-start justify-between">
                <div className="w-12 h-12 bg-slate-100 rounded-2xl" />
                <div className="w-16 h-6 bg-slate-100 rounded-full" />
              </div>
              <div className="space-y-2">
                <div className="w-3/4 h-5 bg-slate-100 rounded-lg" />
                <div className="w-1/2 h-4 bg-slate-100 rounded-lg" />
              </div>
              <div className="flex gap-2 pt-2">
                <div className="w-16 h-5 bg-slate-100 rounded-full" />
                <div className="w-20 h-5 bg-slate-100 rounded-full" />
              </div>
              <div className="pt-4 border-t border-slate-100 flex justify-between items-center">
                <div className="w-24 h-4 bg-slate-100 rounded" />
                <div className="w-20 h-8 bg-slate-100 rounded-xl" />
              </div>
            </div>
          ))
        ) : displayJobs.length > 0 ? (
          displayJobs.map((job) => {
            const breakdown = jobMatchMap.get(job.id);
            const score = breakdown?.overallScore;
            return (
              <JobCard
                key={job.id}
                job={job}
                matchScore={score}
                onViewDetails={(j) => setSelectedJobForDetail(j)}
                onApply={(j) => setSelectedJobForApply(j)}
              />
            );
          })
        ) : (
          <div className="col-span-full py-16 text-center bg-white rounded-3xl border border-slate-200 p-8 space-y-4">
            <Search className="w-12 h-12 text-slate-300 mx-auto" />
            <h4 className="font-heading font-bold text-lg text-signal-navy">
              Không tìm thấy công việc phù hợp với tiêu chí
            </h4>
            <p className="text-sm text-signal-slate max-w-md mx-auto">
              Thử thay đổi từ khóa, mở rộng khoảng lương hoặc chọn ngành nghề khác để xem các cơ hội tương đương.
            </p>
            <Button
              variant="outline"
              size="sm"
              onClick={handleResetFilters}
            >
              Xem toàn bộ 50 việc làm
            </Button>
          </div>
        )}
      </div>

      {/* Job Details Modal with AI Matching Insights */}
      <Modal
        isOpen={!!selectedJobForDetail}
        onClose={() => setSelectedJobForDetail(null)}
        title={selectedJobForDetail?.title || ''}
        subtitle={`${selectedJobForDetail?.companyName} · ${selectedJobForDetail?.location}`}
        maxWidth="2xl"
      >
        {selectedJobForDetail && (
          <div className="space-y-6 max-h-[75vh] overflow-y-auto pr-1">
            {/* Meta tags */}
            <div className="flex flex-wrap items-center gap-2 pb-4 border-b border-slate-100">
              <StatusBadge status={selectedJobForDetail.status} />
              <span className="text-xs px-3 py-1 rounded-full bg-signal-offwhite border border-slate-200 font-semibold text-signal-navy">
                {selectedJobForDetail.jobType}
              </span>
              <span className="text-xs px-3 py-1 rounded-full bg-signal-offwhite border border-slate-200 font-semibold text-signal-navy capitalize">
                Cấp bậc: {selectedJobForDetail.experienceLevel}
              </span>
              <span className="text-xs px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 font-bold text-emerald-800">
                Lương: {selectedJobForDetail.salaryMin ? `${selectedJobForDetail.salaryMin / 1000000}Tr` : ''} - {selectedJobForDetail.salaryMax ? `${selectedJobForDetail.salaryMax / 1000000}Tr VND` : 'Thỏa thuận'}
              </span>
            </div>

            {/* AI Matching Diagnostic Card (if primary CV present) */}
            {selectedJobBreakdown && (
              <div className="p-4 rounded-2xl bg-gradient-to-br from-signal-offwhite to-slate-100 border border-slate-200 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-signal-navy" />
                    <h5 className="font-heading font-bold text-sm text-signal-navy">
                      Đánh giá Độ tương thích AI với hồ sơ của bạn
                    </h5>
                  </div>
                  <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-signal-navy text-signal-lime text-xs font-bold">
                    <span>{selectedJobBreakdown.overallScore}% Tổng thể</span>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2 text-center text-xs">
                  <div className="bg-white p-2.5 rounded-xl border border-slate-200">
                    <span className="block text-slate-500 text-[10px] uppercase font-bold">Kỹ năng cốt lõi (50%)</span>
                    <span className="font-bold text-sm text-signal-navy">{selectedJobBreakdown.hardSkillsScore}%</span>
                  </div>
                  <div className="bg-white p-2.5 rounded-xl border border-slate-200">
                    <span className="block text-slate-500 text-[10px] uppercase font-bold">Ngữ nghĩa Gemini (30%)</span>
                    <span className="font-bold text-sm text-signal-navy">{selectedJobBreakdown.semanticScore}%</span>
                  </div>
                  <div className="bg-white p-2.5 rounded-xl border border-slate-200">
                    <span className="block text-slate-500 text-[10px] uppercase font-bold">Kinh nghiệm (20%)</span>
                    <span className="font-bold text-sm text-signal-navy">{selectedJobBreakdown.experienceScore}%</span>
                  </div>
                </div>

                {selectedJobBreakdown.aiExplanation && (
                  <p className="text-xs text-slate-700 leading-relaxed italic bg-white/60 p-2.5 rounded-xl">
                    &ldquo;{selectedJobBreakdown.aiExplanation}&rdquo;
                  </p>
                )}

                {selectedJobBreakdown.matchedSkills.length > 0 && (
                  <div>
                    <span className="text-[11px] font-bold text-emerald-800 uppercase block mb-1">
                      Kỹ năng đáp ứng ({selectedJobBreakdown.matchedSkills.length}):
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {selectedJobBreakdown.matchedSkills.map((sk, idx) => (
                        <span key={idx} className="text-[11px] px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 font-medium">
                          ✓ {sk}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {selectedJobBreakdown.missingRequiredSkills.length > 0 && (
                  <div>
                    <span className="text-[11px] font-bold text-rose-800 uppercase block mb-1">
                      Kỹ năng cần bổ sung ({selectedJobBreakdown.missingRequiredSkills.length}):
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {selectedJobBreakdown.missingRequiredSkills.map((sk, idx) => (
                        <span key={idx} className="text-[11px] px-2 py-0.5 rounded-md bg-rose-100 text-rose-800 font-medium">
                          ✕ {sk}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            <div>
              <h4 className="font-heading font-bold text-sm text-signal-navy uppercase tracking-wider mb-2">
                Mô tả công việc
              </h4>
              <p className="text-sm text-slate-600 leading-relaxed whitespace-pre-line">
                {selectedJobForDetail.description}
              </p>
            </div>

            <div>
              <h4 className="font-heading font-bold text-sm text-signal-navy uppercase tracking-wider mb-2">
                Yêu cầu ứng viên
              </h4>
              <p className="text-sm text-slate-600 leading-relaxed whitespace-pre-line">
                {selectedJobForDetail.requirements}
              </p>
            </div>

            {selectedJobForDetail.benefits && (
              <div>
                <h4 className="font-heading font-bold text-sm text-signal-navy uppercase tracking-wider mb-2">
                  Quyền lợi & Đãi ngộ
                </h4>
                <p className="text-sm text-slate-600 leading-relaxed whitespace-pre-line">
                  {selectedJobForDetail.benefits}
                </p>
              </div>
            )}

            <div>
              <h4 className="font-heading font-bold text-sm text-signal-navy uppercase tracking-wider mb-2">
                Kỹ năng chuyên môn yêu cầu
              </h4>
              <div className="flex flex-wrap gap-2">
                {(selectedJobForDetail.requiredSkills || []).map((sk, i) => (
                  <SkillBadge key={i} name={sk} variant="default" />
                ))}
              </div>
            </div>

            {selectedJobForDetail.preferredSkills && selectedJobForDetail.preferredSkills.length > 0 && (
              <div>
                <h4 className="font-heading font-bold text-sm text-signal-navy uppercase tracking-wider mb-2">
                  Kỹ năng ưu tiên
                </h4>
                <div className="flex flex-wrap gap-2">
                  {selectedJobForDetail.preferredSkills.map((sk, i) => (
                    <SkillBadge key={i} name={sk} variant="lavender" />
                  ))}
                </div>
              </div>
            )}

            <div className="pt-6 border-t border-slate-100 flex items-center justify-end gap-3">
              <Button
                variant="outline"
                onClick={() => setSelectedJobForDetail(null)}
              >
                Đóng
              </Button>
              <Button
                variant="lime"
                onClick={() => {
                  const target = selectedJobForDetail;
                  setSelectedJobForDetail(null);
                  setSelectedJobForApply(target);
                }}
              >
                Ứng tuyển vị trí này
              </Button>
            </div>
          </div>
        )}
      </Modal>

      {/* Apply Modal */}
      <Modal
        isOpen={!!selectedJobForApply}
        onClose={() => !isApplying && setSelectedJobForApply(null)}
        title="Nộp đơn Ứng tuyển"
        subtitle={`Vị trí: ${selectedJobForApply?.title} tại ${selectedJobForApply?.companyName}`}
        maxWidth="md"
      >
        {applySuccess ? (
          <div className="py-8 text-center space-y-3">
            <CheckCircle2 className="w-16 h-16 text-emerald-500 mx-auto animate-bounce" />
            <h4 className="font-heading text-xl font-bold text-signal-navy">
              Nộp đơn ứng tuyển thành công!
            </h4>
            <p className="text-sm text-signal-slate">
              Hồ sơ và bản phân tích tương thích AI đã được chuyển đến nhà tuyển dụng.
            </p>
          </div>
        ) : (
          <form onSubmit={handleApplySubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
                Chọn CV để nộp
              </label>
              {cvs.length > 0 ? (
                <select
                  value={selectedCvId}
                  onChange={(e) => setSelectedCvId(e.target.value)}
                  className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
                >
                  {cvs.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.fileName} {c.isPrimary ? '(CV Chính)' : ''}
                    </option>
                  ))}
                </select>
              ) : (
                <p className="text-xs text-rose-600">
                  Bạn chưa có CV nào trong hồ sơ. Vui lòng tải CV trước khi nộp đơn.
                </p>
              )}
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
                Thư giới thiệu (Cover Letter) - Tùy chọn
              </label>
              <textarea
                rows={4}
                value={coverLetter}
                onChange={(e) => setCoverLetter(e.target.value)}
                placeholder="Nêu bật lý do bạn phù hợp với vị trí này..."
                className="w-full bg-signal-offwhite text-sm rounded-xl p-3 border border-slate-200 focus:outline-none focus:border-signal-navy"
              />
            </div>

            <div className="pt-4 border-t border-slate-100 flex items-center justify-end gap-3">
              <Button
                type="button"
                variant="outline"
                onClick={() => setSelectedJobForApply(null)}
              >
                Hủy bỏ
              </Button>
              <Button
                type="submit"
                variant="lime"
                isLoading={isApplying}
                disabled={cvs.length === 0}
              >
                Xác nhận nộp đơn
              </Button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import { Job, CV } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { JobCard } from '../../components/ui/JobCard';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { SkillBadge, StatusBadge } from '../../components/ui/SkillBadge';
import { MatchScoreRing } from '../../components/ui/MatchScoreRing';
import { Search, MapPin, Briefcase, Filter, CheckCircle2, Sparkles, Building2 } from 'lucide-react';

export const JobDiscovery: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [cvs, setCvs] = useState<CV[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [locationFilter, setLocationFilter] = useState('all');
  const [jobTypeFilter, setJobTypeFilter] = useState('all');

  // Modal States
  const [selectedJobForDetail, setSelectedJobForDetail] = useState<Job | null>(null);
  const [selectedJobForApply, setSelectedJobForApply] = useState<Job | null>(null);
  const [selectedCvId, setSelectedCvId] = useState<string>('');
  const [coverLetter, setCoverLetter] = useState<string>('');
  const [isApplying, setIsApplying] = useState(false);
  const [applySuccess, setApplySuccess] = useState(false);

  useEffect(() => {
    loadJobs();
    apiService.getCandidateCVs('user-cand-1').then(data => {
      setCvs(data);
      if (data.length > 0) setSelectedCvId(data[0].id);
    });
  }, []);

  const loadJobs = () => {
    apiService.getJobs({
      search: searchQuery,
      location: locationFilter,
      jobType: jobTypeFilter,
    }).then(setJobs);
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadJobs();
  };

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

  return (
    <div className="space-y-6">
      <PageHeader
        title="Khám phá Cơ hội Việc làm"
        subtitle="Tìm kiếm hàng trăm vị trí công nghệ được AI xếp hạng theo mức độ tương thích với hồ sơ của bạn."
      />

      {/* Search and Filters Bar */}
      <form onSubmit={handleSearchSubmit} className="bg-white p-4 sm:p-5 rounded-3xl border border-slate-200/80 shadow-sm space-y-4">
        <div className="flex flex-col md:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-5 h-5 text-slate-400 absolute left-4 top-3.5" />
            <input
              type="text"
              placeholder="Tìm theo chức danh, từ khóa kỹ năng (Python, React, LLMs)..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 bg-signal-offwhite text-sm rounded-2xl border border-slate-200 focus:outline-none focus:border-signal-navy focus:bg-white"
            />
          </div>

          <div className="flex flex-wrap sm:flex-nowrap gap-3">
            <select
              value={locationFilter}
              onChange={(e) => setLocationFilter(e.target.value)}
              className="bg-signal-offwhite text-sm font-medium rounded-2xl px-4 py-3 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
            >
              <option value="all">Tất cả địa điểm</option>
              <option value="TP.HCM">TP. Hồ Chí Minh</option>
              <option value="Hà Nội">Hà Nội</option>
              <option value="Đà Nẵng">Đà Nẵng</option>
            </select>

            <select
              value={jobTypeFilter}
              onChange={(e) => setJobTypeFilter(e.target.value)}
              className="bg-signal-offwhite text-sm font-medium rounded-2xl px-4 py-3 border border-slate-200 focus:outline-none focus:border-signal-navy cursor-pointer"
            >
              <option value="all">Mọi hình thức</option>
              <option value="full_time">Toàn thời gian</option>
              <option value="hybrid">Hybrid</option>
              <option value="remote">Remote (Từ xa)</option>
              <option value="part_time">Bán thời gian</option>
            </select>

            <Button type="submit" variant="primary" size="md">
              Tìm kiếm
            </Button>
          </div>
        </div>
      </form>

      {/* Job Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {jobs.length > 0 ? (
          jobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              matchScore={job.id === 'job-1' ? 92 : job.id === 'job-2' ? 86 : 80}
              onViewDetails={(j) => setSelectedJobForDetail(j)}
              onApply={(j) => setSelectedJobForApply(j)}
            />
          ))
        ) : (
          <div className="col-span-full py-16 text-center bg-white rounded-3xl border border-slate-200 p-8">
            <Search className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <h4 className="font-heading font-bold text-lg text-signal-navy">
              Không tìm thấy công việc phù hợp
            </h4>
            <p className="text-sm text-signal-slate mt-1 mb-4">
              Thử thay đổi từ khóa hoặc bộ lọc để mở rộng kết quả tìm kiếm.
            </p>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                setSearchQuery('');
                setLocationFilter('all');
                setJobTypeFilter('all');
                loadJobs();
              }}
            >
              Xóa tất cả bộ lọc
            </Button>
          </div>
        )}
      </div>

      {/* Job Details Modal */}
      <Modal
        isOpen={!!selectedJobForDetail}
        onClose={() => setSelectedJobForDetail(null)}
        title={selectedJobForDetail?.title || ''}
        subtitle={`${selectedJobForDetail?.companyName} · ${selectedJobForDetail?.location}`}
        maxWidth="xl"
      >
        {selectedJobForDetail && (
          <div className="space-y-6">
            <div className="flex flex-wrap items-center gap-2 pb-4 border-b border-slate-100">
              <StatusBadge status={selectedJobForDetail.status} />
              <span className="text-xs px-3 py-1 rounded-full bg-signal-offwhite border border-slate-200 font-semibold text-signal-navy">
                {selectedJobForDetail.jobType}
              </span>
              <span className="text-xs px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 font-bold text-emerald-800">
                Lương: {selectedJobForDetail.salaryMin ? `${selectedJobForDetail.salaryMin / 1000000}Tr` : ''} - {selectedJobForDetail.salaryMax ? `${selectedJobForDetail.salaryMax / 1000000}Tr VND` : 'Thỏa thuận'}
              </span>
            </div>

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
                {selectedJobForDetail.requiredSkills.map((sk, i) => (
                  <SkillBadge key={i} name={sk} variant="default" />
                ))}
              </div>
            </div>

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
              Hệ thống đã chuyển CV của bạn đến nhà tuyển dụng kèm phân tích điểm tương thích AI.
            </p>
          </div>
        ) : (
          <form onSubmit={handleApplySubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
                Chọn CV để gửi
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
                placeholder="Tóm tắt ngắn gọn lý do bạn phù hợp với vị trí này..."
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

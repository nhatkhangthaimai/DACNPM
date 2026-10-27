import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import { Job } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { StatusBadge, SkillBadge } from '../../components/ui/SkillBadge';
import { CheckCircle2, XCircle, AlertCircle, Eye, Building2, Briefcase } from 'lucide-react';

export const JobModeration: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [isRejectModalOpen, setIsRejectModalOpen] = useState(false);
  const [rejectReason, setRejectReason] = useState('');

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = () => {
    apiService.getJobs().then(setJobs);
  };

  const handleApprove = async (jobId: string) => {
    await apiService.updateJobStatus(jobId, 'published');
    setSelectedJob(null);
    loadJobs();
  };

  const handleRejectConfirm = async () => {
    if (!selectedJob || !rejectReason.trim()) {
      alert('Vui lòng nhập lý do từ chối kiểm duyệt.');
      return;
    }
    await apiService.updateJobStatus(selectedJob.id, 'rejected', rejectReason);
    setIsRejectModalOpen(false);
    setSelectedJob(null);
    setRejectReason('');
    loadJobs();
  };

  const pendingJobs = jobs.filter(j => j.status === 'pending_approval');
  const moderatedJobs = jobs.filter(j => j.status !== 'pending_approval');

  return (
    <div className="space-y-8">
      <PageHeader
        title="Kiểm duyệt Tin Tuyển dụng (Job Moderation)"
        subtitle="Đảm bảo các tin tuyển dụng tuân thủ tiêu chuẩn chất lượng, minh bạch mức lương và chính sách tuyển dụng."
        badge={`${pendingJobs.length} Tin chờ duyệt`}
      />

      {/* Pending Approval Section */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8 space-y-4">
        <h3 className="font-heading font-bold text-xl text-signal-navy flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-signal-gold animate-pulse" />
          Tin đang chờ phê duyệt ({pendingJobs.length})
        </h3>

        {pendingJobs.length > 0 ? (
          <div className="divide-y divide-slate-100">
            {pendingJobs.map((job) => (
              <div key={job.id} className="py-5 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                <div>
                  <div className="flex items-center gap-2.5 mb-1.5">
                    <h4 className="font-heading font-bold text-lg text-signal-navy">
                      {job.title}
                    </h4>
                    <StatusBadge status={job.status} />
                  </div>
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-signal-slate mb-3">
                    <span className="font-semibold text-signal-navy">{job.companyName}</span>
                    <span>{job.location}</span>
                    <span>{job.jobType}</span>
                    <span className="text-emerald-700 font-semibold">
                      {job.salaryMin ? `${job.salaryMin / 1000000}Tr` : ''} - {job.salaryMax ? `${job.salaryMax / 1000000}Tr VND` : 'Thỏa thuận'}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 line-clamp-2 max-w-2xl leading-relaxed">
                    {job.description}
                  </p>
                </div>

                <div className="flex items-center gap-2.5 shrink-0 justify-end">
                  <Button
                    variant="outline"
                    size="sm"
                    icon={<Eye className="w-3.5 h-3.5" />}
                    onClick={() => setSelectedJob(job)}
                  >
                    Xem chi tiết
                  </Button>
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => {
                      setSelectedJob(job);
                      setIsRejectModalOpen(true);
                    }}
                  >
                    Từ chối
                  </Button>
                  <Button
                    variant="lime"
                    size="sm"
                    icon={<CheckCircle2 className="w-3.5 h-3.5 text-signal-navy" />}
                    onClick={() => handleApprove(job.id)}
                  >
                    Phê duyệt tin
                  </Button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="py-8 text-center text-xs text-slate-500 italic">
            Tất cả các tin tuyển dụng đã được xử lý xong.
          </div>
        )}
      </div>

      {/* Moderated History Section */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8 space-y-4">
        <h3 className="font-heading font-bold text-xl text-signal-navy">
          Lịch sử tin tuyển dụng trong hệ thống ({moderatedJobs.length})
        </h3>

        <div className="divide-y divide-slate-100">
          {moderatedJobs.map((job) => (
            <div key={job.id} className="py-4 flex items-center justify-between text-xs">
              <div>
                <span className="font-bold text-signal-navy text-sm block">
                  {job.title}
                </span>
                <span className="text-signal-slate">
                  {job.companyName} · Đăng ngày {new Date(job.createdAt).toLocaleDateString('vi-VN')}
                </span>
                {job.rejectionReason && (
                  <span className="text-rose-600 block mt-1 font-medium">
                    Lý do từ chối: {job.rejectionReason}
                  </span>
                )}
              </div>
              <div className="flex items-center gap-3">
                <StatusBadge status={job.status} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Reject Modal with Mandatory Reason */}
      <Modal
        isOpen={isRejectModalOpen}
        onClose={() => setIsRejectModalOpen(false)}
        title="Từ chối Phê duyệt Tin tuyển dụng"
        subtitle={`Vị trí: ${selectedJob?.title} tại ${selectedJob?.companyName}`}
        maxWidth="md"
      >
        <div className="space-y-4">
          <div className="p-3 rounded-xl bg-rose-50 text-rose-800 text-xs border border-rose-200 flex items-start gap-2">
            <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
            <span>
              Lý do từ chối sẽ được gửi trực tiếp cho Nhà tuyển dụng để chỉnh sửa nội dung phù hợp.
            </span>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Lý do từ chối cụ thể *
            </label>
            <textarea
              rows={4}
              required
              value={rejectReason}
              onChange={(e) => setRejectReason(e.target.value)}
              placeholder="Ví dụ: Thiếu thông tin rõ ràng về mức lương, yêu cầu kỹ năng không hợp lệ..."
              className="w-full bg-signal-offwhite text-sm rounded-xl p-3 border border-slate-200 focus:outline-none focus:border-rose-500"
            />
          </div>

          <div className="pt-4 border-t border-slate-100 flex justify-end gap-3">
            <Button variant="outline" onClick={() => setIsRejectModalOpen(false)}>
              Hủy
            </Button>
            <Button variant="danger" onClick={handleRejectConfirm}>
              Xác nhận Từ chối
            </Button>
          </div>
        </div>
      </Modal>

      {/* View Detail Modal */}
      <Modal
        isOpen={!!selectedJob && !isRejectModalOpen}
        onClose={() => setSelectedJob(null)}
        title={selectedJob?.title || ''}
        subtitle={`${selectedJob?.companyName} · ${selectedJob?.location}`}
        maxWidth="xl"
      >
        {selectedJob && (
          <div className="space-y-5">
            <div>
              <h5 className="font-heading font-bold text-xs uppercase text-signal-slate mb-1">Mô tả:</h5>
              <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">{selectedJob.description}</p>
            </div>
            <div>
              <h5 className="font-heading font-bold text-xs uppercase text-signal-slate mb-1">Yêu cầu:</h5>
              <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">{selectedJob.requirements}</p>
            </div>
            <div>
              <h5 className="font-heading font-bold text-xs uppercase text-signal-slate mb-1">Kỹ năng:</h5>
              <div className="flex flex-wrap gap-2">
                {selectedJob.requiredSkills.map((s, idx) => (
                  <SkillBadge key={idx} name={s} variant="default" />
                ))}
              </div>
            </div>
            <div className="pt-4 border-t border-slate-100 flex justify-end gap-3">
              <Button variant="outline" onClick={() => setSelectedJob(null)}>
                Đóng
              </Button>
              {selectedJob.status === 'pending_approval' && (
                <Button variant="lime" onClick={() => handleApprove(selectedJob.id)}>
                  Phê duyệt tin này
                </Button>
              )}
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

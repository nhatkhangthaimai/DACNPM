import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../../services/api';
import { Job } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { StatusBadge } from '../../components/ui/SkillBadge';
import { Plus, Briefcase, Eye, ToggleLeft, ToggleRight, Search, Users } from 'lucide-react';

export const JobManagement: React.FC = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = () => {
    apiService.getJobs().then(setJobs);
  };

  const handleToggleStatus = async (job: Job) => {
    const nextStatus = job.status === 'published' ? 'closed' : 'published';
    await apiService.updateJobStatus(job.id, nextStatus);
    loadJobs();
  };

  const filteredJobs = jobs.filter(j => {
    if (filterStatus !== 'all' && j.status !== filterStatus) return false;
    if (search && !j.title.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title="Quản lý Tin Tuyển dụng"
        subtitle="Soạn thảo, xuất bản, đóng/mở tin tuyển dụng và theo dõi tiến độ duyệt tin."
        actions={
          <Button
            variant="primary"
            icon={<Plus className="w-4 h-4 text-signal-lime" />}
            onClick={() => navigate('/recruiter/jobs/new')}
          >
            Tạo JD mới
          </Button>
        }
      />

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 sm:p-5 rounded-3xl border border-slate-200/80 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            placeholder="Tìm theo tiêu đề tin..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 text-xs bg-signal-offwhite rounded-xl border border-slate-200 focus:outline-none focus:border-signal-navy"
          />
        </div>

        <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto">
          {['all', 'published', 'pending_approval', 'closed', 'draft'].map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold capitalize whitespace-nowrap transition-all ${
                filterStatus === st
                  ? 'bg-signal-navy text-white'
                  : 'bg-signal-offwhite text-signal-slate hover:bg-slate-200/60'
              }`}
            >
              {st === 'all' ? 'Tất cả' : st === 'published' ? 'Đang mở' : st === 'pending_approval' ? 'Chờ duyệt' : st === 'closed' ? 'Đã đóng' : 'Bản nháp'}
            </button>
          ))}
        </div>
      </div>

      {/* Jobs Table */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-signal-offwhite border-b border-slate-200/80 text-[11px] font-bold uppercase tracking-wider text-signal-slate">
                <th className="py-4 px-6">Tiêu đề tin tuyển dụng</th>
                <th className="py-4 px-6">Hình thức & Địa điểm</th>
                <th className="py-4 px-6">Mức lương</th>
                <th className="py-4 px-6">Trạng thái</th>
                <th className="py-4 px-6 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {filteredJobs.map((job) => (
                <tr key={job.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="py-4 px-6">
                    <span className="font-heading font-bold text-signal-navy block">
                      {job.title}
                    </span>
                    <span className="text-xs text-signal-slate">
                      {job.companyName} · Đăng ngày {new Date(job.createdAt).toLocaleDateString('vi-VN')}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-xs text-slate-600">
                    <div>{job.location}</div>
                    <span className="text-signal-slate">{job.jobType}</span>
                  </td>
                  <td className="py-4 px-6 text-xs font-semibold text-emerald-700">
                    {job.salaryMin ? `${job.salaryMin / 1000000}Tr` : ''} - {job.salaryMax ? `${job.salaryMax / 1000000}Tr VND` : 'Thỏa thuận'}
                  </td>
                  <td className="py-4 px-6">
                    <StatusBadge status={job.status} />
                  </td>
                  <td className="py-4 px-6 text-right space-x-2">
                    <Button
                      variant="soft"
                      size="sm"
                      icon={<Users className="w-3.5 h-3.5" />}
                      onClick={() => navigate('/recruiter/applications')}
                    >
                      Ứng viên
                    </Button>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleToggleStatus(job)}
                    >
                      {job.status === 'published' ? 'Đóng tin' : 'Mở lại'}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

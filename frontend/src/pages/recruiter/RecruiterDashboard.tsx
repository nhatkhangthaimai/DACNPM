import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../../services/api';
import { Job, Application } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { StatCard } from '../../components/ui/StatCard';
import { Button } from '../../components/ui/Button';
import { StatusBadge } from '../../components/ui/SkillBadge';
import { MatchScoreRing } from '../../components/ui/MatchScoreRing';
import {
  Briefcase,
  Users,
  CheckCircle2,
  Clock,
  Plus,
  ArrowRight,
  TrendingUp,
  Sparkles,
  Building2
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

export const RecruiterDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [applications, setApplications] = useState<Application[]>([]);

  useEffect(() => {
    apiService.getJobs().then(setJobs);
    apiService.getApplications('recruiter').then(setApplications);
  }, []);

  const openJobs = jobs.filter(j => j.status === 'published');
  const pendingJobs = jobs.filter(j => j.status === 'pending_approval');

  // Chart data
  const pipelineData = [
    { name: 'Mới nộp', count: applications.filter(a => a.status === 'submitted').length },
    { name: 'Đang duyệt', count: applications.filter(a => a.status === 'reviewing').length },
    { name: 'Phỏng vấn', count: applications.filter(a => a.status === 'interviewed' || a.status === 'shortlisted').length },
    { name: 'Mời nhận việc', count: applications.filter(a => a.status === 'offered').length },
  ];

  const scoreDistribution = [
    { name: 'Xuất sắc (>85%)', value: 4, color: '#C9F16A' },
    { name: 'Khá (70-85%)', value: 6, color: '#68DCC5' },
    { name: 'Trung bình (50-70%)', value: 3, color: '#FFCE7D' },
    { name: 'Cần bổ sung (<50%)', value: 1, color: '#FF876D' },
  ];

  return (
    <div className="space-y-8">
      <PageHeader
        title="Dashboard Tuyển dụng & Phân tích Ứng viên"
        subtitle="Quản lý phễu ứng tuyển, hiệu suất tuyển dụng và bảng xếp hạng nhân tài bằng AI Matching."
        actions={
          <Button
            variant="primary"
            icon={<Plus className="w-4 h-4 text-signal-lime" />}
            onClick={() => navigate('/recruiter/jobs/new')}
          >
            Đăng tin JD mới
          </Button>
        }
      />

      {/* Top Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Tin tuyển dụng đang mở"
          value={openJobs.length}
          subtitle={`${pendingJobs.length} tin đang chờ duyệt`}
          icon={Briefcase}
          trend={{ value: '+2 tháng này', isPositive: true }}
          variant="white"
        />
        <StatCard
          title="Tổng hồ sơ ứng tuyển"
          value={applications.length}
          subtitle="Tự động xếp hạng bởi AI"
          icon={Users}
          variant="navy"
        />
        <StatCard
          title="Ứng viên chất lượng cao (>85%)"
          value="4"
          subtitle="Sẵn sàng gửi lời mời phỏng vấn"
          icon={Sparkles}
          variant="lime"
        />
        <StatCard
          title="Thời gian xử lý TB"
          value="1.8 ngày"
          subtitle="Nhanh hơn 60% nhờ AI"
          icon={Clock}
          variant="white"
        />
      </div>

      {/* Charts Bento Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recruitment Pipeline Bar Chart */}
        <div className="lg:col-span-2 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-heading font-bold text-lg text-signal-navy">
                Phễu Ứng viên theo Trạng thái (Recruitment Pipeline)
              </h3>
              <p className="text-xs text-signal-slate mt-1">
                Số lượng ứng viên chuyển đổi qua từng giai đoạn tuyển dụng
              </p>
            </div>
            <span className="text-xs font-semibold px-3 py-1 rounded-full bg-signal-offwhite border border-slate-200 text-signal-navy">
              Thời gian thực
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={pipelineData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
                <XAxis dataKey="name" stroke="#758193" fontSize={12} tickLine={false} />
                <YAxis stroke="#758193" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0C1A2D',
                    borderRadius: '12px',
                    color: '#fff',
                    border: 'none',
                    fontSize: '12px'
                  }}
                />
                <Bar dataKey="count" fill="#0C1A2D" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* AI Score Quality Distribution */}
        <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="font-heading font-bold text-lg text-signal-navy mb-1">
              Phân bố Điểm Match AI
            </h3>
            <p className="text-xs text-signal-slate mb-4">
              Chất lượng hồ sơ ứng viên theo thang điểm 100
            </p>

            <div className="h-44 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={scoreDistribution}
                    innerRadius={50}
                    outerRadius={75}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {scoreDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="space-y-2 mt-2">
              {scoreDistribution.map((item, idx) => (
                <div key={idx} className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                    <span className="text-signal-navy font-medium">{item.name}</span>
                  </div>
                  <span className="font-bold text-signal-navy">{item.value} hồ sơ</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Recent Open Jobs & Quick Applicants Review */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8 space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-heading font-bold text-xl text-signal-navy">
              Tin tuyển dụng đang hoạt động ({openJobs.length})
            </h3>
            <p className="text-xs text-signal-slate mt-1">
              Xem danh sách ứng viên và điểm tương thích tự động
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('/recruiter/jobs')}
          >
            Quản lý tất cả tin
          </Button>
        </div>

        <div className="divide-y divide-slate-100">
          {openJobs.map((job) => (
            <div key={job.id} className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2.5 mb-1">
                  <h4 className="font-heading font-bold text-base text-signal-navy">
                    {job.title}
                  </h4>
                  <StatusBadge status={job.status} />
                </div>
                <div className="flex items-center gap-4 text-xs text-signal-slate">
                  <span>{job.location}</span>
                  <span>{job.jobType}</span>
                  <span className="text-emerald-700 font-semibold">
                    {job.salaryMin ? `${job.salaryMin / 1000000}Tr` : ''} - {job.salaryMax ? `${job.salaryMax / 1000000}Tr VND` : 'Thỏa thuận'}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <Button
                  variant="lime"
                  size="sm"
                  icon={<Users className="w-4 h-4 text-signal-navy" />}
                  onClick={() => navigate('/recruiter/applications')}
                >
                  Xếp hạng ứng viên AI
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

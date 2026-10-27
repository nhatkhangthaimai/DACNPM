import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../../services/api';
import { Job } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { StatCard } from '../../components/ui/StatCard';
import { Button } from '../../components/ui/Button';
import { StatusBadge } from '../../components/ui/SkillBadge';
import {
  Users,
  Building2,
  Briefcase,
  CheckSquare,
  Cpu,
  ShieldCheck,
  TrendingUp,
  AlertTriangle,
  ArrowRight
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

export const AdminDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    apiService.getJobs().then(setJobs);
  }, []);

  const pendingJobs = jobs.filter(j => j.status === 'pending_approval');

  const growthData = [
    { month: 'T5', users: 120, jobs: 18 },
    { month: 'T6', users: 240, jobs: 35 },
    { month: 'T7', users: 480, jobs: 52 },
    { month: 'T8', users: 790, jobs: 84 },
    { month: 'T9', users: 1250, jobs: 110 },
    { month: 'T10', users: 1840, jobs: 145 },
  ];

  return (
    <div className="space-y-8">
      <PageHeader
        title="Bảng Điều khiển Quản trị Hệ thống (Admin Portal)"
        subtitle="Giám sát tình trạng vận hành nền tảng HireSense AI, kiểm duyệt nội dung và quản lý phân quyền."
        badge="System Superadmin"
        actions={
          <Button
            variant="lime"
            icon={<CheckSquare className="w-4 h-4 text-signal-navy" />}
            onClick={() => navigate('/admin/moderation')}
          >
            Kiểm duyệt {pendingJobs.length} tin chờ
          </Button>
        }
      />

      {/* Top Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <StatCard
          title="Tổng người dùng"
          value="1,840"
          subtitle="1,520 ứng viên · 320 NTD"
          icon={Users}
          trend={{ value: '+24% tháng này', isPositive: true }}
          variant="white"
        />
        <StatCard
          title="Tin đang chờ kiểm duyệt"
          value={pendingJobs.length}
          subtitle="Cần xem xét nội dung"
          icon={CheckSquare}
          variant="lime"
        />
        <StatCard
          title="Doanh nghiệp đối tác"
          value="48"
          subtitle="VNG, FPT, MoMo, VNPT..."
          icon={Building2}
          variant="white"
        />
        <StatCard
          title="Trạng thái Gemini AI"
          value="99.98%"
          subtitle="pgvector index: Healthy"
          icon={Cpu}
          variant="navy"
        />
      </div>

      {/* Growth Chart */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-heading font-bold text-lg text-signal-navy">
              Tăng trưởng Người dùng & Tin tuyển dụng
            </h3>
            <p className="text-xs text-signal-slate mt-1">
              Thống kê lượng truy cập và hoạt động thực tế 6 tháng gần nhất
            </p>
          </div>
          <span className="text-xs font-semibold px-3 py-1 rounded-full bg-signal-offwhite border border-slate-200 text-signal-navy">
            6 tháng qua
          </span>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={growthData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F1F5F9" />
              <XAxis dataKey="month" stroke="#758193" fontSize={12} tickLine={false} />
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
              <Line type="monotone" dataKey="users" name="Người dùng" stroke="#0C1A2D" strokeWidth={3} dot={{ r: 4 }} />
              <Line type="monotone" dataKey="jobs" name="Tin tuyển dụng" stroke="#C9F16A" strokeWidth={3} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Quick Pending Jobs Queue */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/80 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-heading font-bold text-lg text-signal-navy">
              Hàng đợi kiểm duyệt tin tuyển dụng ({pendingJobs.length})
            </h3>
            <p className="text-xs text-signal-slate mt-1">
              Phê duyệt hoặc từ chối các tin tuyển dụng mới gửi lên từ doanh nghiệp
            </p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('/admin/moderation')}
          >
            Xem tất cả hàng đợi
          </Button>
        </div>

        {pendingJobs.length > 0 ? (
          <div className="divide-y divide-slate-100">
            {pendingJobs.map((job) => (
              <div key={job.id} className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <h4 className="font-heading font-bold text-base text-signal-navy">
                    {job.title}
                  </h4>
                  <span className="text-xs text-signal-slate">
                    Đăng bởi: <strong>{job.companyName}</strong> · Địa điểm: {job.location}
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <Button
                    variant="lime"
                    size="sm"
                    onClick={() => navigate('/admin/moderation')}
                  >
                    Kiểm duyệt ngay
                  </Button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 py-4 italic">
            Hiện tại không có tin nào đang chờ duyệt.
          </p>
        )}
      </div>
    </div>
  );
};

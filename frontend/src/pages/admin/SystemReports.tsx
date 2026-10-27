import React from 'react';
import { PageHeader } from '../../components/layout/PageHeader';
import { StatCard } from '../../components/ui/StatCard';
import { Cpu, ShieldCheck, Zap, Activity, HardDrive, Database } from 'lucide-react';

export const SystemReports: React.FC = () => {
  const auditLogs = [
    {
      id: 'log-1',
      action: 'APPROVE_JOB',
      user: 'admin@hiresense.ai',
      target: 'Senior AI Engineer (VNG)',
      ip: '118.69.182.45',
      time: '15 phút trước',
    },
    {
      id: 'log-2',
      action: 'EXTRACT_CV_GEMINI',
      user: 'nguyenvanan.ai@gmail.com',
      target: 'Nguyen_Van_An_CV.pdf (Latency: 1.4s)',
      ip: '14.161.22.10',
      time: '32 phút trước',
    },
    {
      id: 'log-3',
      action: 'CALCULATE_HYBRID_MATCH',
      user: 'System Engine',
      target: 'Job #job-1 vs CV #cv-1 -> Score: 92%',
      ip: '127.0.0.1',
      time: '1 giờ trước',
    },
    {
      id: 'log-4',
      action: 'REGISTER_RECRUITER',
      user: 'hr.lead@vng.com.vn',
      target: 'Company: VNG Corporation',
      ip: '118.69.182.45',
      time: '2 giờ trước',
    },
  ];

  return (
    <div className="space-y-8">
      <PageHeader
        title="Báo cáo Hoạt động & Nhật ký Hệ thống (Audit Logs)"
        subtitle="Giám sát hiệu suất suy luận LLM, bộ đệm pgvector embeddings và lịch sử thao tác của các tài khoản quản trị."
      />

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <StatCard
          title="Thời gian phản hồi AI trung bình"
          value="1.42s"
          subtitle="Gemini 1.5 Flash API"
          icon={Zap}
          variant="lime"
        />
        <StatCard
          title="Vector Embeddings trong CSDL"
          value="12,480"
          subtitle="pgvector HNSW index: OK"
          icon={Database}
          variant="navy"
        />
        <StatCard
          title="Tỷ lệ thành công trích xuất"
          value="99.4%"
          subtitle="Pydantic validation passed"
          icon={Activity}
          variant="white"
        />
      </div>

      {/* Audit Log Table */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm p-6 sm:p-8 space-y-4">
        <h3 className="font-heading font-bold text-xl text-signal-navy">
          Nhật ký Hoạt động Quản trị & AI (Audit Trail)
        </h3>

        <div className="divide-y divide-slate-100">
          {auditLogs.map((log) => (
            <div key={log.id} className="py-3.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
              <div className="space-y-0.5">
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-signal-navy bg-signal-offwhite px-2 py-0.5 rounded-md border border-slate-200">
                    {log.action}
                  </span>
                  <span className="text-slate-600 font-medium">{log.target}</span>
                </div>
                <span className="text-slate-400 block">
                  Thực hiện bởi: {log.user} · IP: {log.ip}
                </span>
              </div>
              <span className="text-slate-400 sm:text-right shrink-0">{log.time}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

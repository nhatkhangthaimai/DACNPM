import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import { Application } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { StatusBadge } from '../../components/ui/SkillBadge';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { Send, Building2, Calendar, FileText, Sparkles, AlertCircle, XCircle } from 'lucide-react';

export const CandidateApplications: React.FC = () => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [selectedApp, setSelectedApp] = useState<Application | null>(null);

  useEffect(() => {
    loadApplications();
  }, []);

  const loadApplications = () => {
    apiService.getApplications('candidate').then(setApplications);
  };

  const handleWithdraw = async (id: string) => {
    if (confirm('Bạn có chắc chắn muốn rút đơn ứng tuyển vị trí này?')) {
      await apiService.updateApplicationStatus(id, 'withdrawn');
      loadApplications();
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Lịch sử Đơn Ứng tuyển"
        subtitle="Theo dõi tiến độ xét duyệt đơn, điểm tương thích AI và phản hồi trực tiếp từ nhà tuyển dụng."
      />

      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm overflow-hidden">
        {applications.length > 0 ? (
          <div className="divide-y divide-slate-100">
            {applications.map((app) => (
              <div
                key={app.id}
                className="p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6 hover:bg-slate-50/50 transition-colors"
              >
                <div className="space-y-1.5 max-w-xl">
                  <div className="flex items-center gap-2.5">
                    <span className="text-xs font-semibold text-signal-slate uppercase tracking-wider">
                      {app.companyName}
                    </span>
                    <StatusBadge status={app.status} />
                  </div>
                  <h4 className="font-heading font-bold text-lg text-signal-navy">
                    {app.jobTitle}
                  </h4>
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-signal-slate">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5" />
                      Ngày nộp: {new Date(app.createdAt).toLocaleDateString('vi-VN')}
                    </span>
                    {app.matchScore && (
                      <span className="flex items-center gap-1 font-semibold text-signal-navy">
                        <Sparkles className="w-3.5 h-3.5 text-signal-lime-dark" />
                        AI Match: {app.matchScore}%
                      </span>
                    )}
                  </div>

                  {app.coverLetter && (
                    <p className="text-xs text-slate-500 italic line-clamp-1 pt-1">
                      Thư giới thiệu: "{app.coverLetter}"
                    </p>
                  )}
                </div>

                <div className="flex items-center gap-3 w-full md:w-auto justify-end">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setSelectedApp(app)}
                  >
                    Xem chi tiết
                  </Button>

                  {app.status !== 'withdrawn' && app.status !== 'offered' && app.status !== 'rejected' && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleWithdraw(app.id)}
                      className="text-rose-600 hover:text-rose-700 hover:bg-rose-50"
                    >
                      Rút đơn
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-16 text-center">
            <Send className="w-12 h-12 text-slate-300 mx-auto mb-3" />
            <h4 className="font-heading font-bold text-lg text-signal-navy">
              Chưa có đơn ứng tuyển nào
            </h4>
            <p className="text-sm text-signal-slate mt-1 mb-4">
              Hãy khám phá các việc làm hấp dẫn và nộp đơn ngay để nhận kết quả phân tích AI.
            </p>
          </div>
        )}
      </div>

      {/* Detail Application Modal */}
      <Modal
        isOpen={!!selectedApp}
        onClose={() => setSelectedApp(null)}
        title="Chi tiết Đơn ứng tuyển"
        subtitle={`Vị trí: ${selectedApp?.jobTitle} · ${selectedApp?.companyName}`}
        maxWidth="md"
      >
        {selectedApp && (
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <span className="text-xs text-signal-slate">Trạng thái hiện tại:</span>
              <StatusBadge status={selectedApp.status} />
            </div>

            <div className="p-4 rounded-2xl bg-signal-offwhite border border-slate-200">
              <span className="text-xs font-semibold text-signal-slate uppercase tracking-wider block mb-1">
                Điểm tương thích AI:
              </span>
              <span className="font-heading font-bold text-2xl text-signal-navy">
                {selectedApp.matchScore || 85}%
              </span>
              {selectedApp.matchBreakdown && (
                <p className="text-xs text-slate-600 mt-2 leading-relaxed">
                  {selectedApp.matchBreakdown.aiExplanation}
                </p>
              )}
            </div>

            {selectedApp.internalNotes && (
              <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 text-xs">
                <span className="font-bold text-amber-900 block mb-1">
                  Ghi chú từ Nhà tuyển dụng:
                </span>
                <p className="text-amber-800">{selectedApp.internalNotes}</p>
              </div>
            )}

            <div className="pt-4 border-t border-slate-100 flex justify-end">
              <Button variant="primary" onClick={() => setSelectedApp(null)}>
                Đóng
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

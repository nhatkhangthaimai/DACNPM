import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Menu, Bell, Sparkles, Plus, CheckCircle, Search } from 'lucide-react';
import { Button } from '../ui/Button';

interface TopNavbarProps {
  onToggleSidebar: () => void;
}

export const TopNavbar: React.FC<TopNavbarProps> = ({ onToggleSidebar }) => {
  const { user, role } = useAuth();
  const navigate = useNavigate();
  const [showNotifications, setShowNotifications] = useState(false);

  const notifications = [
    {
      id: 1,
      title: 'Phân tích CV hoàn tất',
      message: 'Hồ sơ của bạn đạt 92% phù hợp với vị trí Senior AI Engineer tại VNG.',
      time: '10 phút trước',
      unread: true,
    },
    {
      id: 2,
      title: 'Tin tuyển dụng mới phù hợp',
      message: 'FPT Software vừa đăng tin Full-Stack Developer có 5 kỹ năng trùng khớp.',
      time: '1 giờ trước',
      unread: false,
    },
  ];

  return (
    <header className="sticky top-0 z-30 bg-white/90 backdrop-blur-md border-b border-slate-200/80 px-4 sm:px-8 py-3.5 flex items-center justify-between">
      {/* Left: Mobile hamburger & breadcrumbs */}
      <div className="flex items-center gap-3">
        <button
          onClick={onToggleSidebar}
          className="lg:hidden p-2 rounded-xl text-signal-navy hover:bg-slate-100 transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="hidden sm:flex items-center gap-2 text-xs text-signal-slate font-medium">
          <span className="font-heading font-semibold text-signal-navy">HireSense AI</span>
          <span>/</span>
          <span className="capitalize">{role} Portal</span>
        </div>
      </div>

      {/* Right: AI Engine status, Notifications, Role-based action */}
      <div className="flex items-center gap-3 sm:gap-4">
        {/* AI System Badge */}
        <div className="hidden md:inline-flex items-center gap-2 px-3 py-1 rounded-full bg-signal-offwhite border border-slate-200 text-xs text-signal-navy">
          <span className="w-2 h-2 rounded-full bg-signal-lime animate-pulse" />
          <span className="font-mono text-[11px] text-signal-slate">LLM:</span>
          <span className="font-semibold">Gemini 1.5 + pgvector</span>
        </div>

        {/* Notification Bell */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="p-2.5 rounded-full text-signal-navy hover:bg-slate-100 transition-colors relative"
          >
            <Bell className="w-5 h-5" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-signal-coral rounded-full ring-2 ring-white" />
          </button>

          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-2xl shadow-xl border border-slate-100 p-4 z-50">
              <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-3">
                <span className="font-heading font-bold text-sm text-signal-navy">Thông báo hệ thống</span>
                <span className="text-xs text-signal-slate cursor-pointer hover:text-signal-navy">Đánh dấu đã đọc</span>
              </div>
              <div className="space-y-3">
                {notifications.map((n) => (
                  <div key={n.id} className="p-3 rounded-xl bg-signal-offwhite border border-slate-100 text-xs space-y-1">
                    <div className="flex items-center justify-between font-semibold text-signal-navy">
                      <span>{n.title}</span>
                      <span className="text-[10px] text-slate-400 font-normal">{n.time}</span>
                    </div>
                    <p className="text-slate-600 leading-relaxed">{n.message}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Quick Action Button */}
        {role === 'candidate' && (
          <Button
            variant="lime"
            size="sm"
            icon={<Sparkles className="w-4 h-4 text-signal-navy" />}
            onClick={() => navigate('/candidate/cvs')}
          >
            Tải lên CV
          </Button>
        )}

        {role === 'recruiter' && (
          <Button
            variant="primary"
            size="sm"
            icon={<Plus className="w-4 h-4 text-signal-lime" />}
            onClick={() => navigate('/recruiter/jobs/new')}
          >
            Đăng tin JD mới
          </Button>
        )}

        {role === 'admin' && (
          <Button
            variant="lime"
            size="sm"
            icon={<CheckCircle className="w-4 h-4 text-signal-navy" />}
            onClick={() => navigate('/admin/moderation')}
          >
            Kiểm duyệt tin
          </Button>
        )}
      </div>
    </header>
  );
};

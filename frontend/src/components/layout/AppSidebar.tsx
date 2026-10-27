import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { UserRole } from '../../types';
import {
  LayoutDashboard,
  Search,
  FileText,
  Sparkles,
  Send,
  UserCheck,
  Briefcase,
  PlusCircle,
  Users,
  Building2,
  ShieldCheck,
  CheckSquare,
  BarChart3,
  LogOut,
  ChevronRight,
  ExternalLink
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onCloseMobile?: () => void;
}

export const AppSidebar: React.FC<SidebarProps> = ({ isOpen, onCloseMobile }) => {
  const { user, role, switchDemoRole, logout } = useAuth();
  const navigate = useNavigate();

  const candidateNav = [
    { label: 'Tổng quan (Dashboard)', path: '/candidate/dashboard', icon: LayoutDashboard },
    { label: 'Khám phá việc làm', path: '/candidate/jobs', icon: Search },
    { label: 'Hồ sơ & CV của tôi', path: '/candidate/cvs', icon: FileText },
    { label: 'Trung tâm So khớp AI', path: '/candidate/matching', icon: Sparkles, badge: 'AI' },
    { label: 'Đơn đã ứng tuyển', path: '/candidate/applications', icon: Send },
    { label: 'Hồ sơ cá nhân', path: '/candidate/profile', icon: UserCheck },
  ];

  const recruiterNav = [
    { label: 'Dashboard Tuyển dụng', path: '/recruiter/dashboard', icon: LayoutDashboard },
    { label: 'Quản lý Tin tuyển dụng', path: '/recruiter/jobs', icon: Briefcase },
    { label: 'Đăng tin JD mới', path: '/recruiter/jobs/new', icon: PlusCircle },
    { label: 'Xếp hạng Ứng viên', path: '/recruiter/applications', icon: Users, badge: 'AI' },
    { label: 'Hồ sơ Doanh nghiệp', path: '/recruiter/company', icon: Building2 },
  ];

  const adminNav = [
    { label: 'Dashboard Quản trị', path: '/admin/dashboard', icon: LayoutDashboard },
    { label: 'Kiểm duyệt Tin JD', path: '/admin/moderation', icon: CheckSquare, badge: 'Hot' },
    { label: 'Quản lý Người dùng', path: '/admin/users', icon: Users },
    { label: 'Quản lý Doanh nghiệp', path: '/admin/companies', icon: Building2 },
    { label: 'Báo cáo & Thống kê AI', path: '/admin/reports', icon: BarChart3 },
  ];

  const currentNav = role === 'admin' ? adminNav : role === 'recruiter' ? recruiterNav : candidateNav;

  const roleLabels: Record<UserRole, string> = {
    candidate: 'Ứng viên (Candidate)',
    recruiter: 'Nhà tuyển dụng (Recruiter)',
    admin: 'Quản trị viên (Admin)',
  };

  const handleRoleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const nextRole = e.target.value as UserRole;
    switchDemoRole(nextRole);
    if (nextRole === 'candidate') navigate('/candidate/dashboard');
    else if (nextRole === 'recruiter') navigate('/recruiter/dashboard');
    else if (nextRole === 'admin') navigate('/admin/dashboard');
  };

  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-signal-navy/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      {/* Sidebar container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 w-72 bg-signal-navy text-white z-50 flex flex-col justify-between border-r border-signal-navy-border transition-transform duration-300 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div>
          {/* Logo brand lockup */}
          <div className="p-6 pb-4 flex items-center justify-between border-b border-signal-navy-border">
            <NavLink to="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-signal-navy-light border border-signal-lime/40 flex items-center justify-center text-signal-lime group-hover:shadow-signal-glow transition-all">
                <Sparkles className="w-5 h-5 text-signal-lime" />
              </div>
              <div>
                <span className="font-heading font-bold text-lg tracking-tight text-white block leading-tight">
                  HireSense<span className="text-signal-lime font-mono">.AI</span>
                </span>
                <span className="text-[10px] text-signal-slate uppercase tracking-widest block font-medium">
                  SIGNAL Edition
                </span>
              </div>
            </NavLink>
          </div>

          {/* Role Switcher Pill (Quick demo switcher) */}
          <div className="px-6 py-4 border-b border-signal-navy-border bg-signal-navy-dark/40">
            <label className="text-[11px] font-semibold text-signal-slate uppercase tracking-wider block mb-1.5 flex items-center justify-between">
              <span>Đang đăng nhập với vai trò:</span>
              <span className="w-2 h-2 rounded-full bg-signal-lime animate-pulse" />
            </label>
            <select
              value={role}
              onChange={handleRoleChange}
              className="w-full bg-signal-navy-light text-white text-xs font-medium rounded-xl px-3 py-2 border border-signal-navy-border focus:outline-none focus:border-signal-lime cursor-pointer"
            >
              <option value="candidate">Ứng viên: Nguyễn Văn An</option>
              <option value="recruiter">Nhà tuyển dụng: VNG HR</option>
              <option value="admin">Quản trị viên: Hệ thống</option>
            </select>
          </div>

          {/* Navigation links */}
          <nav className="p-4 space-y-1.5 overflow-y-auto max-h-[calc(100vh-280px)]">
            <div className="px-3 pb-2 text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
              {roleLabels[role]}
            </div>

            {currentNav.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={onCloseMobile}
                  className={({ isActive }) =>
                    `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ${
                      isActive
                        ? 'bg-signal-lime text-signal-navy font-semibold shadow-sm'
                        : 'text-slate-300 hover:text-white hover:bg-signal-navy-light'
                    }`
                  }
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-4 h-4 shrink-0" />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-signal-navy-dark text-signal-lime border border-signal-navy-border">
                      {item.badge}
                    </span>
                  )}
                </NavLink>
              );
            })}

            <div className="pt-4 mt-4 border-t border-signal-navy-border px-3">
              <NavLink
                to="/"
                className="flex items-center justify-between text-xs text-slate-400 hover:text-signal-lime transition-colors py-2"
              >
                <span>Xem trang chủ khách (Landing)</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </NavLink>
            </div>
          </nav>
        </div>

        {/* User Card & Logout Footer */}
        <div className="p-4 border-t border-signal-navy-border bg-signal-navy-dark/70">
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3 overflow-hidden">
              <div className="w-9 h-9 rounded-full bg-signal-lime/20 text-signal-lime flex items-center justify-center font-bold text-sm shrink-0 border border-signal-lime/40">
                {user?.fullName.charAt(0) || 'U'}
              </div>
              <div className="overflow-hidden">
                <span className="font-semibold text-sm text-white block truncate">
                  {user?.fullName || 'Người dùng'}
                </span>
                <span className="text-xs text-slate-400 block truncate">
                  {user?.email || 'user@hiresense.ai'}
                </span>
              </div>
            </div>

            <button
              onClick={() => {
                logout();
                navigate('/login');
              }}
              title="Đăng xuất"
              className="p-2 rounded-xl text-slate-400 hover:text-signal-coral hover:bg-signal-navy-light transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
};

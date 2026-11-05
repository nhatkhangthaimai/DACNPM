import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { UserRole } from '../../types';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { Sparkles, Lock, Mail, ArrowRight, ShieldCheck, UserCheck, Building2, AlertCircle, CheckCircle2 } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, switchDemoRole, isDemoAllowed, authError, clearAuthError, forgotPassword } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [selectedRole, setSelectedRole] = useState<UserRole>('candidate');
  const [isLoading, setIsLoading] = useState(false);

  // Forgot Password Modal State
  const [showForgotModal, setShowForgotModal] = useState(false);
  const [forgotEmail, setForgotEmail] = useState('');
  const [forgotLoading, setForgotLoading] = useState(false);
  const [forgotResult, setForgotResult] = useState<{ success: boolean; message: string } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    clearAuthError();

    const success = await login(email, password, selectedRole);
    setIsLoading(false);

    if (success) {
      const savedUser = localStorage.getItem('hiresense_user');
      const role = savedUser ? JSON.parse(savedUser).role : selectedRole;
      if (role === 'admin') navigate('/admin/dashboard');
      else if (role === 'recruiter') navigate('/recruiter/dashboard');
      else navigate('/candidate/dashboard');
    }
  };

  const handleQuickDemoSelect = async (role: UserRole) => {
    setSelectedRole(role);
    const demoCreds: Record<UserRole, { email: string; path: string; name: string }> = {
      candidate: { email: 'nguyenvanan.ai@gmail.com', path: '/candidate/dashboard', name: 'Nguyễn Văn An' },
      recruiter: { email: 'hr.lead@vng.com.vn', path: '/recruiter/dashboard', name: 'Trần Minh Thu (VNG HR)' },
      admin: { email: 'admin@hiresense.ai', path: '/admin/dashboard', name: 'Lê Hoàng Long (Quản trị viên)' },
    };
    const cred = demoCreds[role];
    setEmail(cred.email);
    setPassword('password123');
    setIsLoading(true);
    clearAuthError();

    const ok = await login(cred.email, 'password123', role);
    setIsLoading(false);

    if (ok) {
      navigate(cred.path);
    } else {
      switchDemoRole(role);
      navigate(cred.path);
    }
  };

  const handleForgotPasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!forgotEmail) return;
    setForgotLoading(true);
    setForgotResult(null);
    const res = await forgotPassword(forgotEmail);
    setForgotLoading(false);
    setForgotResult(res);
  };

  return (
    <div className="min-h-screen bg-signal-offwhite flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <NavLink to="/" className="inline-flex items-center gap-2 mb-4">
          <div className="w-10 h-10 rounded-full bg-signal-navy flex items-center justify-center text-signal-lime">
            <Sparkles className="w-5 h-5" />
          </div>
          <span className="font-heading font-bold text-2xl text-signal-navy">HireSense.AI</span>
        </NavLink>
        <h2 className="font-heading text-3xl font-bold tracking-tight text-signal-navy">
          Đăng nhập vào Hệ thống
        </h2>
        <p className="mt-2 text-sm text-signal-slate">
          Chưa có tài khoản?{' '}
          <NavLink to="/register/candidate" className="font-semibold text-signal-navy hover:underline">
            Đăng ký ứng viên
          </NavLink>
          {' · '}
          <NavLink to="/register/recruiter" className="font-semibold text-signal-navy hover:underline">
            Đăng ký nhà tuyển dụng
          </NavLink>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-lg">
        {/* Quick Demo Selector Card: Luôn hiển thị tài khoản mẫu thử nghiệm */}
        <div className="bg-signal-navy text-white rounded-2xl p-5 mb-6 border border-signal-navy-border shadow-md">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <ShieldCheck className="w-4 h-4 text-signal-lime" />
              <span className="text-xs font-semibold text-signal-lime uppercase tracking-wider">
                Tài khoản Demo Mẫu (1-Click Login)
              </span>
            </div>
            <span className="text-[10px] bg-signal-lime/20 text-signal-lime border border-signal-lime/30 px-2 py-0.5 rounded font-mono font-semibold">
              SANDBOX READY
            </span>
          </div>
          <p className="text-xs text-slate-300 mb-4">
            Bấm trực tiếp vào vai trò để đăng nhập trải nghiệm ngay lập tức (Mật khẩu mặc định: <code className="text-signal-lime bg-signal-navy-light px-1.5 py-0.5 rounded font-mono">password123</code>):
          </p>
          <div className="grid grid-cols-3 gap-2.5">
            <button
              type="button"
              onClick={() => handleQuickDemoSelect('candidate')}
              className="p-3 rounded-xl bg-signal-navy-light text-center border border-signal-navy-border hover:border-signal-lime hover:bg-signal-navy-light/80 transition-all cursor-pointer group"
            >
              <UserCheck className="w-5 h-5 text-signal-lime mx-auto mb-1.5 group-hover:scale-110 transition-transform" />
              <span className="text-xs font-bold block text-white">Ứng viên</span>
              <span className="text-[10px] text-slate-300 block truncate">Nguyễn Văn An</span>
              <span className="text-[9px] text-slate-400 block truncate">nguyenvanan.ai@...</span>
            </button>
            <button
              type="button"
              onClick={() => handleQuickDemoSelect('recruiter')}
              className="p-3 rounded-xl bg-signal-navy-light text-center border border-signal-navy-border hover:border-signal-mint hover:bg-signal-navy-light/80 transition-all cursor-pointer group"
            >
              <Building2 className="w-5 h-5 text-signal-mint mx-auto mb-1.5 group-hover:scale-110 transition-transform" />
              <span className="text-xs font-bold block text-white">Tuyển dụng</span>
              <span className="text-[10px] text-slate-300 block truncate">VNG Corp HR</span>
              <span className="text-[9px] text-slate-400 block truncate">hr.lead@vng.com.vn</span>
            </button>
            <button
              type="button"
              onClick={() => handleQuickDemoSelect('admin')}
              className="p-3 rounded-xl bg-signal-navy-light text-center border border-signal-navy-border hover:border-signal-lavender hover:bg-signal-navy-light/80 transition-all cursor-pointer group"
            >
              <ShieldCheck className="w-5 h-5 text-signal-lavender mx-auto mb-1.5 group-hover:scale-110 transition-transform" />
              <span className="text-xs font-bold block text-white">Admin</span>
              <span className="text-[10px] text-slate-300 block truncate">Quản trị viên</span>
              <span className="text-[9px] text-slate-400 block truncate">admin@hiresense.ai</span>
            </button>
          </div>
        </div>

        {/* Regular Login Card */}
        <div className="bg-white py-8 px-6 shadow-sm rounded-3xl border border-slate-200 sm:px-10">
          {authError && (
            <div className="mb-5 p-3.5 bg-signal-coral/10 border border-signal-coral/30 rounded-2xl flex items-center gap-3 text-signal-coral text-xs">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <span>{authError}</span>
            </div>
          )}

          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
                Địa chỉ Email
              </label>
              <div className="relative">
                <Mail className="w-5 h-5 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@company.com"
                  className="w-full pl-11 pr-4 py-2.5 text-sm bg-signal-offwhite border border-slate-200 rounded-xl focus:outline-none focus:border-signal-navy focus:bg-white"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="block text-xs font-semibold uppercase text-signal-slate">
                  Mật khẩu
                </label>
                <button
                  type="button"
                  onClick={() => {
                    setForgotEmail(email);
                    setShowForgotModal(true);
                  }}
                  className="text-xs text-signal-navy hover:underline font-medium"
                >
                  Quên mật khẩu?
                </button>
              </div>
              <div className="relative">
                <Lock className="w-5 h-5 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-11 pr-4 py-2.5 text-sm bg-signal-offwhite border border-slate-200 rounded-xl focus:outline-none focus:border-signal-navy focus:bg-white"
                />
              </div>
            </div>

            <Button
              type="submit"
              variant="primary"
              size="lg"
              isLoading={isLoading}
              className="w-full mt-4"
              icon={<ArrowRight className="w-4 h-4" />}
            >
              Đăng nhập ngay
            </Button>

            {/* Quick credentials hint */}
            <div className="pt-4 border-t border-slate-100">
              <div className="flex items-center justify-between text-[11px] text-signal-slate mb-2">
                <span className="font-semibold text-slate-500 uppercase tracking-wider text-[10px]">
                  Tài khoản mẫu có sẵn (Mật khẩu: <span className="font-mono text-signal-navy font-bold">password123</span>):
                </span>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center text-xs">
                <button
                  type="button"
                  onClick={() => {
                    setEmail('nguyenvanan.ai@gmail.com');
                    setPassword('password123');
                    setSelectedRole('candidate');
                  }}
                  className="py-1.5 px-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-slate-700 font-medium transition-colors"
                >
                  Candidate
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setEmail('hr.lead@vng.com.vn');
                    setPassword('password123');
                    setSelectedRole('recruiter');
                  }}
                  className="py-1.5 px-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-slate-700 font-medium transition-colors"
                >
                  Recruiter
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setEmail('admin@hiresense.ai');
                    setPassword('password123');
                    setSelectedRole('admin');
                  }}
                  className="py-1.5 px-2 bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-lg text-slate-700 font-medium transition-colors"
                >
                  Admin
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>

      {/* Forgot Password Modal */}
      <Modal
        isOpen={showForgotModal}
        onClose={() => {
          setShowForgotModal(false);
          setForgotResult(null);
        }}
        title="Yêu cầu Đặt lại Mật khẩu"
        maxWidth="sm"
      >
        <div className="space-y-4">
          <p className="text-xs text-signal-slate">
            Nhập địa chỉ email đã đăng ký. Hệ thống sẽ tạo mã xác nhận có thời hạn 15 phút để bạn khôi phục quyền truy cập:
          </p>

          {forgotResult && (
            <div className={`p-3 rounded-xl text-xs flex items-center gap-2.5 ${
              forgotResult.success ? 'bg-signal-mint/10 border border-signal-mint/30 text-teal-800' : 'bg-signal-coral/10 border border-signal-coral/30 text-signal-coral'
            }`}>
              {forgotResult.success ? <CheckCircle2 className="w-4 h-4 shrink-0" /> : <AlertCircle className="w-4 h-4 shrink-0" />}
              <span>{forgotResult.message}</span>
            </div>
          )}

          <form onSubmit={handleForgotPasswordSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-signal-slate uppercase mb-1">
                Email nhận liên kết
              </label>
              <input
                type="email"
                required
                value={forgotEmail}
                onChange={(e) => setForgotEmail(e.target.value)}
                placeholder="email@example.com"
                className="w-full px-3.5 py-2.5 text-sm bg-signal-offwhite border border-slate-200 rounded-xl focus:outline-none focus:border-signal-navy"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => {
                  setShowForgotModal(false);
                  setForgotResult(null);
                }}
              >
                Đóng
              </Button>
              <Button
                type="submit"
                variant="primary"
                size="sm"
                isLoading={forgotLoading}
              >
                Gửi yêu cầu
              </Button>
            </div>
          </form>
        </div>
      </Modal>
    </div>
  );
};

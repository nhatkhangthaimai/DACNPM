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

    const success = await login(email, password, isDemoAllowed ? selectedRole : undefined);
    setIsLoading(false);

    if (success) {
      // Role is determined from user state or storage
      const savedUser = localStorage.getItem('hiresense_user');
      const role = savedUser ? JSON.parse(savedUser).role : selectedRole;
      if (role === 'admin') navigate('/admin/dashboard');
      else if (role === 'recruiter') navigate('/recruiter/dashboard');
      else navigate('/candidate/dashboard');
    }
  };

  const handleQuickDemoSelect = (role: UserRole) => {
    if (!isDemoAllowed) return;
    setSelectedRole(role);
    switchDemoRole(role);
    if (role === 'candidate') {
      setEmail('nguyenvanan.ai@gmail.com');
      navigate('/candidate/dashboard');
    } else if (role === 'recruiter') {
      setEmail('hr.lead@vng.com.vn');
      navigate('/recruiter/dashboard');
    } else if (role === 'admin') {
      setEmail('admin@hiresense.ai');
      navigate('/admin/dashboard');
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
        {/* Quick Demo Selector Card: ONLY visible in development mode */}
        {isDemoAllowed && (
          <div className="bg-signal-navy text-white rounded-2xl p-5 mb-6 border border-signal-navy-border shadow-md">
            <div className="flex items-center gap-2 mb-3">
              <ShieldCheck className="w-4 h-4 text-signal-lime" />
              <span className="text-xs font-semibold text-signal-lime uppercase tracking-wider">
                Môi trường Thử nghiệm (Demo Sandbox)
              </span>
            </div>
            <p className="text-xs text-slate-300 mb-4">
              Chế độ phát triển cục bộ: Nhấp vào vai trò để kiểm thử nhanh mà không cần nhập mật khẩu:
            </p>
            <div className="grid grid-cols-3 gap-2.5">
              <button
                type="button"
                onClick={() => handleQuickDemoSelect('candidate')}
                className="p-3 rounded-xl bg-signal-navy-light text-center border border-signal-navy-border hover:border-signal-lime transition-all"
              >
                <UserCheck className="w-5 h-5 text-signal-lime mx-auto mb-1.5" />
                <span className="text-xs font-bold block text-white">Ứng viên</span>
                <span className="text-[10px] text-slate-400">Nguyễn Văn An</span>
              </button>
              <button
                type="button"
                onClick={() => handleQuickDemoSelect('recruiter')}
                className="p-3 rounded-xl bg-signal-navy-light text-center border border-signal-navy-border hover:border-signal-lime transition-all"
              >
                <Building2 className="w-5 h-5 text-signal-mint mx-auto mb-1.5" />
                <span className="text-xs font-bold block text-white">Tuyển dụng</span>
                <span className="text-[10px] text-slate-400">VNG Corp HR</span>
              </button>
              <button
                type="button"
                onClick={() => handleQuickDemoSelect('admin')}
                className="p-3 rounded-xl bg-signal-navy-light text-center border border-signal-navy-border hover:border-signal-lime transition-all"
              >
                <ShieldCheck className="w-5 h-5 text-signal-lavender mx-auto mb-1.5" />
                <span className="text-xs font-bold block text-white">Admin</span>
                <span className="text-[10px] text-slate-400">Quản trị viên</span>
              </button>
            </div>
          </div>
        )}

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

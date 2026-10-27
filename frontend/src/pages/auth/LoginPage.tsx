import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { UserRole } from '../../types';
import { Button } from '../../components/ui/Button';
import { Sparkles, Lock, Mail, ArrowRight, ShieldCheck, UserCheck, Building2 } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, switchDemoRole } = useAuth();
  const [email, setEmail] = useState('nguyenvanan.ai@gmail.com');
  const [password, setPassword] = useState('password123');
  const [selectedRole, setSelectedRole] = useState<UserRole>('candidate');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    await login(email, password, selectedRole);
    setIsLoading(false);
    if (selectedRole === 'candidate') navigate('/candidate/dashboard');
    else if (selectedRole === 'recruiter') navigate('/recruiter/dashboard');
    else if (selectedRole === 'admin') navigate('/admin/dashboard');
  };

  const handleQuickDemoSelect = (role: UserRole) => {
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
          Hoặc{' '}
          <NavLink to="/register/candidate" className="font-semibold text-signal-navy hover:underline">
            tạo tài khoản ứng viên mới
          </NavLink>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-lg">
        {/* Quick Demo Selector Card */}
        <div className="bg-signal-navy text-white rounded-2xl p-5 mb-6 border border-signal-navy-border shadow-md">
          <div className="flex items-center gap-2 mb-3">
            <ShieldCheck className="w-4 h-4 text-signal-lime" />
            <span className="text-xs font-semibold text-signal-lime uppercase tracking-wider">
              Đăng nhập Nhanh Chế độ Demo
            </span>
          </div>
          <p className="text-xs text-slate-300 mb-4">
            Nhấp trực tiếp vào vai trò để kiểm thử toàn diện các luồng nghiệp vụ tương ứng:
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

        {/* Regular Login Card */}
        <div className="bg-white py-8 px-6 shadow-sm rounded-3xl border border-slate-200 sm:px-10">
          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
                Vai trò đăng nhập
              </label>
              <div className="grid grid-cols-3 gap-2">
                {(['candidate', 'recruiter', 'admin'] as UserRole[]).map((r) => (
                  <button
                    key={r}
                    type="button"
                    onClick={() => setSelectedRole(r)}
                    className={`py-2 text-xs font-bold rounded-xl border capitalize transition-all ${
                      selectedRole === r
                        ? 'bg-signal-navy text-white border-signal-navy'
                        : 'bg-signal-offwhite text-signal-slate border-slate-200 hover:border-slate-300'
                    }`}
                  >
                    {r === 'candidate' ? 'Ứng viên' : r === 'recruiter' ? 'Nhà tuyển dụng' : 'Quản trị'}
                  </button>
                ))}
              </div>
            </div>

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
              <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
                Mật khẩu
              </label>
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
    </div>
  );
};

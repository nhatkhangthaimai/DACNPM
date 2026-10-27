import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Button } from '../../components/ui/Button';
import { Sparkles, Mail, Lock, User, Building2, Phone, Globe, ArrowRight } from 'lucide-react';

export const RegisterRecruiterPage: React.FC = () => {
  const navigate = useNavigate();
  const { registerRecruiter } = useAuth();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    await registerRecruiter({
      fullName,
      email,
      companyName,
      phone,
    });
    setIsLoading(false);
    navigate('/recruiter/dashboard');
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
          Đăng ký Nhà tuyển dụng
        </h2>
        <p className="mt-2 text-sm text-signal-slate">
          Xây dựng đội ngũ nhân sự chất lượng cao cùng AI
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-lg">
        <div className="bg-white py-8 px-6 shadow-sm rounded-3xl border border-slate-200 sm:px-10">
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
                Tên Doanh nghiệp / Tổ chức
              </label>
              <div className="relative">
                <Building2 className="w-5 h-5 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  required
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  placeholder="VNG Corporation, FPT, v.v."
                  className="w-full pl-11 pr-4 py-2.5 text-sm bg-signal-offwhite border border-slate-200 rounded-xl focus:outline-none focus:border-signal-navy focus:bg-white"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
                Họ và Tên người đại diện tuyển dụng
              </label>
              <div className="relative">
                <User className="w-5 h-5 text-slate-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Trần Thị Lan (Talent Acquisition)"
                  className="w-full pl-11 pr-4 py-2.5 text-sm bg-signal-offwhite border border-slate-200 rounded-xl focus:outline-none focus:border-signal-navy focus:bg-white"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
                  Email Doanh nghiệp
                </label>
                <div className="relative">
                  <Mail className="w-5 h-5 text-slate-400 absolute left-3.5 top-3" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="hr@company.com"
                    className="w-full pl-11 pr-4 py-2.5 text-sm bg-signal-offwhite border border-slate-200 rounded-xl focus:outline-none focus:border-signal-navy focus:bg-white"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
                  Số điện thoại liên hệ
                </label>
                <div className="relative">
                  <Phone className="w-5 h-5 text-slate-400 absolute left-3.5 top-3" />
                  <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="028 1234 5678"
                    className="w-full pl-11 pr-4 py-2.5 text-sm bg-signal-offwhite border border-slate-200 rounded-xl focus:outline-none focus:border-signal-navy focus:bg-white"
                  />
                </div>
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
              icon={<ArrowRight className="w-4 h-4 text-signal-lime" />}
            >
              Đăng ký Nhà tuyển dụng
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

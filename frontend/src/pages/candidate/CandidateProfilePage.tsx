import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { User, Mail, Phone, MapPin, Briefcase, DollarSign, Globe, Code2, CheckCircle2 } from 'lucide-react';

export const CandidateProfilePage: React.FC = () => {
  const { user } = useAuth();
  const [fullName, setFullName] = useState(user?.fullName || 'Nguyễn Văn An');
  const [phone, setPhone] = useState('0908 123 456');
  const [title, setTitle] = useState('Senior AI / Machine Learning Engineer');
  const [location, setLocation] = useState('TP. Hồ Chí Minh');
  const [yearsExp, setYearsExp] = useState('3.5');
  const [expectedSalary, setExpectedSalary] = useState('50000000');
  const [bio, setBio] = useState('Kỹ sư AI đam mê nghiên cứu và ứng dụng thực tiễn các mô hình ngôn ngữ lớn (LLMs), RAG và kiến trúc microservices.');
  const [github, setGithub] = useState('https://github.com/nguyenvanan-ai');
  const [linkedin, setLinkedin] = useState('https://linkedin.com/in/nguyenvanan-ai');
  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <PageHeader
        title="Hồ sơ Cá nhân & Thiết lập Tài khoản"
        subtitle="Thông tin này sẽ được đồng bộ với hồ sơ ứng tuyển và thuật toán đề xuất việc làm AI."
      />

      <form onSubmit={handleSave} className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/80 shadow-sm space-y-6">
        {savedSuccess && (
          <div className="flex items-center gap-2 p-4 rounded-2xl bg-emerald-50 text-emerald-800 text-sm border border-emerald-200">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>Đã cập nhật hồ sơ cá nhân thành công!</span>
          </div>
        )}

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Họ và Tên
            </label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Địa chỉ Email
            </label>
            <input
              type="email"
              disabled
              value={user?.email || 'nguyenvanan.ai@gmail.com'}
              className="w-full bg-slate-100 text-slate-500 text-sm rounded-xl px-4 py-2.5 border border-slate-200 cursor-not-allowed"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Số điện thoại
            </label>
            <input
              type="tel"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Vị trí / Chức danh chuyên môn
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Địa điểm làm việc mong muốn
            </label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Mức lương kỳ vọng (VND/tháng)
            </label>
            <input
              type="number"
              value={expectedSalary}
              onChange={(e) => setExpectedSalary(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
            Giới thiệu ngắn về bản thân (Bio)
          </label>
          <textarea
            rows={3}
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            className="w-full bg-signal-offwhite text-sm rounded-xl p-3 border border-slate-200 focus:outline-none focus:border-signal-navy"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 pt-2">
          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1 flex items-center gap-1.5">
              <Code2 className="w-4 h-4" /> GitHub Profile
            </label>
            <input
              type="url"
              value={github}
              onChange={(e) => setGithub(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1 flex items-center gap-1.5">
              <Globe className="w-4 h-4" /> LinkedIn Profile
            </label>
            <input
              type="url"
              value={linkedin}
              onChange={(e) => setLinkedin(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>
        </div>

        <div className="pt-6 border-t border-slate-100 flex justify-end">
          <Button type="submit" variant="primary">
            Lưu thay đổi hồ sơ
          </Button>
        </div>
      </form>
    </div>
  );
};

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { Code2, Globe, CheckCircle2 } from 'lucide-react';

interface ProfileData {
  fullName: string;
  phone: string;
  title: string;
  location: string;
  expectedSalary: string;
  bio: string;
  github: string;
  linkedin: string;
}

export const CandidateProfilePage: React.FC = () => {
  const { user } = useAuth();
  const storageKey = `hiresense_profile_${user?.id || 'default'}`;

  const loadProfile = (): ProfileData => {
    const saved = localStorage.getItem(storageKey);
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        // fall through to defaults
      }
    }
    // Lần đầu: lấy thông tin cơ bản từ user auth, còn lại để trống
    return {
      fullName: user?.fullName || '',
      phone: user?.phone || '',
      title: '',
      location: '',
      expectedSalary: '',
      bio: '',
      github: '',
      linkedin: '',
    };
  };

  const [profile, setProfile] = useState<ProfileData>(loadProfile);
  const [savedSuccess, setSavedSuccess] = useState(false);

  // Khi user thay đổi (switch account) thì tải lại profile
  useEffect(() => {
    setProfile(loadProfile());
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.id]);

  const handleChange = (field: keyof ProfileData, value: string) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    localStorage.setItem(storageKey, JSON.stringify(profile));
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 3000);
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
              value={profile.fullName}
              onChange={(e) => handleChange('fullName', e.target.value)}
              placeholder="Nhập họ và tên đầy đủ"
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
              value={user?.email || ''}
              className="w-full bg-slate-100 text-slate-500 text-sm rounded-xl px-4 py-2.5 border border-slate-200 cursor-not-allowed"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Số điện thoại
            </label>
            <input
              type="tel"
              value={profile.phone}
              onChange={(e) => handleChange('phone', e.target.value)}
              placeholder="Nhập số điện thoại"
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Vị trí / Chức danh chuyên môn
            </label>
            <input
              type="text"
              value={profile.title}
              onChange={(e) => handleChange('title', e.target.value)}
              placeholder="Ví dụ: Frontend Developer"
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Địa điểm làm việc mong muốn
            </label>
            <input
              type="text"
              value={profile.location}
              onChange={(e) => handleChange('location', e.target.value)}
              placeholder="Ví dụ: Đà Nẵng, TP.HCM"
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Mức lương kỳ vọng (VND/tháng)
            </label>
            <input
              type="number"
              value={profile.expectedSalary}
              onChange={(e) => handleChange('expectedSalary', e.target.value)}
              placeholder="Ví dụ: 15000000"
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
            value={profile.bio}
            onChange={(e) => handleChange('bio', e.target.value)}
            placeholder="Mô tả ngắn về kinh nghiệm, thế mạnh và định hướng nghề nghiệp của bạn..."
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
              value={profile.github}
              onChange={(e) => handleChange('github', e.target.value)}
              placeholder="https://github.com/username"
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1 flex items-center gap-1.5">
              <Globe className="w-4 h-4" /> LinkedIn Profile
            </label>
            <input
              type="url"
              value={profile.linkedin}
              onChange={(e) => handleChange('linkedin', e.target.value)}
              placeholder="https://linkedin.com/in/username"
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

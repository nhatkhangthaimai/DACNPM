import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../../context/AuthContext';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { Code2, Globe, CheckCircle2, Camera, Image as ImageIcon, Loader2, User as UserIcon } from 'lucide-react';
import { apiService } from '../../services/api';

interface ProfileData {
  fullName: string;
  phone: string;
  title: string;
  location: string;
  expectedSalary: string;
  bio: string;
  github: string;
  linkedin: string;
  avatarUrl?: string;
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
    return {
      fullName: user?.fullName || '',
      phone: user?.phone || '',
      title: '',
      location: '',
      expectedSalary: '',
      bio: '',
      github: '',
      linkedin: '',
      avatarUrl: '',
    };
  };

  const [profile, setProfile] = useState<ProfileData>(loadProfile);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [isUploadingAvatar, setIsUploadingAvatar] = useState(false);
  const [avatarError, setAvatarError] = useState<string | null>(null);

  const photoInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    setProfile(loadProfile());
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.id]);

  const handleChange = (field: keyof ProfileData, value: string) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  const handleAvatarFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    e.target.value = '';

    setAvatarError(null);
    if (!file.type.startsWith('image/') && !file.name.match(/\.(jpg|jpeg|png|webp|heic|heif)$/i)) {
      setAvatarError('Định dạng không được hỗ trợ. Vui lòng chọn ảnh JPG, PNG, WEBP hoặc HEIC.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setAvatarError('Kích thước ảnh đại diện vượt quá 5MB.');
      return;
    }

    setIsUploadingAvatar(true);
    try {
      const uploadedUrl = await apiService.uploadAvatar(file, user?.id);
      setProfile(prev => {
        const next = { ...prev, avatarUrl: uploadedUrl };
        localStorage.setItem(storageKey, JSON.stringify(next));
        return next;
      });
    } catch {
      setAvatarError('Không thể tải lên ảnh đại diện. Vui lòng thử lại.');
    } finally {
      setIsUploadingAvatar(false);
    }
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

      {/* Hidden Inputs for Avatar Mobile Selection */}
      <input
        ref={photoInputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp,image/heic,.jpg,.jpeg,.png,.webp,.heic,.heif"
        onChange={handleAvatarFile}
        className="hidden"
      />
      <input
        ref={cameraInputRef}
        type="file"
        accept="image/*"
        capture="user"
        onChange={handleAvatarFile}
        className="hidden"
      />

      <form onSubmit={handleSave} className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/80 shadow-sm space-y-6">
        {savedSuccess && (
          <div className="flex items-center gap-2 p-4 rounded-2xl bg-emerald-50 text-emerald-800 text-sm border border-emerald-200">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>Đã cập nhật hồ sơ cá nhân thành công!</span>
          </div>
        )}

        {/* Avatar Upload Section */}
        <div className="p-5 rounded-2xl bg-signal-offwhite/80 border border-slate-200 flex flex-col sm:flex-row items-center gap-5">
          <div className="relative">
            <div className="w-24 h-24 rounded-full overflow-hidden border-2 border-signal-lime bg-slate-200 flex items-center justify-center shadow-md">
              {profile.avatarUrl ? (
                <img 
                  src={profile.avatarUrl} 
                  alt={profile.fullName || 'Ảnh đại diện'} 
                  className="w-full h-full object-cover" 
                />
              ) : (
                <UserIcon className="w-12 h-12 text-slate-400" />
              )}
            </div>
            {isUploadingAvatar && (
              <div className="absolute inset-0 rounded-full bg-signal-navy/60 flex items-center justify-center">
                <Loader2 className="w-6 h-6 text-signal-lime animate-spin" />
              </div>
            )}
          </div>

          <div className="flex-1 text-center sm:text-left space-y-2">
            <div>
              <h4 className="text-sm font-heading font-semibold text-signal-navy">Ảnh đại diện hồ sơ</h4>
              <p className="text-xs text-signal-slate">
                Hỗ trợ tải từ thư viện ảnh điện thoại hoặc chụp camera (JPG, PNG, WEBP, HEIC tối đa 5MB)
              </p>
            </div>

            <div className="flex flex-wrap gap-2 justify-center sm:justify-start">
              <button
                type="button"
                onClick={() => photoInputRef.current?.click()}
                disabled={isUploadingAvatar}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 hover:border-signal-navy text-xs font-semibold text-signal-navy shadow-sm hover:bg-slate-50 transition-colors"
              >
                <ImageIcon className="w-3.5 h-3.5 text-emerald-600" />
                <span>Thư viện ảnh điện thoại</span>
              </button>

              <button
                type="button"
                onClick={() => cameraInputRef.current?.click()}
                disabled={isUploadingAvatar}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 hover:border-signal-navy text-xs font-semibold text-signal-navy shadow-sm hover:bg-slate-50 transition-colors"
              >
                <Camera className="w-3.5 h-3.5 text-amber-600" />
                <span>Chụp ảnh mới</span>
              </button>
            </div>

            {avatarError && (
              <p className="text-xs text-rose-600 font-medium">{avatarError}</p>
            )}
          </div>
        </div>

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

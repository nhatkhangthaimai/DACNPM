import React, { useState, useEffect, useRef } from 'react';
import { apiService } from '../../services/api';
import { Company } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { Building2, Globe, MapPin, Users, CheckCircle2, Image as ImageIcon, Camera, Loader2 } from 'lucide-react';

export const CompanyProfilePage: React.FC = () => {
  const [company, setCompany] = useState<Company | null>(null);
  const [name, setName] = useState('VNG Corporation');
  const [website, setWebsite] = useState('https://vng.com.vn');
  const [industry, setIndustry] = useState('Technology & Gaming');
  const [companySize, setCompanySize] = useState('1000+ nhân viên');
  const [address, setAddress] = useState('Z06 Đường số 13, Tân Thuận Đông, Quận 7, TP.HCM');
  const [description, setDescription] = useState('Kỳ lân công nghệ đầu tiên tại Việt Nam, tiên phong trong mảng game trực tuyến, thanh toán số ZaloPay và nền tảng AI.');
  const [logoUrl, setLogoUrl] = useState<string>('');
  const [isUploadingLogo, setIsUploadingLogo] = useState(false);
  const [logoError, setLogoError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  const logoInputRef = useRef<HTMLInputElement>(null);
  const logoCameraRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    apiService.getCompanies().then(comps => {
      if (comps.length > 0) {
        setCompany(comps[0]);
        setName(comps[0].name);
        setWebsite(comps[0].website || '');
        setIndustry(comps[0].industry);
        setCompanySize(comps[0].companySize);
        setAddress(comps[0].address);
        setDescription(comps[0].description);
        setLogoUrl(comps[0].logoUrl || '');
      }
    });
  }, []);

  const handleLogoUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    e.target.value = '';

    setLogoError(null);
    if (!file.type.startsWith('image/') && !file.name.match(/\.(jpg|jpeg|png|webp|heic|heif)$/i)) {
      setLogoError('Định dạng không được hỗ trợ. Vui lòng chọn ảnh JPG, PNG, WEBP hoặc HEIC.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setLogoError('Kích thước logo vượt quá 5MB.');
      return;
    }

    setIsUploadingLogo(true);
    try {
      const uploadedUrl = await apiService.uploadCompanyLogo(file, company?.id);
      setLogoUrl(uploadedUrl);
    } catch {
      setLogoError('Không thể tải lên logo công ty. Vui lòng thử lại.');
    } finally {
      setIsUploadingLogo(false);
    }
  };

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <PageHeader
        title="Hồ sơ Doanh nghiệp"
        subtitle="Thông tin doanh nghiệp sẽ được hiển thị công khai trên các tin tuyển dụng và trang thương hiệu nhà tuyển dụng."
      />

      {/* Hidden Inputs for Logo Upload */}
      <input
        ref={logoInputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp,image/heic,.jpg,.jpeg,.png,.webp,.heic,.heif"
        onChange={handleLogoUpload}
        className="hidden"
      />
      <input
        ref={logoCameraRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleLogoUpload}
        className="hidden"
      />

      <form onSubmit={handleSave} className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/80 shadow-sm space-y-6">
        {saved && (
          <div className="flex items-center gap-2 p-4 rounded-2xl bg-emerald-50 text-emerald-800 text-sm border border-emerald-200">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>Đã cập nhật thông tin doanh nghiệp thành công!</span>
          </div>
        )}

        {/* Company Logo Upload Section */}
        <div className="p-5 rounded-2xl bg-signal-offwhite/80 border border-slate-200 flex flex-col sm:flex-row items-center gap-5">
          <div className="relative">
            <div className="w-24 h-24 rounded-2xl overflow-hidden border-2 border-signal-lime bg-white flex items-center justify-center shadow-md p-2">
              {logoUrl ? (
                <img 
                  src={logoUrl} 
                  alt={name || 'Logo công ty'} 
                  className="w-full h-full object-contain" 
                />
              ) : (
                <Building2 className="w-10 h-10 text-signal-navy/40" />
              )}
            </div>
            {isUploadingLogo && (
              <div className="absolute inset-0 rounded-2xl bg-signal-navy/60 flex items-center justify-center">
                <Loader2 className="w-6 h-6 text-signal-lime animate-spin" />
              </div>
            )}
          </div>

          <div className="flex-1 text-center sm:text-left space-y-2">
            <div>
              <h4 className="text-sm font-heading font-semibold text-signal-navy">Logo Thương hiệu Doanh nghiệp</h4>
              <p className="text-xs text-signal-slate">
                Chọn ảnh logo từ thư viện ảnh điện thoại hoặc máy tính (JPG, PNG, WEBP tối đa 5MB)
              </p>
            </div>

            <div className="flex flex-wrap gap-2 justify-center sm:justify-start">
              <button
                type="button"
                onClick={() => logoInputRef.current?.click()}
                disabled={isUploadingLogo}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 hover:border-signal-navy text-xs font-semibold text-signal-navy shadow-sm hover:bg-slate-50 transition-colors"
              >
                <ImageIcon className="w-3.5 h-3.5 text-emerald-600" />
                <span>Thư viện ảnh điện thoại</span>
              </button>

              <button
                type="button"
                onClick={() => logoCameraRef.current?.click()}
                disabled={isUploadingLogo}
                className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-white border border-slate-200 hover:border-signal-navy text-xs font-semibold text-signal-navy shadow-sm hover:bg-slate-50 transition-colors"
              >
                <Camera className="w-3.5 h-3.5 text-amber-600" />
                <span>Chụp ảnh Logo</span>
              </button>
            </div>

            {logoError && (
              <p className="text-xs text-rose-600 font-medium">{logoError}</p>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Tên Doanh nghiệp
            </label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-signal-offwhite text-sm font-semibold rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Website chính thức
            </label>
            <input
              type="url"
              value={website}
              onChange={(e) => setWebsite(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Lĩnh vực hoạt động
            </label>
            <input
              type="text"
              value={industry}
              onChange={(e) => setIndustry(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
              Quy mô nhân sự
            </label>
            <input
              type="text"
              value={companySize}
              onChange={(e) => setCompanySize(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
            Địa chỉ trụ sở chính
          </label>
          <input
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold uppercase text-signal-slate mb-1">
            Giới thiệu về doanh nghiệp (Văn hóa & Tầm nhìn)
          </label>
          <textarea
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full bg-signal-offwhite text-sm rounded-xl p-3 border border-slate-200 focus:outline-none focus:border-signal-navy"
          />
        </div>

        <div className="pt-6 border-t border-slate-100 flex justify-end">
          <Button type="submit" variant="primary">
            Lưu thay đổi hồ sơ doanh nghiệp
          </Button>
        </div>
      </form>
    </div>
  );
};

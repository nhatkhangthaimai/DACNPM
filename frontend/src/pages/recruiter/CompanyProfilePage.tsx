import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import { Company } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { Building2, Globe, MapPin, Users, CheckCircle2 } from 'lucide-react';

export const CompanyProfilePage: React.FC = () => {
  const [company, setCompany] = useState<Company | null>(null);
  const [name, setName] = useState('VNG Corporation');
  const [website, setWebsite] = useState('https://vng.com.vn');
  const [industry, setIndustry] = useState('Technology & Gaming');
  const [companySize, setCompanySize] = useState('1000+ nhân viên');
  const [address, setAddress] = useState('Z06 Đường số 13, Tân Thuận Đông, Quận 7, TP.HCM');
  const [description, setDescription] = useState('Kỳ lân công nghệ đầu tiên tại Việt Nam, tiên phong trong mảng game trực tuyến, thanh toán số ZaloPay và nền tảng AI.');
  const [saved, setSaved] = useState(false);

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
      }
    });
  }, []);

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

      <form onSubmit={handleSave} className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/80 shadow-sm space-y-6">
        {saved && (
          <div className="flex items-center gap-2 p-4 rounded-2xl bg-emerald-50 text-emerald-800 text-sm border border-emerald-200">
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
            <span>Đã cập nhật thông tin doanh nghiệp thành công!</span>
          </div>
        )}

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

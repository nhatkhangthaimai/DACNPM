import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import { Company } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { StatusBadge } from '../../components/ui/SkillBadge';
import { Building2, Globe, MapPin, Users, CheckCircle2, XCircle } from 'lucide-react';

export const AdminCompanies: React.FC = () => {
  const [companies, setCompanies] = useState<Company[]>([]);

  useEffect(() => {
    apiService.getCompanies().then(setCompanies);
  }, []);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Quản lý Doanh nghiệp Đối tác"
        subtitle="Danh sách các công ty và tập đoàn công nghệ đăng ký sử dụng nền tảng HireSense AI."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {companies.map((comp) => (
          <div
            key={comp.id}
            className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-sm flex flex-col justify-between"
          >
            <div>
              <div className="flex items-start justify-between gap-4 mb-4">
                <img
                  src={comp.logoUrl}
                  alt={comp.name}
                  className="w-14 h-14 rounded-2xl object-cover border border-slate-100"
                />
                <StatusBadge status={comp.status} />
              </div>

              <h4 className="font-heading font-bold text-lg text-signal-navy mb-1">
                {comp.name}
              </h4>
              <span className="text-xs font-semibold text-signal-slate block mb-3">
                {comp.industry} · {comp.companySize}
              </span>

              <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed mb-4">
                {comp.description}
              </p>

              <div className="space-y-1.5 text-xs text-signal-slate pt-3 border-t border-slate-100">
                <div className="flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                  <span className="truncate">{comp.address}</span>
                </div>
                {comp.website && (
                  <div className="flex items-center gap-1.5">
                    <Globe className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <a
                      href={comp.website}
                      target="_blank"
                      rel="noreferrer"
                      className="text-signal-navy hover:underline truncate"
                    >
                      {comp.website}
                    </a>
                  </div>
                )}
              </div>
            </div>

            <div className="pt-4 border-t border-slate-100 mt-4 flex justify-end">
              <Button variant="outline" size="sm">
                Chi tiết đối tác
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

import React from 'react';
import { Job } from '../../types';
import { SkillBadge, StatusBadge } from './SkillBadge';
import { Button } from './Button';
import { MapPin, Briefcase, DollarSign, Sparkles, Building2 } from 'lucide-react';

interface JobCardProps {
  job: Job;
  matchScore?: number;
  onApply?: (job: Job) => void;
  onViewDetails?: (job: Job) => void;
  onCheckMatch?: (job: Job) => void;
}

export const JobCard: React.FC<JobCardProps> = ({
  job,
  matchScore,
  onApply,
  onViewDetails,
  onCheckMatch,
}) => {
  const formatSalary = (min?: number, max?: number, currency = 'VND') => {
    if (!min && !max) return 'Thoả thuận';
    if (currency === 'VND') {
      const minM = min ? `${(min / 1000000).toFixed(0)}Tr` : '';
      const maxM = max ? `${(max / 1000000).toFixed(0)}Tr` : '';
      if (minM && maxM) return `${minM} - ${maxM} VND`;
      return `${minM || maxM} VND`;
    }
    return `$${min || 0} - $${max || 0}`;
  };

  const jobTypeLabels: Record<string, string> = {
    full_time: 'Toàn thời gian',
    part_time: 'Bán thời gian',
    remote: 'Làm việc từ xa',
    hybrid: 'Hybrid (Linh hoạt)',
    internship: 'Thực tập sinh',
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm hover:shadow-md hover:border-slate-300 transition-all duration-200 flex flex-col justify-between">
      <div>
        {/* Top Header: Company & Title & Status */}
        <div className="flex items-start justify-between gap-4 mb-4">
          <div className="flex items-center gap-3.5">
            {job.companyLogo ? (
              <img
                src={job.companyLogo}
                alt={job.companyName}
                className="w-12 h-12 rounded-xl object-cover border border-slate-100"
              />
            ) : (
              <div className="w-12 h-12 rounded-xl bg-signal-navy text-signal-lime flex items-center justify-center font-bold text-lg">
                <Building2 className="w-6 h-6" />
              </div>
            )}
            <div>
              <span className="text-xs font-semibold text-signal-slate uppercase tracking-wider block">
                {job.companyName}
              </span>
              <h4
                onClick={() => onViewDetails?.(job)}
                className="font-heading font-bold text-lg text-signal-navy hover:text-signal-navy-light cursor-pointer line-clamp-1 transition-colors"
              >
                {job.title}
              </h4>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {matchScore !== undefined && (
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-signal-lime/20 border border-signal-lime/40 text-xs font-bold text-signal-navy">
                <Sparkles className="w-3.5 h-3.5 text-signal-navy" />
                <span>{matchScore}% Match</span>
              </div>
            )}
            <StatusBadge status={job.status} />
          </div>
        </div>

        {/* Quick Meta: Location, Type, Salary */}
        <div className="flex flex-wrap items-center gap-y-2 gap-x-4 text-xs text-signal-slate mb-4">
          <span className="inline-flex items-center gap-1">
            <MapPin className="w-3.5 h-3.5 text-slate-400" />
            {job.location}
          </span>
          <span className="inline-flex items-center gap-1">
            <Briefcase className="w-3.5 h-3.5 text-slate-400" />
            {jobTypeLabels[job.jobType] || job.jobType}
          </span>
          <span className="inline-flex items-center gap-1 font-semibold text-emerald-700">
            <DollarSign className="w-3.5 h-3.5 text-emerald-600" />
            {formatSalary(job.salaryMin, job.salaryMax, job.currency)}
          </span>
        </div>

        {/* Short description */}
        <p className="text-sm text-slate-600 line-clamp-2 mb-4 leading-relaxed">
          {job.description}
        </p>

        {/* Required Skills tags */}
        <div className="flex flex-wrap gap-1.5 mb-6">
          {job.requiredSkills.slice(0, 4).map((skill, idx) => (
            <SkillBadge key={idx} name={skill} size="sm" variant="default" />
          ))}
          {job.requiredSkills.length > 4 && (
            <span className="text-xs text-slate-400 self-center px-1">
              +{job.requiredSkills.length - 4} kỹ năng
            </span>
          )}
        </div>
      </div>

      {/* Footer Action buttons */}
      <div className="flex items-center justify-between gap-3 pt-4 border-t border-slate-100">
        <Button
          variant="outline"
          size="sm"
          onClick={() => onViewDetails?.(job)}
        >
          Chi tiết JD
        </Button>

        <div className="flex items-center gap-2">
          {onCheckMatch && (
            <Button
              variant="soft"
              size="sm"
              icon={<Sparkles className="w-3.5 h-3.5 text-signal-navy" />}
              onClick={() => onCheckMatch(job)}
            >
              So khớp AI
            </Button>
          )}

          {onApply && (
            <Button
              variant="lime"
              size="sm"
              onClick={() => onApply(job)}
            >
              Ứng tuyển ngay
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

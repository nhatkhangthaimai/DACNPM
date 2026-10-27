import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: {
    value: string;
    isPositive: boolean;
  };
  variant?: 'white' | 'navy' | 'lime' | 'lavender';
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  variant = 'white',
}) => {
  const isNavy = variant === 'navy';
  const isLime = variant === 'lime';
  const isLavender = variant === 'lavender';

  let containerClass = 'bg-white text-signal-navy border border-slate-200/80 shadow-sm';
  let iconClass = 'bg-signal-offwhite text-signal-navy';

  if (isNavy) {
    containerClass = 'bg-signal-navy text-white border border-signal-navy-border shadow-md';
    iconClass = 'bg-signal-navy-light text-signal-lime';
  } else if (isLime) {
    containerClass = 'bg-signal-lime text-signal-navy border border-signal-lime-hover shadow-sm';
    iconClass = 'bg-white/80 text-signal-navy';
  } else if (isLavender) {
    containerClass = 'bg-signal-lavender/20 text-signal-navy border border-signal-lavender/40 shadow-sm';
    iconClass = 'bg-white text-[#5942be]';
  }

  return (
    <div className={`p-6 rounded-2xl transition-all duration-200 hover:-translate-y-0.5 ${containerClass}`}>
      <div className="flex items-center justify-between mb-4">
        <span className={`text-sm font-medium ${isNavy ? 'text-slate-300' : 'text-signal-slate'}`}>
          {title}
        </span>
        <div className={`p-2.5 rounded-xl ${iconClass}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div className="flex items-baseline justify-between">
        <span className="font-heading text-3xl font-bold tracking-tight">
          {value}
        </span>

        {trend && (
          <span
            className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
              trend.isPositive
                ? isNavy
                  ? 'bg-signal-lime/20 text-signal-lime'
                  : 'bg-emerald-100 text-emerald-700'
                : 'bg-rose-100 text-rose-700'
            }`}
          >
            {trend.isPositive ? '↑' : '↓'} {trend.value}
          </span>
        )}
      </div>

      {subtitle && (
        <p className={`text-xs mt-2 ${isNavy ? 'text-slate-400' : 'text-signal-slate'}`}>
          {subtitle}
        </p>
      )}
    </div>
  );
};

import React from 'react';

interface SkillBadgeProps {
  name: string;
  variant?: 'default' | 'matched' | 'missing-required' | 'missing-preferred' | 'lavender';
  size?: 'sm' | 'md';
  onRemove?: () => void;
}

export const SkillBadge: React.FC<SkillBadgeProps> = ({
  name,
  variant = 'default',
  size = 'md',
  onRemove,
}) => {
  const sizeClasses = size === 'sm' ? 'px-2.5 py-0.5 text-xs' : 'px-3.5 py-1 text-sm';

  const variantStyles = {
    default: 'bg-signal-offwhite text-signal-navy border border-slate-200 hover:border-slate-300',
    matched: 'bg-signal-mint/15 text-[#1b7a66] border border-signal-mint/40 font-medium',
    'missing-required': 'bg-signal-coral/15 text-[#b8381d] border border-signal-coral/40 font-medium',
    'missing-preferred': 'bg-signal-gold/15 text-[#9e6912] border border-signal-gold/40 font-medium',
    lavender: 'bg-signal-lavender/15 text-[#5942be] border border-signal-lavender/40 font-medium',
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full transition-all duration-150 ${sizeClasses} ${variantStyles[variant]}`}
    >
      {variant === 'matched' && <span className="w-1.5 h-1.5 rounded-full bg-signal-mint-dark" />}
      {variant === 'missing-required' && <span className="w-1.5 h-1.5 rounded-full bg-signal-coral-dark" />}
      {variant === 'missing-preferred' && <span className="w-1.5 h-1.5 rounded-full bg-signal-gold-dark" />}
      {variant === 'lavender' && <span className="w-1.5 h-1.5 rounded-full bg-signal-lavender-dark" />}
      <span>{name}</span>
      {onRemove && (
        <button
          type="button"
          onClick={onRemove}
          className="ml-1 text-slate-400 hover:text-slate-600 focus:outline-none"
        >
          ×
        </button>
      )}
    </span>
  );
};

export const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
  const getBadgeConfig = (st: string) => {
    switch (st.toLowerCase()) {
      case 'published':
      case 'approved':
      case 'offered':
      case 'completed':
        return {
          bg: 'bg-signal-mint/15 text-[#1a705e] border-signal-mint/30',
          dot: 'bg-signal-mint',
          label: st === 'published' ? 'Đang tuyển' : st === 'approved' ? 'Đã duyệt' : st === 'offered' ? 'Mời nhận việc' : 'Hoàn thành'
        };
      case 'pending_approval':
      case 'pending':
      case 'submitted':
      case 'reviewing':
        return {
          bg: 'bg-signal-gold/15 text-[#9e6912] border-signal-gold/30',
          dot: 'bg-signal-gold',
          label: st === 'pending_approval' ? 'Chờ duyệt' : st === 'reviewing' ? 'Đang xét duyệt' : 'Mới nộp'
        };
      case 'shortlisted':
      case 'interviewed':
        return {
          bg: 'bg-signal-lavender/20 text-[#5942be] border-signal-lavender/40',
          dot: 'bg-signal-lavender',
          label: st === 'shortlisted' ? 'Lọt phỏng vấn' : 'Đã phỏng vấn'
        };
      case 'closed':
      case 'rejected':
      case 'failed':
        return {
          bg: 'bg-signal-coral/15 text-[#b8381d] border-signal-coral/30',
          dot: 'bg-signal-coral',
          label: st === 'closed' ? 'Đã đóng' : st === 'rejected' ? 'Từ chối' : 'Thất bại'
        };
      default:
        return {
          bg: 'bg-slate-100 text-slate-600 border-slate-200',
          dot: 'bg-slate-400',
          label: st
        };
    }
  };

  const config = getBadgeConfig(status);

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${config.bg}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${config.dot}`} />
      {config.label}
    </span>
  );
};

import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'lime' | 'outline' | 'soft' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  icon?: React.ReactNode;
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  icon,
  isLoading = false,
  className = '',
  disabled,
  ...props
}) => {
  const sizeStyles = {
    sm: 'px-3.5 py-1.5 text-xs font-semibold gap-1.5',
    md: 'px-5 py-2.5 text-sm font-semibold gap-2',
    lg: 'px-7 py-3 text-base font-semibold gap-2.5',
  };

  const variantStyles = {
    primary: 'bg-signal-navy text-white hover:bg-signal-navy-light shadow-sm active:scale-[0.98]',
    lime: 'bg-signal-lime text-signal-navy hover:bg-signal-lime-hover shadow-signal-glow active:scale-[0.98]',
    outline: 'bg-white text-signal-navy border border-slate-200 hover:border-signal-navy/40 hover:bg-slate-50/50 active:scale-[0.98]',
    soft: 'bg-slate-100 text-signal-navy hover:bg-slate-200/80 active:scale-[0.98]',
    danger: 'bg-signal-coral text-white hover:bg-signal-coral-dark shadow-sm active:scale-[0.98]',
    ghost: 'bg-transparent text-signal-slate hover:text-signal-navy hover:bg-slate-100/70',
  };

  return (
    <button
      disabled={disabled || isLoading}
      className={`inline-flex items-center justify-center rounded-full transition-all duration-150 cursor-pointer disabled:opacity-50 disabled:pointer-events-none select-none ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {isLoading ? (
        <span className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin shrink-0" />
      ) : icon ? (
        <span className="shrink-0">{icon}</span>
      ) : null}
      <span>{children}</span>
    </button>
  );
};

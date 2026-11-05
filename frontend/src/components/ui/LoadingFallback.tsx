import React from 'react';
import { Sparkles } from 'lucide-react';

export const LoadingFallback: React.FC = () => {
  return (
    <div className="min-h-[50vh] flex flex-col items-center justify-center p-8">
      <div className="w-12 h-12 rounded-2xl bg-signal-navy flex items-center justify-center text-signal-lime animate-bounce shadow-signal-glow mb-4">
        <Sparkles className="w-6 h-6" />
      </div>
      <p className="text-xs font-semibold uppercase tracking-wider text-signal-navy animate-pulse">
        HireSense<span className="text-signal-lime font-mono">.AI</span> · Đang tải dữ liệu...
      </p>
    </div>
  );
};


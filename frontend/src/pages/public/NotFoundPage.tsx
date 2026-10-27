import React from 'react';
import { NavLink } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { AlertTriangle, Home } from 'lucide-react';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-signal-offwhite flex flex-col items-center justify-center p-6 text-center">
      <div className="w-16 h-16 rounded-full bg-signal-coral/15 text-signal-coral flex items-center justify-center mb-6">
        <AlertTriangle className="w-8 h-8" />
      </div>
      <span className="font-mono text-sm font-bold text-signal-slate uppercase tracking-widest mb-2">
        Error 404
      </span>
      <h1 className="font-heading text-4xl sm:text-5xl font-bold text-signal-navy mb-4">
        Không tìm thấy trang yêu cầu
      </h1>
      <p className="text-signal-slate max-w-md mb-8">
        Đường dẫn bạn vừa truy cập có thể đã được thay đổi, di chuyển hoặc không còn tồn tại trên hệ thống HireSense AI.
      </p>
      <NavLink to="/">
        <Button variant="primary" icon={<Home className="w-4 h-4" />}>
          Trở về Trang chủ
        </Button>
      </NavLink>
    </div>
  );
};

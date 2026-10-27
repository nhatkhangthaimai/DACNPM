import React, { useState } from 'react';
import { User, UserRole } from '../../types';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { Search, Lock, Unlock, ShieldCheck, Mail, Phone, Calendar } from 'lucide-react';

export const UserManagement: React.FC = () => {
  const [users, setUsers] = useState<User[]>([
    {
      id: 'usr-1',
      email: 'nguyenvanan.ai@gmail.com',
      fullName: 'Nguyễn Văn An',
      phone: '0908 123 456',
      role: 'candidate',
      isActive: true,
      isVerified: true,
      createdAt: '2026-10-15T10:00:00Z',
    },
    {
      id: 'usr-2',
      email: 'hr.lead@vng.com.vn',
      fullName: 'Trần Minh Thu (VNG HR)',
      phone: '0912 345 678',
      role: 'recruiter',
      isActive: true,
      isVerified: true,
      createdAt: '2026-10-10T09:00:00Z',
    },
    {
      id: 'usr-3',
      email: 'talent@fpt.com',
      fullName: 'Lê Quang Huy (FPT Software)',
      phone: '0988 111 222',
      role: 'recruiter',
      isActive: true,
      isVerified: true,
      createdAt: '2026-10-12T11:00:00Z',
    },
    {
      id: 'usr-4',
      email: 'admin@hiresense.ai',
      fullName: 'Lê Hoàng Long',
      phone: '0988 888 888',
      role: 'admin',
      isActive: true,
      isVerified: true,
      createdAt: '2026-10-01T00:00:00Z',
    },
    {
      id: 'usr-5',
      email: 'pham.quynh@gmail.com',
      fullName: 'Phạm Như Quỳnh',
      phone: '0933 555 777',
      role: 'candidate',
      isActive: false, // Locked account example
      isVerified: true,
      createdAt: '2026-10-18T14:00:00Z',
    }
  ]);

  const [roleFilter, setRoleFilter] = useState<string>('all');
  const [search, setSearch] = useState('');

  const handleToggleLock = (userId: string) => {
    setUsers(users.map(u => {
      if (u.id === userId) {
        return { ...u, isActive: !u.isActive };
      }
      return u;
    }));
  };

  const filteredUsers = users.filter(u => {
    if (roleFilter !== 'all' && u.role !== roleFilter) return false;
    if (search && !u.fullName.toLowerCase().includes(search.toLowerCase()) && !u.email.toLowerCase().includes(search.toLowerCase())) return false;
    return true;
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title="Quản lý Người dùng & Phân quyền"
        subtitle="Quản lý danh sách ứng viên, tài khoản nhà tuyển dụng và kiểm soát trạng thái hoạt động tài khoản."
      />

      {/* Search and Role Filter */}
      <div className="bg-white p-4 sm:p-5 rounded-3xl border border-slate-200/80 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
          <input
            type="text"
            placeholder="Tìm theo tên hoặc email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2.5 text-xs bg-signal-offwhite rounded-xl border border-slate-200 focus:outline-none focus:border-signal-navy"
          />
        </div>

        <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto">
          {['all', 'candidate', 'recruiter', 'admin'].map((r) => (
            <button
              key={r}
              onClick={() => setRoleFilter(r)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold capitalize whitespace-nowrap transition-all ${
                roleFilter === r
                  ? 'bg-signal-navy text-white'
                  : 'bg-signal-offwhite text-signal-slate hover:bg-slate-200/60'
              }`}
            >
              {r === 'all' ? 'Tất cả' : r === 'candidate' ? 'Ứng viên' : r === 'recruiter' ? 'Nhà tuyển dụng' : 'Admin'}
            </button>
          ))}
        </div>
      </div>

      {/* Users Table */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-signal-offwhite border-b border-slate-200/80 text-[11px] font-bold uppercase tracking-wider text-signal-slate">
                <th className="py-4 px-6">Người dùng</th>
                <th className="py-4 px-6">Vai trò</th>
                <th className="py-4 px-6">Trạng thái</th>
                <th className="py-4 px-6">Ngày tham gia</th>
                <th className="py-4 px-6 text-right">Hành động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {filteredUsers.map((u) => (
                <tr key={u.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="py-4 px-6">
                    <span className="font-heading font-bold text-signal-navy block">
                      {u.fullName}
                    </span>
                    <span className="text-xs text-signal-slate">{u.email}</span>
                  </td>
                  <td className="py-4 px-6">
                    <span
                      className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wide ${
                        u.role === 'admin'
                          ? 'bg-signal-navy text-signal-lime'
                          : u.role === 'recruiter'
                          ? 'bg-signal-lavender/25 text-[#5942be]'
                          : 'bg-signal-mint/20 text-[#1b7a66]'
                      }`}
                    >
                      {u.role}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <span
                      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                        u.isActive
                          ? 'bg-emerald-50 text-emerald-700'
                          : 'bg-rose-50 text-rose-700'
                      }`}
                    >
                      <span className={`w-1.5 h-1.5 rounded-full ${u.isActive ? 'bg-emerald-500' : 'bg-rose-500'}`} />
                      {u.isActive ? 'Đang hoạt động' : 'Đã khóa tài khoản'}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-xs text-slate-500">
                    {new Date(u.createdAt).toLocaleDateString('vi-VN')}
                  </td>
                  <td className="py-4 px-6 text-right">
                    {u.role !== 'admin' && (
                      <Button
                        variant={u.isActive ? 'danger' : 'lime'}
                        size="sm"
                        onClick={() => handleToggleLock(u.id)}
                        icon={u.isActive ? <Lock className="w-3.5 h-3.5" /> : <Unlock className="w-3.5 h-3.5" />}
                      >
                        {u.isActive ? 'Khóa tài khoản' : 'Mở khóa'}
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

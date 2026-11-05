import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { User, UserRole } from '../types';

const rawApiUrl = (import.meta.env.VITE_API_URL || '').trim();
const API_BASE_URL = (rawApiUrl && rawApiUrl.startsWith('https://'))
  ? (rawApiUrl.endsWith('/api/v1') ? rawApiUrl : `${rawApiUrl.replace(/\/+$/, '')}/api/v1`)
  : '/api/v1';

// Demo mode is STRICTLY disabled in production. Only enabled if explicitly configured in dev environment.
export const IS_DEMO_ALLOWED = Boolean(
  import.meta.env.DEV && import.meta.env.VITE_ENABLE_DEMO_MODE === 'true'
);

interface AuthContextType {
  user: User | null;
  token: string | null;
  role: UserRole;
  isAuthenticated: boolean;
  isDemoMode: boolean;
  isDemoAllowed: boolean;
  authError: string | null;
  clearAuthError: () => void;
  login: (email: string, password: string, selectedRole?: UserRole) => Promise<boolean>;
  registerCandidate: (data: { email: string; fullName: string; phone?: string; title?: string; password?: string }) => Promise<boolean>;
  registerRecruiter: (data: { email: string; fullName: string; companyName: string; phone?: string; password?: string }) => Promise<boolean>;
  forgotPassword: (email: string) => Promise<{ success: boolean; message: string }>;
  resetPassword: (token: string, newPassword: string) => Promise<{ success: boolean; message: string }>;
  logout: () => void;
  switchDemoRole: (role: UserRole) => void;
}

const DEMO_USERS: Record<UserRole, User> = {
  candidate: {
    id: 'user-cand-1',
    email: 'nguyenvanan.ai@gmail.com',
    fullName: 'Nguyễn Văn An',
    phone: '0908 123 456',
    role: 'candidate',
    isActive: true,
    isVerified: true,
    createdAt: '2026-10-15T10:00:00Z',
  },
  recruiter: {
    id: 'user-rec-1',
    email: 'hr.lead@vng.com.vn',
    fullName: 'Trần Minh Thu (VNG HR)',
    phone: '0912 345 678',
    role: 'recruiter',
    isActive: true,
    isVerified: true,
    createdAt: '2026-10-10T09:00:00Z',
  },
  admin: {
    id: 'user-adm-1',
    email: 'admin@hiresense.ai',
    fullName: 'Lê Hoàng Long (Quản trị viên)',
    phone: '0988 888 888',
    role: 'admin',
    isActive: true,
    isVerified: true,
    createdAt: '2026-10-01T00:00:00Z',
  }
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const token = localStorage.getItem('hiresense_token');
    const saved = localStorage.getItem('hiresense_user');
    if (token && saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return null;
      }
    }
    return null;
  });

  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('hiresense_token') || null;
  });

  const [isDemoMode, setIsDemoMode] = useState<boolean>(() => {
    return IS_DEMO_ALLOWED && localStorage.getItem('hiresense_demo_mode') === 'true';
  });

  const [authError, setAuthError] = useState<string | null>(null);

  const clearAuthError = () => setAuthError(null);

  useEffect(() => {
    if (user) {
      localStorage.setItem('hiresense_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('hiresense_user');
    }
  }, [user]);

  useEffect(() => {
    if (token) {
      localStorage.setItem('hiresense_token', token);
    } else {
      localStorage.removeItem('hiresense_token');
    }
  }, [token]);

  useEffect(() => {
    if (IS_DEMO_ALLOWED) {
      localStorage.setItem('hiresense_demo_mode', String(isDemoMode));
    } else {
      localStorage.removeItem('hiresense_demo_mode');
    }
  }, [isDemoMode]);

  const login = async (email: string, password: string, selectedRole: UserRole = 'candidate'): Promise<boolean> => {
    setAuthError(null);
    try {
      // 1. Authenticate with backend FastAPI
      const res = await axios.post(`${API_BASE_URL}/auth/login`, {
        email,
        password,
      }, { timeout: 8000 });

      if (res.data && res.data.access_token) {
        const data = res.data;
        const loggedUser: User = {
          id: data.user_id,
          email: data.email,
          fullName: data.full_name,
          role: data.role as UserRole,
          isActive: true,
          isVerified: true,
          createdAt: new Date().toISOString(),
        };
        setUser(loggedUser);
        setToken(data.access_token);
        setIsDemoMode(false);
        return true;
      }
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || 'Email hoặc mật khẩu không chính xác.';
      // 2. Only if demo mode is explicitly enabled in dev environment, allow fallback
      if (IS_DEMO_ALLOWED && selectedRole) {
        const targetUser = DEMO_USERS[selectedRole];
        const loggedUser: User = {
          ...targetUser,
          email: email || targetUser.email,
        };
        setUser(loggedUser);
        setToken(`jwt_${loggedUser.role}_${Date.now()}`);
        setIsDemoMode(true);
        return true;
      }
      setAuthError(detail);
      return false;
    }

    setAuthError('Đăng nhập không thành công.');
    return false;
  };

  const registerCandidate = async (data: { email: string; fullName: string; phone?: string; title?: string; password?: string }): Promise<boolean> => {
    setAuthError(null);
    try {
      const res = await axios.post(`${API_BASE_URL}/auth/register/candidate`, {
        email: data.email,
        password: data.password || 'password123',
        full_name: data.fullName,
        phone: data.phone,
        title: data.title,
      }, { timeout: 8000 });

      if (res.data && res.data.access_token) {
        const ret = res.data;
        const newUser: User = {
          id: ret.user_id,
          email: ret.email,
          fullName: ret.full_name,
          phone: data.phone,
          role: 'candidate',
          isActive: true,
          isVerified: true,
          createdAt: new Date().toISOString(),
        };
        setUser(newUser);
        setToken(ret.access_token);
        setIsDemoMode(false);
        return true;
      }
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || 'Đăng ký tài khoản ứng viên thất bại.';
      setAuthError(detail);
      return false;
    }
    return false;
  };

  const registerRecruiter = async (data: { email: string; fullName: string; companyName: string; phone?: string; password?: string }): Promise<boolean> => {
    setAuthError(null);
    try {
      const res = await axios.post(`${API_BASE_URL}/auth/register/recruiter`, {
        email: data.email,
        password: data.password || 'password123',
        full_name: data.fullName,
        company_name: data.companyName,
        phone: data.phone,
      }, { timeout: 8000 });

      if (res.data && res.data.access_token) {
        const ret = res.data;
        const newUser: User = {
          id: ret.user_id,
          email: ret.email,
          fullName: `${ret.full_name} (${data.companyName})`,
          phone: data.phone,
          role: 'recruiter',
          isActive: true,
          isVerified: true,
          createdAt: new Date().toISOString(),
        };
        setUser(newUser);
        setToken(ret.access_token);
        setIsDemoMode(false);
        return true;
      }
    } catch (err: any) {
      const detail = err.response?.data?.detail || err.message || 'Đăng ký tài khoản nhà tuyển dụng thất bại.';
      setAuthError(detail);
      return false;
    }
    return false;
  };

  const forgotPassword = async (email: string): Promise<{ success: boolean; message: string }> => {
    try {
      const res = await axios.post(`${API_BASE_URL}/auth/forgot-password`, { email });
      return { success: true, message: res.data?.message || 'Yêu cầu đặt lại mật khẩu đã được xử lý.' };
    } catch (err: any) {
      return { success: false, message: err.response?.data?.detail || 'Không thể gửi yêu cầu đặt lại mật khẩu.' };
    }
  };

  const resetPassword = async (resetToken: string, newPassword: string): Promise<{ success: boolean; message: string }> => {
    try {
      const res = await axios.post(`${API_BASE_URL}/auth/reset-password`, { token: resetToken, new_password: newPassword });
      return { success: true, message: res.data?.message || 'Mật khẩu đã được cập nhật thành công.' };
    } catch (err: any) {
      return { success: false, message: err.response?.data?.detail || 'Mã xác nhận không hợp lệ hoặc đã hết hạn.' };
    }
  };

  const logout = () => {
    try {
      if (token) {
        axios.post(`${API_BASE_URL}/auth/logout`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        }).catch(() => {});
      }
    } finally {
      setUser(null);
      setToken(null);
      setIsDemoMode(false);
      setAuthError(null);
      localStorage.removeItem('hiresense_user');
      localStorage.removeItem('hiresense_token');
      localStorage.removeItem('hiresense_demo_mode');
    }
  };

  const switchDemoRole = (role: UserRole) => {
    if (!IS_DEMO_ALLOWED) {
      console.warn('[Security Guard] Demo role switching is strictly disabled in production.');
      return;
    }
    const nextUser = DEMO_USERS[role];
    setUser(nextUser);
    setToken(`jwt_${role}_${Date.now()}`);
    setIsDemoMode(true);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        role: user?.role || 'candidate',
        isAuthenticated: !!user,
        isDemoMode,
        isDemoAllowed: IS_DEMO_ALLOWED,
        authError,
        clearAuthError,
        login,
        registerCandidate,
        registerRecruiter,
        forgotPassword,
        resetPassword,
        logout,
        switchDemoRole,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

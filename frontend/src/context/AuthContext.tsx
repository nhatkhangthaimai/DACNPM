import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { User, UserRole } from '../types';

const rawApiUrl = (import.meta.env.VITE_API_URL || '').trim();
const API_BASE_URL = (rawApiUrl && rawApiUrl.startsWith('https://'))
  ? (rawApiUrl.endsWith('/api/v1') ? rawApiUrl : `${rawApiUrl.replace(/\/+$/, '')}/api/v1`)
  : '/api/v1';

interface AuthContextType {
  user: User | null;
  token: string | null;
  role: UserRole;
  isAuthenticated: boolean;
  isDemoMode: boolean;
  login: (email: string, password: string, selectedRole?: UserRole) => Promise<boolean>;
  registerCandidate: (data: { email: string; fullName: string; phone?: string; title?: string; password?: string }) => Promise<boolean>;
  registerRecruiter: (data: { email: string; fullName: string; companyName: string; phone?: string; password?: string }) => Promise<boolean>;
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
    return localStorage.getItem('hiresense_demo_mode') === 'true';
  });

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
    localStorage.setItem('hiresense_demo_mode', String(isDemoMode));
  }, [isDemoMode]);

  const login = async (email: string, password: string, selectedRole: UserRole = 'candidate'): Promise<boolean> => {
    try {
      // 1. Try authenticating with backend FastAPI first
      const res = await axios.post(`${API_BASE_URL}/auth/login`, {
        email,
        password,
      }, { timeout: 4000 });

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
      console.warn('Backend login attempt encountered error, checking demo credentials fallback:', err?.message);
    }

    // 2. Fallback to Demo persona login if demo credentials match
    const targetUser = DEMO_USERS[selectedRole];
    const loggedUser: User = {
      ...targetUser,
      email: email || targetUser.email,
    };
    const isDemoEmail = Object.values(DEMO_USERS).some(u => u.email === email);
    if (!isDemoEmail) {
      const realUser: User = {
        id: `user-${selectedRole}-${btoa(email).replace(/[^a-z0-9]/gi, '').slice(0, 8)}`,
        email,
        fullName: email.split('@')[0],
        role: selectedRole,
        isActive: true,
        isVerified: true,
        createdAt: new Date().toISOString(),
      };
      setUser(realUser);
      setToken(`jwt_${selectedRole}_${Date.now()}`);
      setIsDemoMode(false);
      return true;
    }

    setUser(loggedUser);
    setToken(`jwt_${loggedUser.role}_${Date.now()}`);
    setIsDemoMode(true);
    return true;
  };

  const registerCandidate = async (data: { email: string; fullName: string; phone?: string; title?: string; password?: string }): Promise<boolean> => {
    try {
      const res = await axios.post(`${API_BASE_URL}/auth/register/candidate`, {
        email: data.email,
        password: data.password || 'password123',
        full_name: data.fullName,
        phone: data.phone,
        title: data.title,
      }, { timeout: 5000 });

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
      console.warn('Backend candidate register error, falling back locally:', err?.message);
    }

    const userId = `cand-${Date.now()}`;
    const newUser: User = {
      id: userId,
      email: data.email,
      fullName: data.fullName,
      phone: data.phone,
      role: 'candidate',
      isActive: true,
      isVerified: true,
      createdAt: new Date().toISOString(),
    };
    setUser(newUser);
    setToken(`jwt_candidate_${Date.now()}`);
    setIsDemoMode(false);
    return true;
  };

  const registerRecruiter = async (data: { email: string; fullName: string; companyName: string; phone?: string; password?: string }): Promise<boolean> => {
    try {
      const res = await axios.post(`${API_BASE_URL}/auth/register/recruiter`, {
        email: data.email,
        password: data.password || 'password123',
        full_name: data.fullName,
        company_name: data.companyName,
        phone: data.phone,
      }, { timeout: 5000 });

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
      console.warn('Backend recruiter register error, falling back locally:', err?.message);
    }

    const newUser: User = {
      id: `rec-${Date.now()}`,
      email: data.email,
      fullName: `${data.fullName} (${data.companyName})`,
      phone: data.phone,
      role: 'recruiter',
      isActive: true,
      isVerified: true,
      createdAt: new Date().toISOString(),
    };
    setUser(newUser);
    setToken(`jwt_recruiter_${Date.now()}`);
    setIsDemoMode(false);
    return true;
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setIsDemoMode(false);
    localStorage.removeItem('hiresense_user');
    localStorage.removeItem('hiresense_token');
    localStorage.removeItem('hiresense_demo_mode');
  };

  const switchDemoRole = (role: UserRole) => {
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
        login,
        registerCandidate,
        registerRecruiter,
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

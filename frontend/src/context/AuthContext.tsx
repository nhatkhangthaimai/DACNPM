import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, UserRole } from '../types';

interface AuthContextType {
  user: User | null;
  token: string | null;
  role: UserRole;
  isAuthenticated: boolean;
  login: (email: string, password: string, selectedRole?: UserRole) => Promise<boolean>;
  registerCandidate: (data: { email: string; fullName: string; phone?: string; title?: string }) => Promise<boolean>;
  registerRecruiter: (data: { email: string; fullName: string; companyName: string; phone?: string }) => Promise<boolean>;
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
    const saved = localStorage.getItem('hiresense_user');
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch {
        return DEMO_USERS.candidate;
      }
    }
    return DEMO_USERS.candidate; // Default to Candidate for initial experience
  });

  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('hiresense_token') || 'demo_mock_jwt_token_signal_2026';
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

  const login = async (email: string, password: string, selectedRole: UserRole = 'candidate'): Promise<boolean> => {
    // Attempt demo / API login
    const targetUser = DEMO_USERS[selectedRole];
    const loggedUser: User = {
      ...targetUser,
      email: email || targetUser.email,
    };
    setUser(loggedUser);
    setToken(`jwt_${loggedUser.role}_${Date.now()}`);
    return true;
  };

  const registerCandidate = async (data: { email: string; fullName: string; phone?: string; title?: string }): Promise<boolean> => {
    const newUser: User = {
      id: `cand-${Date.now()}`,
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
    return true;
  };

  const registerRecruiter = async (data: { email: string; fullName: string; companyName: string; phone?: string }): Promise<boolean> => {
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
    return true;
  };

  const logout = () => {
    setUser(null);
    setToken(null);
  };

  const switchDemoRole = (role: UserRole) => {
    const nextUser = DEMO_USERS[role];
    setUser(nextUser);
    setToken(`jwt_${role}_${Date.now()}`);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        role: user?.role || 'candidate',
        isAuthenticated: !!user,
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

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallbackTitle?: string;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('[HireSense AI] Uncaught render error in component tree:', error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[360px] flex items-center justify-center p-6">
          <div className="bg-white rounded-3xl border border-rose-200 p-8 max-w-lg w-full text-center shadow-lg space-y-4">
            <div className="w-14 h-14 bg-rose-50 text-rose-600 rounded-2xl flex items-center justify-center mx-auto">
              <AlertTriangle className="w-7 h-7" />
            </div>
            <h3 className="font-heading font-bold text-lg text-signal-navy">
              {this.props.fallbackTitle || 'Đã xảy ra sự cố hiển thị'}
            </h3>
            <p className="text-sm text-signal-slate">
              {this.state.error?.message || 'Giao diện gặp sự cố tạm thời khi xử lý dữ liệu. Vui lòng bấm thử lại hoặc tải lại trang.'}
            </p>
            <div className="pt-2 flex justify-center gap-3">
              <button
                onClick={() => {
                  this.setState({ hasError: false, error: null });
                }}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-signal-lime text-signal-navy text-xs font-bold hover:opacity-90 transition-all cursor-pointer"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                Thử lại
              </button>
              <button
                onClick={() => window.location.reload()}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-slate-100 text-slate-700 text-xs font-semibold hover:bg-slate-200 transition-all cursor-pointer"
              >
                Tải lại trang (F5)
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

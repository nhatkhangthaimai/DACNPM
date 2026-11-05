import React from 'react';
import { NavLink } from 'react-router-dom';
import { Sparkles, Shield, ArrowLeft, CheckCircle2, Lock, Eye, Trash2, FileText } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const PrivacyPolicyPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-signal-offwhite text-signal-navy font-sans">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-30">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <NavLink to="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-signal-navy text-signal-lime flex items-center justify-center">
              <Sparkles className="w-5 h-5" />
            </div>
            <span className="font-heading font-bold text-xl text-signal-navy">
              HireSense<span className="text-signal-lime font-mono">.AI</span>
            </span>
          </NavLink>
          <NavLink to="/">
            <Button variant="outline" size="sm" icon={<ArrowLeft className="w-4 h-4" />}>
              Về Trang chủ
            </Button>
          </NavLink>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
        <div className="bg-white rounded-3xl p-8 sm:p-12 border border-slate-200 shadow-sm space-y-8">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-signal-mint/15 text-teal-800 text-xs font-semibold mb-3 border border-signal-mint/40">
              <Shield className="w-3.5 h-3.5" />
              Tuân thủ Luật 91/2025/QH15 & Nghị định 356/2025/NĐ-CP
            </div>
            <h1 className="font-heading text-3xl sm:text-4xl font-bold tracking-tight text-signal-navy">
              Chính sách Quyền riêng tư & Bảo vệ Dữ liệu Cá nhân
            </h1>
            <p className="text-sm text-signal-slate mt-2">
              Phiên bản hiệu lực: Tháng 11/2026 · Áp dụng cho toàn bộ người dùng và dữ liệu CV trên nền tảng HireSense AI.
            </p>
          </div>

          <div className="border-t border-slate-100 pt-6 space-y-6 text-sm text-slate-700 leading-relaxed">
            <section className="space-y-3">
              <h2 className="font-heading text-lg font-bold text-signal-navy flex items-center gap-2">
                <Lock className="w-5 h-5 text-signal-navy" />
                1. Nguyên tắc cốt lõi về bảo vệ dữ liệu
              </h2>
              <p>
                HireSense AI tôn trọng tuyệt đối quyền riêng tư và dữ liệu cá nhân của ứng viên. Chúng tôi cam kết:
              </p>
              <ul className="list-disc pl-5 space-y-1.5 text-slate-600">
                <li>Chỉ thu thập thông tin CV phục vụ mục đích duy nhất là phân tích kỹ năng và gợi ý việc làm phù hợp.</li>
                <li>Không bán, chia sẻ hoặc thương mại hóa hồ sơ cá nhân của bạn cho bất kỳ bên thứ ba không liên quan.</li>
                <li>Hồ sơ CV của bạn chỉ được cung cấp cho nhà tuyển dụng khi bạn chủ động nộp đơn ứng tuyển cho vị trí đó.</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="font-heading text-lg font-bold text-signal-navy flex items-center gap-2">
                <Eye className="w-5 h-5 text-signal-navy" />
                2. Minh bạch về việc sử dụng Trí tuệ Nhân tạo (Gemini AI)
              </h2>
              <p>
                HireSense AI ứng dụng Google Gemini API để đọc hiểu văn bản CV và hỗ trợ trích xuất có cấu trúc:
              </p>
              <ul className="list-disc pl-5 space-y-1.5 text-slate-600">
                <li>Điểm số so khớp (Matching Score) chỉ mang tính chất <strong>tham khảo và định hướng</strong>, không thay thế cho quyết định tuyển dụng của con người.</li>
                <li>Hệ thống áp dụng thuật toán công bằng (Fair AI): Tuyệt đối không sử dụng giới tính, độ tuổi, tôn giáo, địa chỉ cư trú hoặc hình ảnh chân dung để chấm điểm năng lực.</li>
                <li>Nếu dữ liệu trích xuất có sai lệch, ứng viên có toàn quyền tự do chỉnh sửa thông tin kỹ năng trực tiếp trên hệ thống.</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="font-heading text-lg font-bold text-signal-navy flex items-center gap-2">
                <Trash2 className="w-5 h-5 text-signal-navy" />
                3. Quyền của Chủ thể Dữ liệu (Rights of Data Subjects)
              </h2>
              <p>
                Theo quy định của Luật Bảo vệ Dữ liệu Cá nhân Việt Nam, bạn có đầy đủ các quyền:
              </p>
              <div className="grid sm:grid-cols-2 gap-3 pt-1">
                <div className="p-4 rounded-2xl bg-signal-offwhite border border-slate-200">
                  <span className="font-bold block text-signal-navy mb-1">Quyền Xuất Dữ liệu (Portability)</span>
                  <span className="text-xs text-slate-600">Bạn có thể tải về toàn bộ dữ liệu cá nhân và lịch sử ứng tuyển dưới dạng tệp tin JSON có cấu trúc bất cứ lúc nào.</span>
                </div>
                <div className="p-4 rounded-2xl bg-signal-offwhite border border-slate-200">
                  <span className="font-bold block text-signal-navy mb-1">Quyền Được Lãng Quên (Erasure)</span>
                  <span className="text-xs text-slate-600">Bạn có thể yêu cầu xóa vĩnh viễn toàn bộ tệp CV và tài khoản khỏi hệ thống máy chủ và cơ sở dữ liệu ngay lập tức.</span>
                </div>
              </div>
            </section>

            <section className="space-y-3">
              <h2 className="font-heading text-lg font-bold text-signal-navy flex items-center gap-2">
                <FileText className="w-5 h-5 text-signal-navy" />
                4. Liên hệ bộ phận Bảo vệ Dữ liệu (DPO)
              </h2>
              <p>
                Mọi thắc mắc, yêu cầu trợ giúp hoặc khiếu nại về xử lý dữ liệu cá nhân, xin vui lòng liên hệ:
              </p>
              <p className="font-mono text-xs bg-signal-offwhite p-3 rounded-xl border border-slate-200">
                Email DPO: privacy@hiresense.ai · Hotline: 1900 8888 · Địa chỉ: TP. Hồ Chí Minh, Việt Nam
              </p>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
};


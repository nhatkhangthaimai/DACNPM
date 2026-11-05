import React from 'react';
import { NavLink } from 'react-router-dom';
import { Sparkles, FileText, ArrowLeft, ShieldAlert, CheckCircle, Scale } from 'lucide-react';
import { Button } from '../../components/ui/Button';

export const TermsOfServicePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-signal-offwhite text-signal-navy font-sans">
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

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
        <div className="bg-white rounded-3xl p-8 sm:p-12 border border-slate-200 shadow-sm space-y-8">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-signal-lime/20 text-signal-navy text-xs font-semibold mb-3 border border-signal-lime/50">
              <Scale className="w-3.5 h-3.5" />
              Điều khoản Nền tảng Tuyển dụng Thông minh
            </div>
            <h1 className="font-heading text-3xl sm:text-4xl font-bold tracking-tight text-signal-navy">
              Điều khoản Dịch vụ HireSense AI
            </h1>
            <p className="text-sm text-signal-slate mt-2">
              Có hiệu lực từ ngày 01/11/2026. Bằng việc truy cập hoặc sử dụng HireSense AI, bạn đồng ý với các điều khoản dưới đây.
            </p>
          </div>

          <div className="border-t border-slate-100 pt-6 space-y-6 text-sm text-slate-700 leading-relaxed">
            <section className="space-y-3">
              <h2 className="font-heading text-lg font-bold text-signal-navy">
                1. Quy định đối với Nhà tuyển dụng (Recruiter)
              </h2>
              <ul className="list-disc pl-5 space-y-1.5 text-slate-600">
                <li>Thông tin doanh nghiệp và nội dung tin tuyển dụng (JD) phải trung thực, chính xác và hợp pháp tại Việt Nam.</li>
                <li>Nghiêm cấm tuyệt đối hành vi thu phí tuyển dụng, đặt cọc giữ chỗ, yêu cầu nạp tiền hoặc làm nhiệm vụ trái pháp luật.</li>
                <li>Mọi tin tuyển dụng vi phạm quy chuẩn an toàn sẽ bị hệ thống tự động đình chỉ và xử lý tài khoản theo quy định.</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="font-heading text-lg font-bold text-signal-navy">
                2. Quy định đối với Ứng viên (Candidate)
              </h2>
              <ul className="list-disc pl-5 space-y-1.5 text-slate-600">
                <li>Ứng viên cam kết thông tin kỹ năng, học vấn và kinh nghiệm trong CV là có thực và thuộc quyền sở hữu của chính mình.</li>
                <li>Không tải lên các tệp tin chứa mã độc, tài liệu khiêu dâm hoặc nội dung xâm phạm bản quyền/bí mật kinh doanh.</li>
                <li>Ứng viên có quyền rút đơn ứng tuyển hoặc yêu cầu nhà tuyển dụng xóa dữ liệu hồ sơ theo quy định pháp luật.</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="font-heading text-lg font-bold text-signal-navy">
                3. Miễn trừ trách nhiệm về Đánh giá AI
              </h2>
              <p>
                Điểm số phù hợp (Matching Score) và phân tích khoảng cách kỹ năng (Skill Gap) là các thuật toán trợ lực dựa trên mô hình toán học và LLMs. HireSense AI không đảm bảo tuyệt đối rằng ứng viên sẽ được tuyển dụng hoặc nhà tuyển dụng sẽ chọn được ứng viên hoàn hảo. Quyết định phỏng vấn và ký kết hợp đồng lao động hoàn toàn thuộc thẩm quyền của hai bên.
              </p>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
};


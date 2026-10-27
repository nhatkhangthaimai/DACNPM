import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { apiService } from '../../services/api';
import { Job } from '../../types';
import { Button } from '../../components/ui/Button';
import { JobCard } from '../../components/ui/JobCard';
import { MatchScoreRing } from '../../components/ui/MatchScoreRing';
import { SkillBadge } from '../../components/ui/SkillBadge';
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Zap,
  Target,
  FileSearch,
  Cpu,
  TrendingUp,
  CheckCircle2,
  Users,
  Building2,
  Layers,
  ChevronRight
} from 'lucide-react';

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated, role } = useAuth();
  const [featuredJobs, setFeaturedJobs] = useState<Job[]>([]);
  const [selectedDemoScore, setSelectedDemoScore] = useState<number>(94);

  useEffect(() => {
    apiService.getJobs().then(jobs => setFeaturedJobs(jobs.slice(0, 3)));
  }, []);

  return (
    <div className="min-h-screen bg-signal-offwhite text-signal-navy flex flex-col selection:bg-signal-lime selection:text-signal-navy">
      {/* Floating Stadium Navigation (Mobbin / SIGNAL Pill style) */}
      <header className="sticky top-4 z-50 px-4 max-w-6xl mx-auto w-full">
        <div className="bg-white/95 backdrop-blur-md rounded-full px-5 py-3 border border-slate-200/90 shadow-sm flex items-center justify-between">
          {/* Logo brand lockup */}
          <NavLink to="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-full bg-signal-navy flex items-center justify-center text-signal-lime">
              <Sparkles className="w-4 h-4" />
            </div>
            <span className="font-heading font-bold text-lg tracking-tight text-signal-navy">
              HireSense<span className="text-signal-navy font-mono">.AI</span>
            </span>
          </NavLink>

          {/* Center Links */}
          <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-signal-slate">
            <a href="#matching" className="hover:text-signal-navy transition-colors">Công nghệ AI Matching</a>
            <a href="#features" className="hover:text-signal-navy transition-colors">Tính năng nổi bật</a>
            <a href="#jobs" className="hover:text-signal-navy transition-colors">Việc làm mới nhất</a>
            <a href="#workflow" className="hover:text-signal-navy transition-colors">Quy trình xử lý</a>
          </nav>

          {/* Action CTAs */}
          <div className="flex items-center gap-2.5">
            {isAuthenticated ? (
              <Button
                variant="primary"
                size="sm"
                onClick={() => navigate(`/${role}/dashboard`)}
                icon={<ArrowRight className="w-3.5 h-3.5" />}
              >
                Vào Dashboard
              </Button>
            ) : (
              <>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => navigate('/login')}
                >
                  Đăng nhập
                </Button>
                <Button
                  variant="lime"
                  size="sm"
                  onClick={() => navigate('/register/candidate')}
                >
                  Tham gia miễn phí
                </Button>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Hero Section – Editorial AI Recruiter Header */}
      <section className="pt-16 pb-20 px-4 max-w-7xl mx-auto w-full text-center">
        {/* Eyebrow Chip */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-signal-lime/25 border border-signal-lime/50 text-xs font-semibold text-[#445b14] mb-6 shadow-sm">
          <Sparkles className="w-3.5 h-3.5 text-signal-navy" />
          <span>HireSense AI – SIGNAL Edition | Tuyển dụng thông minh thế hệ mới</span>
        </div>

        {/* Main Display Headline */}
        <h1 className="font-heading text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-signal-navy max-w-5xl mx-auto leading-[1.08] mb-6">
          Khớp lệnh việc làm chính xác với <span className="underline decoration-signal-lime decoration-4 underline-offset-8">Mô hình Ngôn ngữ Lớn</span>.
        </h1>

        {/* Subtitle */}
        <p className="text-lg sm:text-xl text-signal-slate max-w-3xl mx-auto font-light leading-relaxed mb-10">
          Nền tảng tuyển dụng thông minh tích hợp Google Gemini API & Vector Database pgvector.
          Tự động trích xuất cấu trúc CV, phân tích khoảng cách kỹ năng (Skill Gap) và kết nối nhân tài phù hợp trong vài giây.
        </p>

        {/* Hero CTAs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
          <Button
            variant="lime"
            size="lg"
            onClick={() => navigate('/register/candidate')}
            icon={<ArrowRight className="w-4 h-4 text-signal-navy" />}
          >
            Trải nghiệm Phân tích CV ngay
          </Button>

          <Button
            variant="primary"
            size="lg"
            onClick={() => navigate('/register/recruiter')}
            icon={<Building2 className="w-4 h-4 text-signal-lime" />}
          >
            Dành cho Nhà tuyển dụng
          </Button>
        </div>

        {/* Interactive Bento Showcase: The SIGNAL Match Engine Preview */}
        <div className="bg-signal-navy rounded-3xl p-6 sm:p-10 text-white text-left shadow-2xl border border-signal-navy-border relative overflow-hidden">
          <div className="absolute top-0 right-1/4 w-96 h-96 bg-signal-lime/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 right-0 w-80 h-80 bg-signal-lavender/15 rounded-full blur-3xl pointer-events-none" />

          <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8 pb-8 border-b border-signal-navy-border mb-8">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-signal-navy-light text-signal-lime text-xs font-mono font-semibold uppercase mb-2">
                <Cpu className="w-3.5 h-3.5" />
                Live Hybrid Matching Engine
              </div>
              <h3 className="font-heading text-2xl sm:text-3xl font-bold text-white">
                Mô phỏng Thuật toán So khớp Thông minh
              </h3>
              <p className="text-sm text-slate-400 mt-1">
                Kết hợp Weighted Hard Skills Matching + Cosine Semantic Similarity + Trải nghiệm thực tế
              </p>
            </div>

            {/* Slider / Score switcher */}
            <div className="flex items-center gap-3 bg-signal-navy-light/80 p-2 rounded-2xl border border-signal-navy-border">
              <span className="text-xs text-slate-400 font-medium pl-2">Mức độ tương thích:</span>
              {[78, 88, 94].map((s) => (
                <button
                  key={s}
                  onClick={() => setSelectedDemoScore(s)}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                    selectedDemoScore === s
                      ? 'bg-signal-lime text-signal-navy shadow-sm'
                      : 'text-slate-300 hover:text-white'
                  }`}
                >
                  {s}%
                </button>
              ))}
            </div>
          </div>

          {/* Bento Grid inside Hero */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Left Box: CV Input */}
            <div className="bg-signal-navy-light/70 rounded-2xl p-6 border border-signal-navy-border/80">
              <span className="text-xs font-semibold text-signal-lavender uppercase tracking-wider block mb-2">
                01. CV Trích xuất (Candidate)
              </span>
              <h4 className="font-heading font-bold text-lg text-white mb-2">
                Nguyễn Văn An – Senior AI Engineer
              </h4>
              <p className="text-xs text-slate-400 mb-4 line-clamp-2">
                3+ năm kinh nghiệm phát triển hệ thống RAG, LLMs, Vector Databases (pgvector) tại TP.HCM.
              </p>
              <div className="flex flex-wrap gap-1.5">
                {['Python', 'PyTorch', 'LLMs', 'pgvector', 'FastAPI'].map((s, idx) => (
                  <span key={idx} className="px-2.5 py-1 rounded-full text-xs font-medium bg-white/10 text-slate-200">
                    {s}
                  </span>
                ))}
              </div>
            </div>

            {/* Center Box: Ring & Formula */}
            <div className="bg-signal-navy-light/70 rounded-2xl p-6 border border-signal-navy-border/80 flex flex-col items-center justify-center text-center">
              <MatchScoreRing score={selectedDemoScore} size={120} strokeWidth={10} />
              <span className="font-heading font-bold text-sm text-signal-lime mt-3">
                Độ tương thích Xuất sắc
              </span>
              <p className="text-xs text-slate-400 mt-1 max-w-xs">
                Hard Skills (95%) · Ngữ nghĩa (92%) · Kinh nghiệm (88%)
              </p>
            </div>

            {/* Right Box: Target JD & Gap */}
            <div className="bg-signal-navy-light/70 rounded-2xl p-6 border border-signal-navy-border/80">
              <span className="text-xs font-semibold text-signal-mint uppercase tracking-wider block mb-2">
                02. Tin tuyển dụng (Target JD)
              </span>
              <h4 className="font-heading font-bold text-lg text-white mb-2">
                VNG Corp – AI Engineer (LLMs & RAG)
              </h4>
              <div className="space-y-2 mt-4">
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Kỹ năng trùng khớp:</span>
                  <span className="text-signal-mint font-bold">5 / 5 kỹ năng bắt buộc</span>
                </div>
                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">Kỹ năng khuyến khích:</span>
                  <span className="text-signal-gold font-bold">Cần bổ sung Docker / CI-CD</span>
                </div>
                <div className="p-2.5 rounded-xl bg-signal-navy-dark text-[11px] text-slate-300 mt-2 border border-signal-navy-border">
                  ✨ <span className="font-semibold text-signal-lime">AI Gợi ý:</span> Ứng viên sẵn sàng cho vòng phỏng vấn kỹ thuật chuyên sâu.
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Highlights Section */}
      <section id="features" className="py-20 px-4 bg-white border-y border-slate-200/80">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs font-semibold text-signal-slate uppercase tracking-wider block mb-2">
              Tại sao chọn HireSense AI
            </span>
            <h2 className="font-heading text-3xl sm:text-5xl font-bold text-signal-navy tracking-tight">
              Công nghệ giải quyết bài toán tuyển dụng thực tế
            </h2>
            <p className="text-signal-slate text-base sm:text-lg mt-3">
              Không còn tốn hàng giờ lọc CV thủ công hay nhận về những hồ sơ không đúng chuyên môn.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bento-card">
              <div className="w-12 h-12 rounded-2xl bg-signal-lime/20 text-[#4c6615] flex items-center justify-center mb-6">
                <Zap className="w-6 h-6" />
              </div>
              <h3 className="font-heading text-xl font-bold text-signal-navy mb-2">
                Trích xuất CV Đa cấu trúc
              </h3>
              <p className="text-sm text-signal-slate leading-relaxed">
                Gemini LLM phân tích toàn diện định dạng PDF/DOCX, chuẩn hóa học vấn, lịch sử công tác, dự án thực tế và kỹ năng mềm/cứng.
              </p>
            </div>

            <div className="bento-card">
              <div className="w-12 h-12 rounded-2xl bg-signal-lavender/25 text-[#5942be] flex items-center justify-center mb-6">
                <Target className="w-6 h-6" />
              </div>
              <h3 className="font-heading text-xl font-bold text-signal-navy mb-2">
                Hybrid Job Matching
              </h3>
              <p className="text-sm text-signal-slate leading-relaxed">
                Kết hợp vector embedding ngữ nghĩa và trọng số kỹ năng thực tế. Giải thích rõ ràng nguyên nhân cho điểm và minh bạch tiêu chí.
              </p>
            </div>

            <div className="bento-card">
              <div className="w-12 h-12 rounded-2xl bg-signal-mint/20 text-[#1b7a66] flex items-center justify-center mb-6">
                <TrendingUp className="w-6 h-6" />
              </div>
              <h3 className="font-heading text-xl font-bold text-signal-navy mb-2">
                Skill Gap Analysis & Roadmap
              </h3>
              <p className="text-sm text-signal-slate leading-relaxed">
                Tự động phát hiện kỹ năng còn thiếu so với yêu cầu thị trường và gợi ý lộ trình nâng cao năng lực cho ứng viên.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Jobs Section */}
      <section id="jobs" className="py-20 px-4 max-w-7xl mx-auto w-full">
        <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4 mb-10">
          <div>
            <span className="text-xs font-semibold text-signal-slate uppercase tracking-wider block mb-2">
              Cơ hội nghề nghiệp hàng đầu
            </span>
            <h2 className="font-heading text-3xl sm:text-4xl font-bold text-signal-navy tracking-tight">
              Việc làm AI & Công nghệ nổi bật
            </h2>
          </div>
          <Button
            variant="outline"
            size="md"
            onClick={() => navigate('/candidate/jobs')}
            icon={<ArrowRight className="w-4 h-4" />}
          >
            Xem tất cả {featuredJobs.length > 0 ? '12+' : ''} việc làm
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredJobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              matchScore={job.id === 'job-1' ? 92 : job.id === 'job-2' ? 86 : 80}
              onApply={() => navigate('/candidate/jobs')}
              onViewDetails={() => navigate('/candidate/jobs')}
              onCheckMatch={() => navigate('/candidate/matching')}
            />
          ))}
        </div>
      </section>

      {/* 4-Step AI Pipeline Section */}
      <section id="workflow" className="py-20 px-4 bg-signal-navy text-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <span className="text-xs font-semibold text-signal-lime uppercase tracking-wider block mb-2">
              Quy trình AI khép kín
            </span>
            <h2 className="font-heading text-3xl sm:text-4xl font-bold tracking-tight text-white">
              Từ tải lên CV đến quyết định tuyển dụng thông minh
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { step: '01', title: 'Tải lên CV', desc: 'Hỗ trợ kéo thả PDF/DOCX, tự động kiểm tra dung lượng và cấu trúc tệp an toàn.' },
              { step: '02', title: 'Gemini Extraction', desc: 'Trích xuất văn bản sạch, Pydantic schema validation chuẩn hóa toàn bộ trường dữ liệu.' },
              { step: '03', title: 'pgvector Embeddings', desc: 'Mã hóa ngữ nghĩa kinh nghiệm và yêu cầu JD thành không gian vector đa chiều.' },
              { step: '04', title: 'Hybrid Matching', desc: 'Tính toán điểm phù hợp 0-100, chỉ rõ khoảng cách kỹ năng và xuất báo cáo AI.' },
            ].map((st, i) => (
              <div key={i} className="p-6 rounded-2xl bg-signal-navy-light/80 border border-signal-navy-border flex flex-col justify-between">
                <div>
                  <span className="font-heading font-bold text-3xl text-signal-lime block mb-4">
                    {st.step}
                  </span>
                  <h4 className="font-heading font-bold text-lg text-white mb-2">{st.title}</h4>
                  <p className="text-xs text-slate-300 leading-relaxed">{st.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Box */}
      <section className="py-20 px-4 max-w-5xl mx-auto w-full text-center">
        <div className="bg-signal-lime text-signal-navy rounded-3xl p-10 sm:p-14 shadow-signal-glow">
          <h2 className="font-heading text-3xl sm:text-5xl font-bold tracking-tight mb-4">
            Sẵn sàng nâng tầm trải nghiệm tuyển dụng của bạn?
          </h2>
          <p className="text-base sm:text-lg text-signal-navy/80 max-w-2xl mx-auto mb-8 font-medium">
            Tạo tài khoản ứng viên để nhận điểm tương thích tức thì hoặc đăng tin tuyển dụng thông minh ngay hôm nay.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
              variant="primary"
              size="lg"
              onClick={() => navigate('/register/candidate')}
            >
              Tạo hồ sơ Ứng viên miễn phí
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={() => navigate('/register/recruiter')}
            >
              Đăng ký Nhà tuyển dụng
            </Button>
          </div>
        </div>
      </section>

      {/* Mobbin / SIGNAL Style Inverse Near-Black Footer with Rounded Top Corners */}
      <footer className="mt-auto bg-signal-navy text-white rounded-t-3xl pt-16 pb-12 px-6 border-t border-signal-navy-border">
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-10 pb-12 border-b border-signal-navy-border">
          {/* Col 1 */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-full bg-signal-lime text-signal-navy flex items-center justify-center font-bold">
                <Sparkles className="w-4 h-4" />
              </div>
              <span className="font-heading font-bold text-xl text-white">HireSense AI</span>
            </div>
            <p className="text-sm text-slate-400 max-w-md leading-relaxed">
              Nghiên cứu sử dụng mô hình ngôn ngữ lớn (LLMs) và xây dựng Hệ thống tuyển dụng thông minh – Phân tích CV và Job Matching.
            </p>
            <div className="text-xs text-signal-lime font-mono">
              Designed with HireSense AI – SIGNAL Edition Aesthetics
            </div>
          </div>

          {/* Col 2 */}
          <div className="space-y-3">
            <h5 className="font-heading font-bold text-sm text-white">Dành cho Ứng viên</h5>
            <ul className="space-y-2 text-xs text-slate-400">
              <li><NavLink to="/candidate/jobs" className="hover:text-white transition-colors">Tìm kiếm việc làm</NavLink></li>
              <li><NavLink to="/candidate/cvs" className="hover:text-white transition-colors">Tải lên & Phân tích CV</NavLink></li>
              <li><NavLink to="/candidate/matching" className="hover:text-white transition-colors">Trung tâm So khớp AI</NavLink></li>
              <li><NavLink to="/candidate/applications" className="hover:text-white transition-colors">Theo dõi đơn ứng tuyển</NavLink></li>
            </ul>
          </div>

          {/* Col 3 */}
          <div className="space-y-3">
            <h5 className="font-heading font-bold text-sm text-white">Dành cho Doanh nghiệp</h5>
            <ul className="space-y-2 text-xs text-slate-400">
              <li><NavLink to="/recruiter/jobs/new" className="hover:text-white transition-colors">Đăng tin tuyển dụng</NavLink></li>
              <li><NavLink to="/recruiter/applications" className="hover:text-white transition-colors">Xếp hạng ứng viên AI</NavLink></li>
              <li><NavLink to="/recruiter/company" className="hover:text-white transition-colors">Hồ sơ Doanh nghiệp</NavLink></li>
              <li><NavLink to="/admin/dashboard" className="hover:text-white transition-colors">Cổng Quản trị viên</NavLink></li>
            </ul>
          </div>
        </div>

        <div className="max-w-7xl mx-auto pt-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-400 gap-4">
          <span>© 2026 HireSense AI. Bản quyền thuộc Đề tài Tuyển dụng Thông minh & Phân tích CV.</span>
          <div className="flex items-center gap-6">
            <span>Bảo mật dữ liệu</span>
            <span>Điều khoản dịch vụ</span>
            <span>Swagger API</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

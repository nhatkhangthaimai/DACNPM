import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../../services/api';
import { PageHeader } from '../../components/layout/PageHeader';
import { Button } from '../../components/ui/Button';
import { SkillBadge } from '../../components/ui/SkillBadge';
import { Sparkles, Plus, ArrowLeft, CheckCircle2, Building2 } from 'lucide-react';

export const CreateJobPage: React.FC = () => {
  const navigate = useNavigate();
  const [title, setTitle] = useState('');
  const [jobType, setJobType] = useState('full_time');
  const [location, setLocation] = useState('TP. Hồ Chí Minh');
  const [salaryMin, setSalaryMin] = useState('25000000');
  const [salaryMax, setSalaryMax] = useState('45000000');
  const [experienceLevel, setExperienceLevel] = useState('mid');
  const [description, setDescription] = useState('');
  const [requirements, setRequirements] = useState('');
  const [benefits, setBenefits] = useState('');

  // Skills
  const [requiredSkills, setRequiredSkills] = useState<string[]>(['ReactJS', 'TypeScript', 'Tailwind CSS', 'FastAPI']);
  const [newSkillInput, setNewSkillInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleAddSkill = (e: React.KeyboardEvent | React.MouseEvent) => {
    if (newSkillInput.trim() && !requiredSkills.includes(newSkillInput.trim())) {
      setRequiredSkills([...requiredSkills, newSkillInput.trim()]);
      setNewSkillInput('');
    }
  };

  const handleRemoveSkill = (skillToRemove: string) => {
    setRequiredSkills(requiredSkills.filter(s => s !== skillToRemove));
  };

  const handleAiSuggestSkills = () => {
    const suggestions = ['Docker', 'PostgreSQL', 'pgvector', 'Microservices', 'RESTful API', 'Git'];
    const merged = Array.from(new Set([...requiredSkills, ...suggestions]));
    setRequiredSkills(merged);
  };

  const handleSubmit = async (status: 'published' | 'draft' | 'pending_approval') => {
    if (!title || !description || !requirements) {
      alert('Vui lòng điền đầy đủ Tiêu đề, Mô tả và Yêu cầu công việc.');
      return;
    }

    setIsSubmitting(true);
    await apiService.createJob({
      title,
      jobType: jobType as any,
      location,
      salaryMin: Number(salaryMin),
      salaryMax: Number(salaryMax),
      experienceLevel: experienceLevel as any,
      description,
      requirements,
      benefits,
      status,
      requiredSkills,
      preferredSkills: ['Docker', 'CI/CD'],
    });
    setIsSubmitting(false);
    navigate('/recruiter/jobs');
  };

  return (
    <div className="space-y-6 max-w-4xl">
      <div className="flex items-center gap-2 mb-2">
        <button
          onClick={() => navigate('/recruiter/jobs')}
          className="inline-flex items-center gap-1.5 text-xs text-signal-slate hover:text-signal-navy font-semibold"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> Quay lại danh sách tin
        </button>
      </div>

      <PageHeader
        title="Đăng Tin Tuyển dụng Mới (JD)"
        subtitle="Hệ thống sẽ tự động đối sánh kỹ năng và lập chỉ mục Vector Embedding bằng Gemini AI để tối ưu ứng viên phù hợp."
      />

      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/80 shadow-sm space-y-6">
        <div>
          <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
            Tiêu đề Vị trí tuyển dụng *
          </label>
          <input
            type="text"
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Ví dụ: Senior Backend Developer (Python / FastAPI)"
            className="w-full bg-signal-offwhite text-sm font-semibold rounded-xl px-4 py-3 border border-slate-200 focus:outline-none focus:border-signal-navy focus:bg-white"
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
              Hình thức làm việc
            </label>
            <select
              value={jobType}
              onChange={(e) => setJobType(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            >
              <option value="full_time">Toàn thời gian (Full-time)</option>
              <option value="hybrid">Hybrid (Linh hoạt)</option>
              <option value="remote">Làm việc từ xa (Remote)</option>
              <option value="part_time">Bán thời gian</option>
              <option value="internship">Thực tập sinh</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
              Địa điểm làm việc
            </label>
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="TP. Hồ Chí Minh"
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
              Cấp bậc kinh nghiệm
            </label>
            <select
              value={experienceLevel}
              onChange={(e) => setExperienceLevel(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            >
              <option value="entry">Entry / Fresher</option>
              <option value="junior">Junior (1-2 năm)</option>
              <option value="mid">Middle (2-4 năm)</option>
              <option value="senior">Senior (4+ năm)</option>
              <option value="lead">Lead / Architect</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
              Mức lương tối thiểu (VND)
            </label>
            <input
              type="number"
              value={salaryMin}
              onChange={(e) => setSalaryMin(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
              Mức lương tối đa (VND)
            </label>
            <input
              type="number"
              value={salaryMax}
              onChange={(e) => setSalaryMax(e.target.value)}
              className="w-full bg-signal-offwhite text-sm rounded-xl px-4 py-2.5 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
          </div>
        </div>

        {/* AI Skills Selector */}
        <div className="p-5 rounded-2xl bg-signal-offwhite border border-slate-200/80 space-y-3">
          <div className="flex items-center justify-between">
            <label className="block text-xs font-semibold uppercase text-signal-navy">
              Kỹ năng yêu cầu bắt buộc (Hard Skills)
            </label>
            <button
              type="button"
              onClick={handleAiSuggestSkills}
              className="inline-flex items-center gap-1.5 text-xs font-bold text-[#5942be] hover:underline"
            >
              <Sparkles className="w-3.5 h-3.5" />
              AI Gợi ý kỹ năng tự động
            </button>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="text"
              value={newSkillInput}
              onChange={(e) => setNewSkillInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSkill(e))}
              placeholder="Nhập kỹ năng rồi bấm Thêm (e.g. PyTorch, Docker)..."
              className="flex-1 bg-white text-xs rounded-xl px-4 py-2 border border-slate-200 focus:outline-none focus:border-signal-navy"
            />
            <Button type="button" variant="soft" size="sm" onClick={handleAddSkill}>
              Thêm
            </Button>
          </div>

          <div className="flex flex-wrap gap-2 pt-1">
            {requiredSkills.map((sk) => (
              <SkillBadge
                key={sk}
                name={sk}
                variant="default"
                onRemove={() => handleRemoveSkill(sk)}
              />
            ))}
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
            Mô tả công việc (Job Description) *
          </label>
          <textarea
            rows={4}
            required
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Mô tả trách nhiệm cốt lõi, dự án tham gia, quy mô nhóm..."
            className="w-full bg-signal-offwhite text-sm rounded-xl p-3 border border-slate-200 focus:outline-none focus:border-signal-navy"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
            Yêu cầu ứng viên (Requirements) *
          </label>
          <textarea
            rows={4}
            required
            value={requirements}
            onChange={(e) => setRequirements(e.target.value)}
            placeholder="Yêu cầu về năm kinh nghiệm, học vấn, kỹ năng chuyên sâu..."
            className="w-full bg-signal-offwhite text-sm rounded-xl p-3 border border-slate-200 focus:outline-none focus:border-signal-navy"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold uppercase text-signal-slate mb-1.5">
            Chế độ đãi ngộ & Quyền lợi (Benefits)
          </label>
          <textarea
            rows={3}
            value={benefits}
            onChange={(e) => setBenefits(e.target.value)}
            placeholder="Thưởng KPI, bảo hiểm sức khỏe quốc tế, trang thiết bị làm việc..."
            className="w-full bg-signal-offwhite text-sm rounded-xl p-3 border border-slate-200 focus:outline-none focus:border-signal-navy"
          />
        </div>

        <div className="pt-6 border-t border-slate-100 flex items-center justify-between">
          <Button
            type="button"
            variant="ghost"
            onClick={() => handleSubmit('draft')}
          >
            Lưu bản nháp
          </Button>

          <div className="flex items-center gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/recruiter/jobs')}
            >
              Hủy bỏ
            </Button>
            <Button
              type="button"
              variant="lime"
              isLoading={isSubmitting}
              onClick={() => handleSubmit('published')}
              icon={<Sparkles className="w-4 h-4 text-signal-navy" />}
            >
              Xuất bản tin JD ngay
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

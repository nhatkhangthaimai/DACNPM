import React from 'react';
import { MatchScoreBreakdown } from '../../types';
import { MatchScoreRing } from './MatchScoreRing';
import { SkillBadge } from './SkillBadge';
import { Sparkles, AlertCircle, CheckCircle2, TrendingUp, BookOpen } from 'lucide-react';

interface SkillGapPanelProps {
  breakdown: MatchScoreBreakdown;
  jobTitle?: string;
  candidateName?: string;
}

export const SkillGapPanel: React.FC<SkillGapPanelProps> = ({
  breakdown,
  jobTitle,
  candidateName,
}) => {
  // Normalize breakdown defensively to guarantee arrays and numbers exist
  const raw = breakdown as any || {};
  const overallScore = Math.max(0, Math.min(100, Math.round(Number(breakdown?.overallScore ?? raw.overall_score ?? 0))));
  const hardSkillsScore = Math.max(0, Math.min(100, Math.round(Number(breakdown?.hardSkillsScore ?? raw.hard_skills_score ?? 0))));
  const semanticScore = Math.max(0, Math.min(100, Math.round(Number(breakdown?.semanticScore ?? raw.semantic_score ?? 0))));
  const experienceScore = Math.max(0, Math.min(100, Math.round(Number(breakdown?.experienceScore ?? raw.experience_score ?? 0))));

  const matchedSkills: string[] = Array.isArray(breakdown?.matchedSkills)
    ? breakdown.matchedSkills
    : Array.isArray(raw.matched_skills)
    ? raw.matched_skills
    : [];

  const missingRequiredSkills: string[] = Array.isArray(breakdown?.missingRequiredSkills)
    ? breakdown.missingRequiredSkills
    : Array.isArray(raw.missing_required_skills)
    ? raw.missing_required_skills
    : [];

  const missingPreferredSkills: string[] = Array.isArray(breakdown?.missingPreferredSkills)
    ? breakdown.missingPreferredSkills
    : Array.isArray(raw.missing_preferred_skills)
    ? raw.missing_preferred_skills
    : [];

  const aiExplanation = breakdown?.aiExplanation || raw.ai_explanation || 'Hệ thống đã phân tích hồ sơ và đưa ra đánh giá tương thích.';
  const recommendations: string[] = Array.isArray(breakdown?.recommendations)
    ? breakdown.recommendations
    : Array.isArray(raw.recommendations)
    ? raw.recommendations
    : [];

  return (
    <div className="bg-white rounded-2xl border border-slate-200/80 p-6 md:p-8 shadow-sm space-y-6">
      {/* Header with Overall Score & Summary */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-6 pb-6 border-b border-slate-100">
        <div className="flex items-center gap-5">
          <MatchScoreRing score={overallScore} size={110} />
          <div>
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-signal-lime/20 text-[#557512] text-xs font-semibold uppercase tracking-wider mb-2">
              <Sparkles className="w-3.5 h-3.5" />
              AI Match Analysis
            </div>
            <h3 className="font-heading text-xl font-bold text-signal-navy">
              {jobTitle ? `Độ tương thích với ${jobTitle}` : 'Đánh giá độ phù hợp tổng thể'}
            </h3>
            <p className="text-sm text-signal-slate mt-1">
              {candidateName ? `Hồ sơ của: ${candidateName}` : 'Dựa trên phân tích ngữ nghĩa và trọng số kỹ năng thực tế'}
            </p>
          </div>
        </div>

        {/* Sub-scores */}
        <div className="grid grid-cols-3 gap-3 w-full md:w-auto">
          <div className="bg-signal-offwhite rounded-xl p-3 text-center border border-slate-100">
            <span className="text-xs text-signal-slate font-medium block">Hard Skills</span>
            <span className="font-heading font-bold text-lg text-signal-navy">{hardSkillsScore}%</span>
          </div>
          <div className="bg-signal-offwhite rounded-xl p-3 text-center border border-slate-100">
            <span className="text-xs text-signal-slate font-medium block">Ngữ nghĩa</span>
            <span className="font-heading font-bold text-lg text-signal-navy">{semanticScore}%</span>
          </div>
          <div className="bg-signal-offwhite rounded-xl p-3 text-center border border-slate-100">
            <span className="text-xs text-signal-slate font-medium block">Kinh nghiệm</span>
            <span className="font-heading font-bold text-lg text-signal-navy">{experienceScore}%</span>
          </div>
        </div>
      </div>

      {/* Skills Matrix (Matched vs Missing) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Matched Skills */}
        <div className="bg-emerald-50/50 rounded-xl p-5 border border-emerald-100">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            <h4 className="font-heading font-semibold text-signal-navy text-sm">
              Kỹ năng đã đáp ứng ({matchedSkills.length})
            </h4>
          </div>
          <div className="flex flex-wrap gap-2">
            {matchedSkills.length > 0 ? (
              matchedSkills.map((skill, idx) => (
                <SkillBadge key={idx} name={skill} variant="matched" />
              ))
            ) : (
              <span className="text-xs text-slate-500 italic">Chưa tìm thấy kỹ năng trùng khớp</span>
            )}
          </div>
        </div>

        {/* Missing Skills */}
        <div className="bg-rose-50/50 rounded-xl p-5 border border-rose-100">
          <div className="flex items-center gap-2 mb-3">
            <AlertCircle className="w-5 h-5 text-rose-600" />
            <h4 className="font-heading font-semibold text-signal-navy text-sm">
              Khoảng cách kỹ năng cần bổ sung ({missingRequiredSkills.length + missingPreferredSkills.length})
            </h4>
          </div>
          <div className="space-y-3">
            {missingRequiredSkills.length > 0 && (
              <div>
                <span className="text-xs font-semibold text-rose-700 block mb-1.5 uppercase tracking-wide">
                  Bắt buộc (Required):
                </span>
                <div className="flex flex-wrap gap-2">
                  {missingRequiredSkills.map((skill, idx) => (
                    <SkillBadge key={idx} name={skill} variant="missing-required" />
                  ))}
                </div>
              </div>
            )}
            {missingPreferredSkills.length > 0 && (
              <div>
                <span className="text-xs font-semibold text-amber-700 block mb-1.5 uppercase tracking-wide">
                  Ưu tiên thêm (Preferred):
                </span>
                <div className="flex flex-wrap gap-2">
                  {missingPreferredSkills.map((skill, idx) => (
                    <SkillBadge key={idx} name={skill} variant="missing-preferred" />
                  ))}
                </div>
              </div>
            )}
            {missingRequiredSkills.length === 0 && missingPreferredSkills.length === 0 && (
              <span className="text-xs text-emerald-700 font-medium">
                Tuyệt vời! Ứng viên đáp ứng đầy đủ tất cả kỹ năng được liệt kê trong tin tuyển dụng.
              </span>
            )}
          </div>
        </div>
      </div>

      {/* AI Explanation Callout */}
      <div className="bg-signal-navy text-white rounded-xl p-5 border border-signal-navy-border relative overflow-hidden">
        <div className="absolute top-0 right-0 w-32 h-32 bg-signal-lavender/10 rounded-full blur-2xl pointer-events-none" />
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-signal-lavender/20 text-signal-lavender shrink-0 mt-0.5">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h5 className="font-heading font-bold text-sm text-signal-lime mb-1">
              Nhận định từ HireSense AI Reasoning Engine
            </h5>
            <p className="text-sm text-slate-300 leading-relaxed">
              {aiExplanation}
            </p>
          </div>
        </div>
      </div>

      {/* Personalized Recommendations Roadmap */}
      {recommendations.length > 0 && (
        <div className="pt-2">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-4 h-4 text-signal-navy" />
            <h4 className="font-heading font-semibold text-signal-navy text-sm">
              Lộ trình đề xuất cải thiện hồ sơ (Learning Recommendations)
            </h4>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {recommendations.map((rec, idx) => (
              <div
                key={idx}
                className="flex items-start gap-3 p-3.5 rounded-xl bg-signal-offwhite border border-slate-200/80 text-sm text-signal-navy"
              >
                <div className="w-5 h-5 rounded-full bg-signal-lime flex items-center justify-center font-bold text-xs text-signal-navy shrink-0 mt-0.5">
                  {idx + 1}
                </div>
                <span>{rec}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

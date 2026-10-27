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
  return (
    <div className="bg-white rounded-2xl border border-slate-200/80 p-6 md:p-8 shadow-sm space-y-6">
      {/* Header with Overall Score & Summary */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-6 pb-6 border-b border-slate-100">
        <div className="flex items-center gap-5">
          <MatchScoreRing score={breakdown.overallScore} size={110} />
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
            <span className="font-heading font-bold text-lg text-signal-navy">{breakdown.hardSkillsScore}%</span>
          </div>
          <div className="bg-signal-offwhite rounded-xl p-3 text-center border border-slate-100">
            <span className="text-xs text-signal-slate font-medium block">Ngữ nghĩa</span>
            <span className="font-heading font-bold text-lg text-signal-navy">{breakdown.semanticScore}%</span>
          </div>
          <div className="bg-signal-offwhite rounded-xl p-3 text-center border border-slate-100">
            <span className="text-xs text-signal-slate font-medium block">Kinh nghiệm</span>
            <span className="font-heading font-bold text-lg text-signal-navy">{breakdown.experienceScore}%</span>
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
              Kỹ năng đã đáp ứng ({breakdown.matchedSkills.length})
            </h4>
          </div>
          <div className="flex flex-wrap gap-2">
            {breakdown.matchedSkills.length > 0 ? (
              breakdown.matchedSkills.map((skill, idx) => (
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
              Khoảng cách kỹ năng cần bổ sung ({breakdown.missingRequiredSkills.length + breakdown.missingPreferredSkills.length})
            </h4>
          </div>
          <div className="space-y-3">
            {breakdown.missingRequiredSkills.length > 0 && (
              <div>
                <span className="text-xs font-semibold text-rose-700 block mb-1.5 uppercase tracking-wide">
                  Bắt buộc (Required):
                </span>
                <div className="flex flex-wrap gap-2">
                  {breakdown.missingRequiredSkills.map((skill, idx) => (
                    <SkillBadge key={idx} name={skill} variant="missing-required" />
                  ))}
                </div>
              </div>
            )}
            {breakdown.missingPreferredSkills.length > 0 && (
              <div>
                <span className="text-xs font-semibold text-amber-700 block mb-1.5 uppercase tracking-wide">
                  Ưu tiên thêm (Preferred):
                </span>
                <div className="flex flex-wrap gap-2">
                  {breakdown.missingPreferredSkills.map((skill, idx) => (
                    <SkillBadge key={idx} name={skill} variant="missing-preferred" />
                  ))}
                </div>
              </div>
            )}
            {breakdown.missingRequiredSkills.length === 0 && breakdown.missingPreferredSkills.length === 0 && (
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
              {breakdown.aiExplanation}
            </p>
          </div>
        </div>
      </div>

      {/* Personalized Recommendations Roadmap */}
      {breakdown.recommendations.length > 0 && (
        <div className="pt-2">
          <div className="flex items-center gap-2 mb-3">
            <TrendingUp className="w-4 h-4 text-signal-navy" />
            <h4 className="font-heading font-semibold text-signal-navy text-sm">
              Lộ trình đề xuất cải thiện hồ sơ (Learning Recommendations)
            </h4>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {breakdown.recommendations.map((rec, idx) => (
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

import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import { CV } from '../../types';
import { useAuth } from '../../context/AuthContext';
import { PageHeader } from '../../components/layout/PageHeader';
import { FileUploadZone } from '../../components/ui/FileUploadZone';
import { Button } from '../../components/ui/Button';
import { Modal } from '../../components/ui/Modal';
import { SkillBadge, StatusBadge } from '../../components/ui/SkillBadge';
import {
  FileText,
  Trash2,
  Star,
  Sparkles,
  GraduationCap,
  Briefcase,
  CheckCircle2,
  Calendar,
  Award,
  Globe,
  Edit3
} from 'lucide-react';

export const CVManagement: React.FC = () => {
  const { user } = useAuth();
  const [cvs, setCvs] = useState<CV[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedCVForReview, setSelectedCVForReview] = useState<CV | null>(null);
  const [cvToDelete, setCvToDelete] = useState<CV | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    loadCVs();
  }, []);

  const loadCVs = () => {
    apiService.getCandidateCVs(user?.id || 'user-cand-1').then(setCvs);
  };

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    try {
      const newCv = await apiService.uploadAndAnalyzeCV(file, user?.id || 'user-cand-1');
      setCvs(prev => [newCv, ...prev]);
      setSelectedCVForReview(newCv);
    } finally {
      setIsUploading(false);
    }
  };

  const confirmDelete = async () => {
    if (!cvToDelete) return;
    setIsDeleting(true);
    const targetId = cvToDelete.id;
    setCvs(prev => prev.filter(c => c.id !== targetId));
    try {
      await apiService.deleteCV(targetId);
    } catch (err) {
      console.error('Lỗi khi xóa CV:', err);
    } finally {
      setIsDeleting(false);
      setCvToDelete(null);
      loadCVs();
    }
  };

  const handleSetPrimary = async (id: string) => {
    setCvs(prev => prev.map(c => ({ ...c, isPrimary: c.id === id })));
    try {
      await apiService.setPrimaryCV(id);
    } catch (err) {
      console.error('Lỗi khi đặt CV chính:', err);
    }
    loadCVs();
  };


  return (
    <div className="space-y-8">
      <PageHeader
        title="Quản lý Hồ sơ & Phân tích CV bằng AI"
        subtitle="Hệ thống tự động đọc văn bản và sử dụng Gemini LLM để bóc tách thông tin có cấu trúc, phát hiện kỹ năng và phục vụ so khớp công việc."
      />

      {/* Upload Zone */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200/80 shadow-sm">
        <h3 className="font-heading font-bold text-lg text-signal-navy mb-2 flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-signal-lime" />
          Tải lên CV mới để phân tích tự động
        </h3>
        <p className="text-xs text-amber-700 bg-amber-50 border border-amber-200 rounded-xl px-4 py-2.5 mb-4">
          ⚠️ <strong>Lưu ý:</strong> Hệ thống sử dụng PyMuPDF và python-docx để đọc dữ liệu thực tế. Vui lòng tải lên tệp <strong>.pdf</strong> (có text layer) hoặc <strong>.docx</strong> chuẩn. Không tải bản scan/ảnh chưa có OCR.
        </p>
        <FileUploadZone
          onFileUploaded={handleUpload}
          isUploading={isUploading}
        />
      </div>

      {/* List of Candidate CVs */}
      <div className="space-y-4">
        <h3 className="font-heading font-bold text-xl text-signal-navy">
          Danh sách CV đã tải lên ({cvs.length})
        </h3>

        <div className="grid grid-cols-1 gap-4">
          {cvs.map((cv) => (
            <div
              key={cv.id}
              className={`p-6 rounded-2xl border transition-all duration-200 bg-white ${
                cv.isPrimary
                  ? 'border-signal-lime ring-1 ring-signal-lime shadow-sm'
                  : 'border-slate-200 hover:border-slate-300'
              } flex flex-col md:flex-row items-start md:items-center justify-between gap-6`}
            >
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-2xl bg-signal-offwhite text-signal-navy border border-slate-200 flex items-center justify-center shrink-0">
                  <FileText className="w-6 h-6" />
                </div>
                <div>
                  <div className="flex items-center gap-2.5 mb-1">
                    <h4 className="font-heading font-bold text-base text-signal-navy">
                      {cv.fileName}
                    </h4>
                    {cv.isPrimary && (
                      <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-signal-lime text-signal-navy">
                        CV Chính
                      </span>
                    )}
                    <StatusBadge status={cv.extractionStatus} />
                  </div>
                  <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-signal-slate">
                    <span>Dung lượng: {(cv.fileSize / 1024).toFixed(1)} KB</span>
                    <span>Tải lên: {new Date(cv.createdAt).toLocaleDateString('vi-VN')}</span>
                    {(cv.extractionStatus === 'failed' || cv.extractionStatus === 'extraction_failed') ? (
                      <span className="text-rose-600 font-semibold block w-full mt-1">
                        ⚠️ Không thể đọc nội dung CV. Vui lòng tải lên file PDF/DOCX hợp lệ hoặc thử một file khác.
                      </span>
                    ) : (
                      cv.parsedData && (
                        <span className="text-signal-navy font-semibold">
                          Đã trích xuất {cv.parsedData.hardSkills.length} hard skills · {cv.parsedData.experience.length} công ty
                        </span>
                      )
                    )}
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-2.5 w-full md:w-auto justify-end pt-4 md:pt-0 border-t md:border-t-0 border-slate-100">
                <Button
                  variant="outline"
                  size="sm"
                  icon={<Sparkles className="w-3.5 h-3.5 text-signal-navy" />}
                  onClick={() => setSelectedCVForReview(cv)}
                >
                  Xem dữ liệu AI
                </Button>

                {!cv.isPrimary && (
                  <Button
                    variant="soft"
                    size="sm"
                    icon={<Star className="w-3.5 h-3.5" />}
                    onClick={() => handleSetPrimary(cv.id)}
                  >
                    Đặt làm chính
                  </Button>
                )}

                <button
                  type="button"
                  onClick={() => setCvToDelete(cv)}
                  className="p-2.5 rounded-full text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                  title="Xóa CV"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Review Extracted Data Modal */}
      <Modal
        isOpen={!!selectedCVForReview}
        onClose={() => setSelectedCVForReview(null)}
        title="Dữ liệu Trích xuất bởi Gemini AI"
        subtitle={`Tệp: ${selectedCVForReview?.fileName} · Kiểm tra và xác thực thông tin`}
        maxWidth="2xl"
      >
        {selectedCVForReview && (
          <div className="space-y-6">
            {(selectedCVForReview.extractionStatus === 'failed' || selectedCVForReview.extractionStatus === 'extraction_failed') ? (
              <div className="bg-rose-50 border border-rose-200 rounded-2xl p-6 space-y-4">
                <div className="flex items-center gap-2.5 text-rose-800 font-bold text-base">
                  <span className="w-2.5 h-2.5 rounded-full bg-rose-600 animate-pulse" />
                  <span>Trích xuất nội dung thất bại</span>
                </div>
                <p className="text-sm text-rose-700 leading-relaxed font-medium">
                  Không thể đọc nội dung CV. Vui lòng tải lên file PDF/DOCX hợp lệ hoặc thử một file khác.
                </p>
                {selectedCVForReview.extractionError && (
                  <div className="text-xs text-rose-700 bg-white/80 p-3 rounded-xl border border-rose-200 font-mono">
                    <strong>Chi tiết lỗi:</strong> {selectedCVForReview.extractionError}
                  </div>
                )}
                <div className="pt-2 flex items-center justify-between">
                  <span className="text-xs text-slate-500">Mã lỗi: CV_EXTRACTION_FAILED</span>
                  <Button
                    variant="primary"
                    size="sm"
                    onClick={() => {
                      setSelectedCVForReview(null);
                      window.scrollTo({ top: 0, behavior: 'smooth' });
                    }}
                  >
                    Tải lại tệp khác
                  </Button>
                </div>
              </div>
            ) : (
              selectedCVForReview.parsedData && (
                <>
                  {/* Header info */}
                  <div className="bg-signal-offwhite rounded-2xl p-5 border border-slate-200">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div>
                        <h4 className="font-heading font-bold text-xl text-signal-navy">
                          {selectedCVForReview.parsedData.fullName || 'Chưa xác định tên'}
                        </h4>
                        <div className="flex flex-wrap items-center gap-4 text-xs text-signal-slate mt-1">
                          <span>Email: {selectedCVForReview.parsedData.email || 'N/A'}</span>
                          <span>Số điện thoại: {selectedCVForReview.parsedData.phone || 'N/A'}</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-bold">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                          Schema Validated
                        </span>
                        {selectedCVForReview.contentValidated && (
                          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-50 text-blue-800 border border-blue-200 text-xs font-bold">
                            <CheckCircle2 className="w-3.5 h-3.5 text-blue-600" />
                            Content Validated
                          </span>
                        )}
                      </div>
                    </div>

                    {selectedCVForReview.parsedData.summary && (
                      <p className="text-sm text-slate-600 mt-3 pt-3 border-t border-slate-200/80 leading-relaxed">
                        {selectedCVForReview.parsedData.summary}
                      </p>
                    )}
                  </div>

            {/* Skills Matrix */}
            <div>
              <h4 className="font-heading font-bold text-sm text-signal-navy uppercase tracking-wider mb-3">
                Kỹ năng chuyên môn trích xuất (Hard & Soft Skills)
              </h4>
              <div className="space-y-3">
                <div>
                  <span className="text-xs font-semibold text-signal-slate block mb-1.5">
                    Hard Skills ({selectedCVForReview.parsedData.hardSkills.length}):
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {selectedCVForReview.parsedData.hardSkills.map((sk, i) => (
                      <SkillBadge key={i} name={sk} variant="default" />
                    ))}
                  </div>
                </div>
                <div>
                  <span className="text-xs font-semibold text-signal-slate block mb-1.5">
                    Soft Skills ({selectedCVForReview.parsedData.softSkills.length}):
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {selectedCVForReview.parsedData.softSkills.map((sk, i) => (
                      <SkillBadge key={i} name={sk} variant="lavender" />
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Experience records */}
            <div>
              <h4 className="font-heading font-bold text-sm text-signal-navy uppercase tracking-wider mb-3 flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-signal-navy" />
                Lịch sử kinh nghiệm công tác ({selectedCVForReview.parsedData.experience.length})
              </h4>
              <div className="space-y-3">
                {selectedCVForReview.parsedData.experience.map((exp, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-signal-offwhite border border-slate-200/80">
                    <div className="flex items-center justify-between font-bold text-sm text-signal-navy mb-1">
                      <span>{exp.jobTitle}</span>
                      <span className="text-xs font-medium text-signal-slate">
                        {exp.startDate} - {exp.endDate || (exp.isCurrent ? 'Hiện tại' : '')}
                      </span>
                    </div>
                    <span className="text-xs text-signal-slate block mb-2 font-medium">
                      {exp.companyName}
                    </span>
                    {exp.description && (
                      <p className="text-xs text-slate-600 leading-relaxed">{exp.description}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Education records */}
            <div>
              <h4 className="font-heading font-bold text-sm text-signal-navy uppercase tracking-wider mb-3 flex items-center gap-2">
                <GraduationCap className="w-4 h-4 text-signal-navy" />
                Học vấn & Bằng cấp
              </h4>
              <div className="space-y-2">
                {selectedCVForReview.parsedData.education.map((edu, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-signal-offwhite border border-slate-200/80 flex items-center justify-between">
                    <div>
                      <span className="font-bold text-sm text-signal-navy block">
                        {edu.institution}
                      </span>
                      <span className="text-xs text-signal-slate">
                        {edu.degree} · Chuyên ngành: {edu.fieldOfStudy}
                      </span>
                    </div>
                    {edu.gpa && (
                      <span className="text-xs font-bold px-2.5 py-1 rounded-full bg-signal-mint/20 text-[#1b7a66]">
                        GPA: {edu.gpa}
                      </span>
                    )}
                  </div>
                ))}
              </div>
            </div>

            <div className="pt-6 border-t border-slate-100 flex items-center justify-end">
              <Button
                variant="primary"
                onClick={() => setSelectedCVForReview(null)}
              >
                Xác nhận & Đóng
              </Button>
            </div>
          </>
        )
      )}
    </div>
  )}
</Modal>

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={!!cvToDelete}
        onClose={() => setCvToDelete(null)}
        title="Xác nhận xóa tệp CV"
        maxWidth="md"
      >
        {cvToDelete && (
          <div className="space-y-4">
            <p className="text-sm text-slate-600">
              Bạn có chắc chắn muốn xóa tệp CV <strong className="text-signal-navy font-bold">{cvToDelete.fileName}</strong> khỏi hệ thống?
            </p>
            <div className="text-xs text-rose-700 bg-rose-50 border border-rose-200 rounded-xl p-3">
              ⚠️ <strong>Lưu ý:</strong> Hành động này sẽ xóa vĩnh viễn tệp CV và các kết quả so khớp AI liên quan khỏi cơ sở dữ liệu.
            </div>
            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCvToDelete(null)}
                disabled={isDeleting}
              >
                Hủy bỏ
              </Button>
              <Button
                variant="primary"
                size="sm"
                className="bg-rose-600 hover:bg-rose-700 text-white border-transparent"
                icon={<Trash2 className="w-4 h-4" />}
                isLoading={isDeleting}
                onClick={confirmDelete}
              >
                Xác nhận Xóa
              </Button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

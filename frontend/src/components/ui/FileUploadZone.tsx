import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';

interface FileUploadZoneProps {
  onFileUploaded: (file: File) => Promise<void>;
  isUploading?: boolean;
}

export const FileUploadZone: React.FC<FileUploadZoneProps> = ({
  onFileUploaded,
  isUploading = false,
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateAndProcessFile = async (file: File) => {
    setErrorMessage(null);
    const validExtensions = ['pdf', 'docx', 'doc'];
    const ext = file.name.split('.').pop()?.toLowerCase() || '';

    if (!validExtensions.includes(ext)) {
      setErrorMessage('Định dạng tệp không được hỗ trợ. Vui lòng tải lên tệp PDF hoặc DOCX.');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setErrorMessage('Kích thước tệp vượt quá giới hạn 10MB.');
      return;
    }

    setSelectedFileName(file.name);
    try {
      await onFileUploaded(file);
    } catch {
      setErrorMessage('Có lỗi xảy ra trong quá trình xử lý tệp.');
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndProcessFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndProcessFile(e.target.files[0]);
    }
  };

  return (
    <div className="w-full">
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200 ${
          isDragOver
            ? 'border-signal-lime bg-signal-lime/5 scale-[1.01]'
            : 'border-slate-300 hover:border-signal-navy/50 bg-white hover:bg-slate-50/50'
        } ${isUploading ? 'pointer-events-none opacity-80' : ''}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.doc"
          onChange={handleFileChange}
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-signal-offwhite border border-slate-200 flex items-center justify-center text-signal-navy">
            {isUploading ? (
              <Loader2 className="w-8 h-8 text-signal-navy animate-spin" />
            ) : selectedFileName ? (
              <FileText className="w-8 h-8 text-signal-navy" />
            ) : (
              <UploadCloud className="w-8 h-8 text-signal-navy" />
            )}
          </div>

          <div>
            <h4 className="font-heading font-semibold text-lg text-signal-navy">
              {isUploading
                ? 'Đang phân tích CV với Gemini AI Pipeline...'
                : selectedFileName
                ? selectedFileName
                : 'Kéo thả tệp CV hoặc Nhấp để chọn tệp'}
            </h4>
            <p className="text-sm text-signal-slate mt-1">
              Hỗ trợ định dạng PDF, DOCX dung lượng tối đa 10MB
            </p>
          </div>

          {!isUploading && !selectedFileName && (
            <span className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-signal-navy text-white text-sm font-semibold hover:bg-signal-navy-light transition-colors shadow-sm">
              Chọn tệp từ máy tính
            </span>
          )}

          {isUploading && (
            <div className="w-full max-w-xs space-y-2">
              <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-signal-lime animate-pulse w-3/4 rounded-full" />
              </div>
              <p className="text-xs text-signal-slate">
                Trích xuất học vấn, kinh nghiệm và kỹ năng tự động...
              </p>
            </div>
          )}
        </div>
      </div>

      {errorMessage && (
        <div className="mt-3 flex items-center gap-2 text-sm text-rose-600 bg-rose-50 p-3 rounded-xl border border-rose-100">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}
    </div>
  );
};

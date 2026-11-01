import React, { useState, useRef } from 'react';
import { 
  UploadCloud, 
  FileText, 
  AlertCircle, 
  Loader2, 
  Image as ImageIcon, 
  Camera, 
  FolderOpen, 
  X,
  CheckCircle2
} from 'lucide-react';

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
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isImageFile, setIsImageFile] = useState(false);

  // Hidden file inputs for specific device triggers
  const generalInputRef = useRef<HTMLInputElement>(null);
  const photoLibraryInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const documentInputRef = useRef<HTMLInputElement>(null);

  const validateAndProcessFile = async (file: File) => {
    setErrorMessage(null);
    const validDocExtensions = ['pdf', 'docx', 'doc'];
    const validImageExtensions = ['jpg', 'jpeg', 'png', 'webp', 'heic', 'heif'];
    const allValid = [...validDocExtensions, ...validImageExtensions];

    const ext = file.name.split('.').pop()?.toLowerCase() || '';
    const isImg = validImageExtensions.includes(ext) || file.type.startsWith('image/');

    if (!allValid.includes(ext) && !isImg) {
      setErrorMessage('Định dạng tệp không được hỗ trợ. Vui lòng tải lên tệp PDF, DOCX hoặc ảnh CV (JPG, PNG, WEBP, HEIC).');
      return;
    }

    // Size limit: 10MB for documents, 15MB for high-res mobile camera photos
    const maxMb = isImg ? 15 : 10;
    if (file.size > maxMb * 1024 * 1024) {
      setErrorMessage(`Kích thước tệp vượt quá giới hạn cho phép ${maxMb}MB.`);
      return;
    }

    if (file.size === 0) {
      setErrorMessage('Tệp tải lên rỗng (0 bytes). Vui lòng chọn tệp hợp lệ.');
      return;
    }

    setSelectedFileName(file.name);
    setIsImageFile(isImg);

    // Create thumbnail preview for image files
    if (isImg) {
      try {
        const objUrl = URL.createObjectURL(file);
        setPreviewUrl(objUrl);
      } catch {
        setPreviewUrl(null);
      }
    } else {
      setPreviewUrl(null);
    }

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
    // Reset value so the user can re-select the same file if needed
    e.target.value = '';
  };

  const handleReset = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedFileName(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }
    setIsImageFile(false);
    setErrorMessage(null);
  };

  return (
    <div className="w-full space-y-3">
      {/* Hidden Inputs for different mobile actions */}
      {/* 1. General Input: Accepts both documents and images */}
      <input
        ref={generalInputRef}
        type="file"
        accept=".pdf,.docx,.doc,.jpg,.jpeg,.png,.webp,.heic,.heif,image/jpeg,image/png,image/webp,image/heic,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        onChange={handleFileChange}
        className="hidden"
      />
      {/* 2. Photo Library Input: Strictly for photos (NEVER uses capture, so iOS/Android opens Photo Library/Gallery) */}
      <input
        ref={photoLibraryInputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp,image/heic,.jpg,.jpeg,.png,.webp,.heic,.heif"
        onChange={handleFileChange}
        className="hidden"
      />
      {/* 3. Camera Capture Input: For instant camera photo of a paper CV */}
      <input
        ref={cameraInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleFileChange}
        className="hidden"
      />
      {/* 4. Document Browser Input: Specifically for PDFs & DOCXs */}
      <input
        ref={documentInputRef}
        type="file"
        accept=".pdf,.docx,.doc,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        onChange={handleFileChange}
        className="hidden"
      />

      {/* Main Drag & Drop / Click Zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => !isUploading && generalInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-3xl p-6 sm:p-8 text-center cursor-pointer transition-all duration-200 ${
          isDragOver
            ? 'border-signal-lime bg-signal-lime/5 scale-[1.01]'
            : 'border-slate-300 hover:border-signal-navy/50 bg-white hover:bg-slate-50/50 shadow-sm'
        } ${isUploading ? 'pointer-events-none opacity-80' : ''}`}
      >
        <div className="flex flex-col items-center justify-center space-y-4">
          {/* Icon or Image Preview */}
          {previewUrl ? (
            <div className="relative group">
              <div className="w-24 h-32 rounded-xl overflow-hidden border-2 border-signal-lime shadow-md bg-slate-100 flex items-center justify-center">
                <img 
                  src={previewUrl} 
                  alt="Ảnh CV xem trước" 
                  className="w-full h-full object-cover" 
                />
              </div>
              {!isUploading && (
                <button
                  type="button"
                  onClick={handleReset}
                  className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-rose-500 text-white flex items-center justify-center shadow hover:bg-rose-600 transition-colors"
                  title="Xóa và chọn lại"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          ) : (
            <div className="w-16 h-16 rounded-2xl bg-signal-offwhite border border-slate-200 flex items-center justify-center text-signal-navy shadow-inner">
              {isUploading ? (
                <Loader2 className="w-8 h-8 text-signal-navy animate-spin" />
              ) : selectedFileName ? (
                <FileText className="w-8 h-8 text-signal-navy" />
              ) : (
                <UploadCloud className="w-8 h-8 text-signal-navy" />
              )}
            </div>
          )}

          {/* Title & Description */}
          <div>
            <h4 className="font-heading font-semibold text-lg text-signal-navy">
              {isUploading
                ? (isImageFile ? 'Đang phân tích ảnh CV bằng Gemini Vision AI...' : 'Đang phân tích CV với Gemini AI Pipeline...')
                : selectedFileName
                ? selectedFileName
                : 'Kéo thả tệp CV hoặc Nhấp để chọn'}
            </h4>
            <p className="text-sm text-signal-slate mt-1 max-w-md mx-auto">
              Hỗ trợ <strong>PDF, DOCX</strong> và <strong>Ảnh CV (JPG, PNG, WEBP, HEIC/iPhone)</strong> tối đa 15MB.
            </p>
          </div>

          {/* Upload Progress Indicator */}
          {isUploading && (
            <div className="w-full max-w-xs space-y-2">
              <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-signal-lime animate-pulse w-4/5 rounded-full" />
              </div>
              <p className="text-xs text-signal-slate font-medium">
                {isImageFile 
                  ? 'Trích xuất văn bản từ ảnh & phân tích kỹ năng, học vấn tự động...' 
                  : 'Bóc tách học vấn, kinh nghiệm và kỹ năng tự động...'}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Action Buttons for Mobile & Desktop (Crucial for iOS/Android picker choices) */}
      {!isUploading && (
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">
          {/* Button 1: Open Photo Library / Gallery */}
          <button
            type="button"
            onClick={() => photoLibraryInputRef.current?.click()}
            className="flex items-center justify-center gap-2 px-4 py-3 rounded-2xl bg-white border border-slate-200 hover:border-signal-navy text-signal-navy text-sm font-semibold shadow-sm hover:bg-slate-50 active:scale-[0.98] transition-all min-h-[48px]"
          >
            <ImageIcon className="w-4 h-4 text-emerald-600 shrink-0" />
            <span>Thư viện ảnh điện thoại</span>
          </button>

          {/* Button 2: Choose Documents (PDF, DOCX) */}
          <button
            type="button"
            onClick={() => documentInputRef.current?.click()}
            className="flex items-center justify-center gap-2 px-4 py-3 rounded-2xl bg-white border border-slate-200 hover:border-signal-navy text-signal-navy text-sm font-semibold shadow-sm hover:bg-slate-50 active:scale-[0.98] transition-all min-h-[48px]"
          >
            <FolderOpen className="w-4 h-4 text-indigo-600 shrink-0" />
            <span>Tệp PDF / DOCX</span>
          </button>

          {/* Button 3: Capture Photo with Camera */}
          <button
            type="button"
            onClick={() => cameraInputRef.current?.click()}
            className="flex items-center justify-center gap-2 px-4 py-3 rounded-2xl bg-signal-offwhite border border-slate-200 hover:border-signal-navy text-signal-navy text-sm font-semibold shadow-sm hover:bg-slate-100 active:scale-[0.98] transition-all min-h-[48px]"
          >
            <Camera className="w-4 h-4 text-amber-600 shrink-0" />
            <span>Chụp ảnh CV ngay</span>
          </button>
        </div>
      )}

      {/* Error alert with icon */}
      {errorMessage && (
        <div className="flex items-center gap-2 text-sm text-rose-600 bg-rose-50 p-3.5 rounded-2xl border border-rose-200 animate-fadeIn">
          <AlertCircle className="w-4 h-4 shrink-0 text-rose-500" />
          <span className="flex-1 font-medium">{errorMessage}</span>
          <button 
            type="button" 
            onClick={() => setErrorMessage(null)} 
            className="text-rose-400 hover:text-rose-600 p-1"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}
    </div>
  );
};

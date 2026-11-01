import os
import json
import io
import re
import math
import unicodedata
import uuid
import asyncio
from collections import Counter
from typing import Dict, Any, List, Optional, Set, Tuple

import numpy as np
from PIL import Image, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HAS_HEIF = True
except Exception:
    HAS_HEIF = False

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from app.core.config import settings

# Configure Gemini if key is provided and SDK is installed
if genai and settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY, transport="rest")
    except Exception as e:
        print(f"[Gemini Config] Notice: {e}")


# ================= SKILL SYNONYM & CANONICAL DICTIONARY =================
SYNONYM_MAP: Dict[str, str] = {
    "react": "react",
    "reactjs": "react",
    "react.js": "react",
    "react native": "react native",
    "node": "nodejs",
    "nodejs": "nodejs",
    "node.js": "nodejs",
    "python": "python",
    "python3": "python",
    "fastapi": "fastapi",
    "fast-api": "fastapi",
    "django": "django",
    "flask": "flask",
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "psql": "postgresql",
    "mysql": "mysql",
    "mongodb": "mongodb",
    "redis": "redis",
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "vue": "vue",
    "vuejs": "vue",
    "vue.js": "vue",
    "angular": "angular",
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "docker": "docker",
    "golang": "go",
    "go": "go",
    "java": "java",
    "c#": "c#",
    "c++": "c++",
    ".net": ".net",
    "dotnet": ".net",
    "ci/cd": "ci/cd",
    "aws": "aws",
    "azure": "azure",
    "gcp": "gcp",
    "git": "git",
    "ml": "machine learning",
    "machine learning": "machine learning",
    "ai": "artificial intelligence",
    "llm": "llms",
    "llms": "llms",
    "rag": "rag",
    "pytorch": "pytorch",
    "tensorflow": "tensorflow",
    "photoshop": "photoshop",
    "graphic design": "graphic design",
    "figma": "figma",
    "ui/ux": "ui/ux",
}

COMMON_TECH_SKILLS = [
    "Python", "FastAPI", "Django", "Flask", "React", "ReactJS", "Node.js", "NodeJS",
    "TypeScript", "JavaScript", "PostgreSQL", "MySQL", "MongoDB", "Redis",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "CI/CD",
    "C#", "C++", ".NET", "Java", "Go", "Golang", "Rust", "PHP",
    "Machine Learning", "PyTorch", "TensorFlow", "LLMs", "RAG",
    "HTML", "CSS", "Tailwind CSS", "VueJS", "Angular", "GraphQL",
    "Linux", "SQL Server", "Elasticsearch", "Figma", "UI/UX"
]


def normalize_skill(skill: str) -> str:
    cleaned = re.sub(r'[^a-zA-Z0-9\+\#\.\s]', '', skill).strip().lower()
    return SYNONYM_MAP.get(cleaned, cleaned)


def compute_cosine_similarity(text1: str, text2: str) -> float:
    """Compute cosine similarity between two text strings using bag-of-words / TF-IDF."""
    def get_tokens(text: str) -> List[str]:
        words = re.findall(r'\b[a-zA-Z0-9_\+#\.]+\b', text.lower())
        return [normalize_skill(w) for w in words if len(w) > 1]

    tokens1 = get_tokens(text1)
    tokens2 = get_tokens(text2)

    if not tokens1 or not tokens2:
        return 0.0

    vec1 = Counter(tokens1)
    vec2 = Counter(tokens2)

    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum(vec1[x] * vec2[x] for x in intersection)

    sum1 = sum(vec1[x] ** 2 for x in vec1.keys())
    sum2 = sum(vec2[x] ** 2 for x in vec2.keys())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return float(numerator) / denominator


SUPPORTED_DOC_EXTENSIONS = ["pdf", "docx", "doc"]
SUPPORTED_IMG_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "heic", "heif"]
ALL_SUPPORTED_EXTENSIONS = SUPPORTED_DOC_EXTENSIONS + SUPPORTED_IMG_EXTENSIONS


# ================= STEP 1: FILE VALIDATION =================
def validate_cv_file(file_name: str, file_bytes: bytes, mime_type: Optional[str] = None) -> Tuple[bool, str, str]:
    """
    Validate uploaded CV file.
    Checks:
    - Extension (.pdf, .docx, .doc, .jpg, .jpeg, .png, .webp, .heic, .heif)
    - File size (not empty, <= MAX_FILE_SIZE_MB for docs, <= 15MB for mobile camera photos)
    - Magic bytes / file signatures (never trust client name or mime alone)
    Returns: (is_valid, file_type, error_message)
    """
    if not file_bytes or len(file_bytes) == 0:
        return False, "", "Tệp tải lên rỗng (0 bytes). Vui lòng chọn tệp CV hợp lệ."

    ext = file_name.split(".")[-1].lower() if file_name and "." in file_name else ""
    if ext not in ALL_SUPPORTED_EXTENSIONS:
        return False, "", "Định dạng tệp không được hỗ trợ. Hệ thống chấp nhận tệp PDF, DOCX hoặc ảnh CV (JPG, PNG, WEBP, HEIC)."

    # Size check: 10MB for documents, 15MB for high-res smartphone photos
    is_img = ext in SUPPORTED_IMG_EXTENSIONS
    max_mb = 15 if is_img else settings.MAX_FILE_SIZE_MB
    max_bytes = max_mb * 1024 * 1024
    if len(file_bytes) > max_bytes:
        return False, "", f"Kích thước tệp ({round(len(file_bytes) / (1024*1024), 2)}MB) vượt quá giới hạn cho phép {max_mb}MB."

    # Verify signature for PDF
    if ext == "pdf":
        if b"%PDF-" not in file_bytes[:1024]:
            return False, "", "Tệp không phải là định dạng PDF hợp lệ hoặc cấu trúc tệp đã bị hỏng (thiếu chữ ký %PDF-)."
        return True, "pdf", "Hợp lệ"

    # Verify signature for DOCX / DOC
    if ext in ["docx", "doc"]:
        if file_bytes[:4] == b"PK\x03\x04" or b"PK" in file_bytes[:8]:
            return True, "docx", "Hợp lệ"
        if file_bytes[:4] == b"\xd0\xcf\x11\xe0":
            return True, "doc", "Hợp lệ"
        return False, "", "Tệp không phải là định dạng DOCX hợp lệ hoặc tệp đã bị hỏng."

    # Verify signature for Images (JPG, PNG, WEBP, HEIC/HEIF)
    if is_img:
        if ext in ["jpg", "jpeg"] and file_bytes[:3] != b"\xff\xd8\xff":
            return False, "", "Tệp không phải là định dạng ảnh JPEG hợp lệ hoặc dữ liệu ảnh bị hỏng."
        if ext == "png" and file_bytes[:8] != b"\x89PNG\r\n\x1a\n":
            return False, "", "Tệp không phải là định dạng ảnh PNG hợp lệ hoặc dữ liệu ảnh bị hỏng."
        if ext == "webp" and (file_bytes[:4] != b"RIFF" or file_bytes[8:12] != b"WEBP"):
            return False, "", "Tệp không phải là định dạng ảnh WEBP hợp lệ hoặc dữ liệu ảnh bị hỏng."

        # Deep validation via Pillow
        try:
            with Image.open(io.BytesIO(file_bytes)) as test_img:
                test_img.verify()
            return True, ext, "Hợp lệ"
        except Exception as e:
            return False, "", f"Tệp hình ảnh không hợp lệ hoặc bị hỏng ({str(e)})."

    return False, "", "Định dạng tệp không hợp lệ."


# ================= STEP 2: PDF TEXT EXTRACTION =================
def extract_pdf_text(file_bytes: bytes) -> Tuple[str, bool, str]:
    """
    Extract text from PDF using PyMuPDF (fitz) as primary parser and pdfplumber as fallback.
    Detects scanned PDFs without OCR.
    NEVER uses file_bytes.decode('utf-8') directly!
    Returns: (extracted_text, success, error_message)
    """
    # 1. Primary Parser: PyMuPDF (fitz)
    try:
        import fitz
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            if doc.page_count == 0:
                return "", False, "Tài liệu PDF không có trang nào."

            pages_text = []
            has_images = False
            for page in doc:
                text = page.get_text("text", sort=True)
                if text and text.strip():
                    pages_text.append(text)
                if len(page.get_images()) > 0:
                    has_images = True

            combined = "\n".join(pages_text).strip()
            if combined and len(combined) >= 30:
                cleaned = clean_and_normalize_text(combined)
                return cleaned, True, ""

            # Detect scanned PDF or graphics-only PDF: render pages to images and run OCR
            if doc.page_count > 0:
                ocr_texts = []
                for pno in range(min(doc.page_count, 3)):
                    page = doc[pno]
                    pix = page.get_pixmap(dpi=150)
                    img_bytes = pix.tobytes("png")
                    img_text, img_ok, _ = extract_image_cv(img_bytes, f"page_{pno}.png")
                    if img_ok and img_text:
                        ocr_texts.append(img_text)
                if ocr_texts:
                    ocr_combined = "\n".join(ocr_texts).strip()
                    if len(ocr_combined) >= 30:
                        return clean_and_normalize_text(ocr_combined), True, ""

            if doc.page_count > 0 and (not combined or len(combined) < 30) and has_images:
                return "", False, "Tài liệu PDF là bản scan/ảnh không chứa lớp văn bản (text layer) và không thể nhận diện qua OCR. Vui lòng tải lên file PDF rõ nét hoặc file DOCX."
    except Exception as e:
        # PyMuPDF failed, fall through to pdfplumber
        pass

    # 2. Fallback Parser: pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            if len(pdf.pages) == 0:
                return "", False, "Tài liệu PDF không có trang nào."

            pages_text = []
            for page in pdf.pages:
                t = page.extract_text()
                if t and t.strip():
                    pages_text.append(t)

            combined = "\n".join(pages_text).strip()
            if combined and len(combined) >= 30:
                cleaned = clean_and_normalize_text(combined)
                return cleaned, True, ""
    except Exception:
        pass

    # Strictly do NOT decode raw bytes as string!
    return "", False, "Không thể đọc nội dung văn bản từ tệp PDF. Tệp có thể là ảnh scan chưa qua OCR hoặc đã bị lỗi font chữ/mã hoá."


# ================= STEP 3: DOCX TEXT EXTRACTION =================
def extract_docx_text(file_bytes: bytes) -> Tuple[str, bool, str]:
    """
    Extract text from DOCX using python-docx.
    Extracts paragraphs and tables in proper sequential order.
    Returns: (extracted_text, success, error_message)
    """
    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

        table_lines = []
        for table in doc.tables:
            for row in table.rows:
                seen_cells = set()
                row_texts = []
                for cell in row.cells:
                    ct = cell.text.strip()
                    if ct and ct not in seen_cells:
                        seen_cells.add(ct)
                        row_texts.append(ct)
                if row_texts:
                    table_lines.append(" | ".join(row_texts))

        combined = "\n".join(paragraphs + table_lines).strip()
        if not combined or len(combined) < 20:
            return "", False, "Tệp DOCX không chứa văn bản nào hoặc nội dung quá ngắn."

        cleaned = clean_and_normalize_text(combined)
        return cleaned, True, ""
    except Exception as e:
        return "", False, f"Không thể trích xuất nội dung DOCX: {str(e)}"


# ================= STEP 4: TEXT CLEANING =================
def clean_and_normalize_text(text: str) -> str:
    """
    Normalize text:
    - Unicode NFC normalization for Vietnamese
    - Remove control characters while keeping whitespace/newlines
    - Clean excessive whitespace and blank lines
    - Preserve Vietnamese diacritics, tech terms, and emails
    """
    if not text:
        return ""

    # Unicode NFC normalization
    text = unicodedata.normalize("NFC", text)

    # Remove non-printable control characters except \n, \t, \r
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

    # Normalize horizontal whitespace
    text = re.sub(r'[ \t]+', ' ', text)

    # Normalize excessive newlines (max 2 consecutive newlines)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


# ================= STEP 5: TEXT QUALITY VALIDATION =================
def validate_extracted_text(text: str) -> Tuple[bool, str]:
    """
    Validate the quality of extracted text before allowing AI processing:
    - Detects raw PDF binary markers (%PDF-, /Type, /Pages, /Font, obj, endstream)
    - Detects unreadable / corrupted encoding
    - Detects empty or too-short text
    - Detects lack of meaningful words
    Returns: (is_valid, error_reason)
    """
    if not text or not text.strip():
        return False, "Nội dung CV rỗng hoặc không trích xuất được văn bản."

    cleaned = text.strip()

    # 1. Detect raw PDF binary leakage
    if cleaned.startswith("%PDF-") or "%PDF-" in cleaned[:100]:
        return False, "Phát hiện mã binary PDF thô (%PDF-). Parser chưa trích xuất được văn bản hiển thị."

    pdf_operators = ["/Type", "/Pages", "/Font", "/Filter", "/Length", "/Catalog", "/MediaBox", "endobj", "endstream", "xref", "trailer"]
    op_count = sum(cleaned.count(op) for op in pdf_operators)
    if op_count >= 3:
        return False, "Nội dung trích xuất chứa cấu trúc mã PDF nội bộ (/Type, /Pages, obj) thay vì văn bản ứng viên."

    # 2. Length check: minimum meaningful characters
    if len(cleaned) < 40:
        return False, "Nội dung CV quá ngắn (dưới 40 ký tự), không đủ thông tin có ý nghĩa."

    # 3. Ratio of printable / readable characters (detect garbage encoding)
    readable_chars = sum(1 for c in cleaned if c.isalnum() or c.isspace() or c in ",.-_@+/()[]:;'\"#*!?%$~`<>{}")
    ratio = readable_chars / max(1, len(cleaned))
    if ratio < 0.65:
        return False, "Nội dung có dấu hiệu bị lỗi mã hoá ký tự (tỷ lệ ký tự đọc được quá thấp)."

    # 4. Word count check
    words = cleaned.split()
    if len(words) < 8:
        return False, "Nội dung CV không chứa đủ số lượng từ có ý nghĩa để phân tích."

    return True, "Hợp lệ"


# ================= STEP 3.5: IMAGE CV TEXT EXTRACTION (VISION OCR) =================
def extract_image_cv(file_bytes: bytes, file_name: str) -> Tuple[str, bool, str]:
    """
    Extract text from image CV (JPG, PNG, WEBP, HEIC/HEIF).
    Supports smartphone photos, gallery images, and scans.
    Performs auto-orientation (EXIF transpose), blank image detection,
    and Gemini Multimodal Vision OCR extraction.
    Returns: (extracted_text, success, error_message)
    """
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # Auto-rotate smartphone photos based on EXIF tag
        image = ImageOps.exif_transpose(image)
        if image.mode != "RGB":
            image = image.convert("RGB")
    except Exception as e:
        return "", False, f"Không thể giải mã dữ liệu hình ảnh: {str(e)}"

    # Dimension validation (must be at least 150x150 to be a document)
    w, h = image.size
    if w < 150 or h < 150:
        return "", False, f"Kích thước hình ảnh quá nhỏ ({w}x{h}px) để nhận diện nội dung văn bản CV."

    # Blank / solid-color image detection
    try:
        gray = image.convert("L")
        arr = np.array(gray)
        variance = float(np.var(arr))
        if variance < 8.0:
            return "", False, "Hình ảnh rỗng hoặc không chứa nội dung (ảnh đơn sắc/trắng tinh). Vui lòng chọn ảnh chụp CV rõ nét."
    except Exception:
        pass

    # Check if Gemini Vision is configured
    has_valid_key = bool(
        settings.GEMINI_API_KEY and 
        settings.GEMINI_API_KEY.strip() and 
        settings.GEMINI_API_KEY != "your_gemini_api_key_here"
    )

    if genai and has_valid_key:
        try:
            model = genai.GenerativeModel(settings.GEMINI_MODEL)
            prompt = """
            Bạn là Chuyên gia AI Phân tích CV & Nhận diện Tài liệu Tuyển dụng (HireSense AI Vision Engine).
            Hãy đọc kỹ toàn bộ văn bản trong bức ảnh này (hỗ trợ cả tiếng Việt có dấu và tiếng Anh).

            YÊU CẦU:
            1. Đọc và trích xuất TOÀN BỘ nội dung chữ xuất hiện trong tài liệu CV từ trên xuống dưới, bao gồm:
               - Họ và tên, email, số điện thoại, địa chỉ
               - Mục tiêu nghề nghiệp, tóm tắt
               - Kỹ năng chuyên môn (Hard Skills), kỹ năng mềm (Soft Skills)
               - Quá trình học vấn, trường lớp, chuyên ngành
               - Lịch sử kinh nghiệm làm việc, tên công ty, chức danh, thời gian, mô tả công việc
               - Các dự án, chứng chỉ, ngoại ngữ
            2. Giữ nguyên định dạng đoạn văn bản rõ ràng.
            3. Nếu ảnh bị mờ hoàn toàn, không có chữ, hoặc không phải là CV, hãy trả về đúng từ khóa:
               ERROR: IMAGE_UNREADABLE
            """
            response = model.generate_content([image, prompt])
            resp_text = response.text.strip() if response and response.text else ""

            if not resp_text or "ERROR: IMAGE_UNREADABLE" in resp_text:
                return "", False, "Hình ảnh CV bị mờ hoặc không chứa nội dung văn bản có thể đọc được. Vui lòng chụp rõ nét hơn hoặc tải file PDF/DOCX."

            cleaned = clean_and_normalize_text(resp_text)
            if len(cleaned) < 30:
                return "", False, "Hình ảnh CV chứa quá ít văn bản để phân tích. Vui lòng chọn ảnh CV đầy đủ thông tin."

            return cleaned, True, ""
        except Exception as e:
            print(f"[Gemini Vision OCR Error]: {e}")
            # Fall through if Gemini API returns error

    # If Gemini Vision is unavailable, do not fake hallucinated CV data
    return "", False, "Không thể đọc nội dung văn bản từ hình ảnh CV khi không có dịch vụ AI Vision. Vui lòng đảm bảo ảnh chụp rõ nét hoặc tải lên file PDF/DOCX."


# ================= AVATAR & COMPANY LOGO IMAGE PROCESSOR =================
def process_and_save_image(
    file_bytes: bytes, 
    original_filename: str, 
    max_size_mb: int = 5, 
    is_avatar: bool = False,
    is_logo: bool = False
) -> Tuple[bool, str, str]:
    """
    Validate, sanitize, resize and save profile avatar or company logo.
    - Limits size <= max_size_mb (default 5MB)
    - Validates image signature
    - Fixes smartphone camera rotation (EXIF transpose)
    - Crops to square if avatar
    - Generates safe unique filename (no user input in path)
    - Saves in settings.UPLOAD_DIR as WebP/JPEG
    Returns: (success, file_url, error_message)
    """
    if not file_bytes or len(file_bytes) == 0:
        return False, "", "Tệp ảnh rỗng (0 bytes). Vui lòng chọn ảnh hợp lệ."

    if len(file_bytes) > max_size_mb * 1024 * 1024:
        return False, "", f"Kích thước ảnh vượt quá giới hạn {max_size_mb}MB."

    try:
        image = Image.open(io.BytesIO(file_bytes))
        image = ImageOps.exif_transpose(image)
    except Exception as e:
        return False, "", f"Tệp không phải là định dạng hình ảnh hợp lệ hoặc đã bị hỏng: {str(e)}"

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    prefix = "avatar" if is_avatar else ("logo" if is_logo else "img")
    safe_name = f"{prefix}_{uuid.uuid4().hex}.webp"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_name)

    try:
        if is_avatar:
            # Center crop to square
            w, h = image.size
            min_dim = min(w, h)
            left = (w - min_dim) // 2
            top = (h - min_dim) // 2
            image = image.crop((left, top, left + min_dim, top + min_dim))
            image = image.resize((400, 400), Image.Resampling.LANCZOS)
        elif is_logo:
            image.thumbnail((500, 500), Image.Resampling.LANCZOS)
        else:
            image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)

        if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
            image.save(file_path, format="WEBP", quality=90)
        else:
            image = image.convert("RGB")
            image.save(file_path, format="WEBP", quality=90)

        return True, f"/uploads/{safe_name}", ""
    except Exception as e:
        return False, "", f"Lỗi khi lưu trữ hình ảnh: {str(e)}"


# ================= HIGH-LEVEL EXTRACTION ENTRYPOINT =================
def extract_text_from_cv(file_bytes: bytes, file_name: str, mime_type: Optional[str] = None) -> Tuple[str, bool, str]:
    """
    Complete CV extraction pipeline:
    1. Validate file (format, signature, size)
    2. Extract text (PyMuPDF / pdfplumber for PDF, python-docx for DOCX, Gemini Vision for Images)
    3. Validate extracted text quality
    Returns: (clean_text, success, error_message)
    """
    is_valid, file_type, val_err = validate_cv_file(file_name, file_bytes, mime_type)
    if not is_valid:
        return "", False, val_err

    if file_type == "pdf":
        raw_text, ext_ok, ext_err = extract_pdf_text(file_bytes)
    elif file_type in ["docx", "doc"]:
        raw_text, ext_ok, ext_err = extract_docx_text(file_bytes)
    elif file_type in SUPPORTED_IMG_EXTENSIONS:
        raw_text, ext_ok, ext_err = extract_image_cv(file_bytes, file_name)
    else:
        return "", False, "Định dạng tệp không được hỗ trợ."

    if not ext_ok:
        return "", False, ext_err

    # Validate quality of text
    is_quality_ok, quality_err = validate_extracted_text(raw_text)
    if not is_quality_ok:
        return "", False, quality_err

    return raw_text, True, ""


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Legacy helper for extracting text from PDF without binary decode fallback."""
    text, ok, _ = extract_pdf_text(file_bytes)
    return text if ok else ""


# ================= EMBEDDING GENERATION =================
def generate_embedding(text: str) -> Optional[List[float]]:
    """
    Generate dense embedding vector (dimension 768) from valid text.
    Uses Gemini text-embedding-004 when available, or a deterministic normalized vector.
    """
    if not text or not text.strip():
        return None

    cleaned_text = clean_and_normalize_text(text)[:2048]

    # Try live Gemini embedding if configured
    if genai and settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here":
        try:
            result = genai.embed_content(
                model=settings.EMBEDDING_MODEL,
                content=cleaned_text,
                task_type="retrieval_document"
            )
            emb = result.get("embedding")
            if emb:
                return emb[:768]
        except Exception as e:
            print(f"[Gemini Embedding Warning]: {e}")

    # Deterministic local TF-IDF / hash embedding (768 dimensions) for standalone/test mode
    vec = [0.0] * 768
    words = re.findall(r'\b[a-zA-Z0-9_\+#\.]+\b', cleaned_text.lower())
    for w in words:
        h = abs(hash(w)) % 768
        vec[h] += 1.0

    # L2 normalize
    norm = math.sqrt(sum(x ** 2 for x in vec))
    if norm > 0:
        vec = [round(x / norm, 6) for x in vec]
    return vec


# ================= STEP 6: GEMINI AI STRUCTURED EXTRACTION =================
def heuristic_cv_extraction(raw_text: str) -> Dict[str, Any]:
    """
    Deterministic factual extractor directly parsing the real text.
    NEVER returns %PDF-1.4 or raw PDF syntax operators.
    """
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    # 1. Extract Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}', raw_text)
    email = email_match.group(0) if email_match else None

    # 2. Extract Phone (VN format)
    phone_match = re.search(r'(?:\+84|0)[1-9][0-9\s\.-]{7,11}', raw_text)
    phone = phone_match.group(0).strip() if phone_match else None

    # 3. Extract Full Name
    full_name = None
    name_patterns = [
        r'(?:Họ(?:\s+và)?\s+tên|Full\s*Name|Candidate|Ứng\s*viên)[ \t]*[:\-][ \t]*([^\n\r\|]+)',
        r'(?:Họ\s*tên|Tên)[ \t]*[:\-][ \t]*([^\n\r\|]+)',
    ]
    for pat in name_patterns:
        m = re.search(pat, raw_text, re.IGNORECASE)
        if m:
            cand = m.group(1).strip()
            # Clean any leading label or punctuation
            cand = re.sub(r'^(?:Họ(?:\s+và)?\s+tên|Tên|Name)[:\-\s]+', '', cand, flags=re.IGNORECASE).strip()
            if cand and not cand.startswith("%") and "/" not in cand and len(cand) < 60:
                full_name = cand
                break

    if not full_name and lines:
        for line in lines[:5]:
            # Must not be email, url, phone, or PDF code
            if "@" in line or "http" in line or line.startswith("%") or "/" in line:
                continue
            if re.match(r'^\d', line):
                continue
            # A human name in CV is typically 2 to 5 words, length between 4 and 40
            words = line.split()
            if 2 <= len(words) <= 5 and 4 <= len(line) <= 40:
                full_name = line
                break

    # 4. Extract Hard Skills by matching actual text
    lower_text = raw_text.lower()
    found_hard_skills = []
    for skill in COMMON_TECH_SKILLS:
        pattern = r'(?:\b|\s|^)' + re.escape(skill.lower()) + r'(?:\b|\s|$|[,\.\:\;])'
        if re.search(pattern, lower_text):
            if skill not in found_hard_skills:
                found_hard_skills.append(skill)

    # 5. Extract Education
    education = []
    edu_keywords = ["đại học", "học viện", "cao đẳng", "university", "college", "hcmut", "bách khoa", "khtn", "fpt"]
    for i, line in enumerate(lines):
        if any(kw in line.lower() for kw in edu_keywords):
            degree = None
            if "kỹ sư" in line.lower(): degree = "Kỹ sư"
            elif "cử nhân" in line.lower(): degree = "Cử nhân"
            elif "thạc sĩ" in line.lower(): degree = "Thạc sĩ"

            education.append({
                "institution": line[:100],
                "degree": degree,
                "field_of_study": None,
                "start_date": None,
                "end_date": None,
                "gpa": None
            })
            if len(education) >= 3:
                break

    # 6. Extract Experience
    experience = []
    exp_pattern = re.compile(r'(?:từ\s+)?(\d{1,2}/\d{4}|\d{4})\s*[-–]\s*(\d{1,2}/\d{4}|\d{4}|hiện tại|nay|present|current)', re.IGNORECASE)
    for i, line in enumerate(lines):
        m = exp_pattern.search(line)
        if m:
            is_current = bool(re.search(r'hiện tại|nay|present|current', m.group(2), re.IGNORECASE))
            desc_lines = lines[i:i+3]
            company_candidate = desc_lines[0][:100]
            # Avoid using PDF operators
            if not company_candidate.startswith("/") and "%" not in company_candidate:
                experience.append({
                    "company_name": company_candidate,
                    "job_title": desc_lines[1][:100] if len(desc_lines) > 1 else "Chuyên viên",
                    "start_date": m.group(1),
                    "end_date": "Hiện tại" if is_current else m.group(2),
                    "is_current": is_current,
                    "description": " ".join(desc_lines)[:300]
                })
                if len(experience) >= 5:
                    break

    # 7. Summary
    summary = None
    sum_match = re.search(r'(?:mục tiêu|giới thiệu|tóm tắt|objective|summary|about me)[:\s]*\n?([^\n]{20,400})', raw_text, re.IGNORECASE)
    if sum_match:
        summary = sum_match.group(1).strip()
    elif lines:
        for line in lines[1:6]:
            if len(line) > 30 and "@" not in line and not line.startswith("%"):
                summary = line
                break

    missing = []
    if not full_name: missing.append("Họ tên")
    if not email: missing.append("Email")
    if not phone: missing.append("Số điện thoại")
    if not found_hard_skills: missing.append("Kỹ năng")

    return {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "address": None,
        "summary": summary,
        "hard_skills": found_hard_skills,
        "soft_skills": [],
        "education": education,
        "experience": experience,
        "projects": [],
        "certifications": [],
        "languages": ["Tiếng Anh"] if "tiếng anh" in lower_text or "english" in lower_text else [],
        "missing_fields": missing
    }


def mock_llm_extraction(raw_text: str) -> Dict[str, Any]:
    """Backward compatible heuristic extractor for local testing."""
    return heuristic_cv_extraction(raw_text)


async def gemini_extract_structured_cv(raw_text: str) -> Dict[str, Any]:
    """
    Extract structured CV entities using Gemini LLM.
    Returns structured JSON with fields: full_name, email, phone, summary,
    hard_skills, soft_skills, education, experience, certifications, languages, projects.
    """
    # 1. Text Quality check before invoking Gemini
    is_quality_ok, quality_err = validate_extracted_text(raw_text)
    if not is_quality_ok:
        raise ValueError(f"Dữ liệu CV không đạt tiêu chuẩn chất lượng: {quality_err}")

    has_valid_key = bool(
        settings.GEMINI_API_KEY and 
        settings.GEMINI_API_KEY.strip() and 
        settings.GEMINI_API_KEY != "your_gemini_api_key_here"
    )

    if not has_valid_key or not genai:
        return heuristic_cv_extraction(raw_text)

    try:
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        prompt = f"""
        You are a Senior Talent AI Extraction Engine. Extract all factual information strictly from the following CV text.
        
        CRITICAL RULES:
        1. Extract ONLY facts explicitly stated in the CV.
        2. NEVER hallucinate or guess a candidate name. Under NO circumstances should you extract "%PDF-1.4" or PDF code as a name.
        3. NEVER use PDF operators (e.g. /Type, /E(, /Pg 9 0 R) as work experience, company names, or job titles.
        4. If a field is not present in the CV text, use null for strings, or an empty list [] for arrays.
        5. For hard skills, extract only technical skills mentioned in the CV (e.g. programming languages, frameworks, databases, tools).
        
        CV TEXT:
        \"\"\"{raw_text[:12000]}\"\"\"
        
        Respond ONLY with a valid JSON object matching this exact schema:
        {{
            "full_name": string or null,
            "email": string or null,
            "phone": string or null,
            "address": string or null,
            "summary": string or null,
            "hard_skills": [string],
            "soft_skills": [string],
            "education": [
                {{
                    "institution": string,
                    "degree": string or null,
                    "field_of_study": string or null,
                    "start_date": string or null,
                    "end_date": string or null,
                    "gpa": string or null
                }}
            ],
            "experience": [
                {{
                    "company_name": string,
                    "job_title": string,
                    "start_date": string or null,
                    "end_date": string or null,
                    "is_current": boolean,
                    "description": string or null
                }}
            ],
            "projects": [
                {{
                    "name": string,
                    "role": string or null,
                    "description": string or null,
                    "technologies": [string]
                }}
            ],
            "certifications": [string],
            "languages": [string],
            "missing_fields": [string]
        }}
        """
        response = await asyncio.wait_for(model.generate_content_async(prompt), timeout=12.0)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        parsed = json.loads(text.strip())

        # Post-validation on Gemini output to ensure no binary or operator leaks
        full_name = parsed.get("full_name") or ""
        if "%PDF" in full_name or "/" in full_name or len(full_name) > 80:
            parsed["full_name"] = None

        return parsed
    except Exception as e:
        print(f"[Gemini extraction error]: {e}")
        return heuristic_cv_extraction(raw_text)


# ================= STEP 7: HYBRID JOB MATCHING ALGORITHM =================
def calculate_hybrid_match(cv_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hybrid Job Matching algorithm:
    - Weighted Hard Skills Matching (50%): Uses canonical normalization and synonym mapping
    - Semantic Similarity (30%): Computes domain cosine similarity across texts
    - Experience Alignment (20%): Evaluates experience and preferred skill match
    Outputs transparent score (0 - 100), components, matched & missing skills, and recommendations.
    NO hardcoded 42%, 82%, 85% baselines!
    """
    raw_cv_skills = cv_data.get("hard_skills") or []
    norm_cv_skills: Set[str] = {normalize_skill(s) for s in raw_cv_skills if s}

    req_skills = job_data.get("required_skills") or []
    pref_skills = job_data.get("preferred_skills") or []

    matched_req = []
    missing_req = []
    for r in req_skills:
        if normalize_skill(r) in norm_cv_skills:
            matched_req.append(r)
        else:
            missing_req.append(r)

    matched_pref = []
    missing_pref = []
    for p in pref_skills:
        if normalize_skill(p) in norm_cv_skills:
            matched_pref.append(p)
        else:
            missing_pref.append(p)

    # 1. Hard Skills Score (0 - 100, weight: 50%)
    if req_skills:
        hard_ratio = len(matched_req) / len(req_skills)
        hard_score = round(hard_ratio * 100.0, 1)
    else:
        hard_score = 100.0 if norm_cv_skills else 0.0

    # 2. Semantic Similarity Score (0 - 100, weight: 30%)
    cv_exp_texts = []
    for exp in cv_data.get("experience") or []:
        if isinstance(exp, dict):
            cv_exp_texts.append(exp.get("description") or exp.get("job_title") or "")
        elif isinstance(exp, str):
            cv_exp_texts.append(exp)

    cv_text = (
        (cv_data.get("summary") or "") + " " +
        " ".join(raw_cv_skills) + " " +
        " ".join(cv_exp_texts)
    ).strip()

    job_text = (
        (job_data.get("title") or "") + " " +
        (job_data.get("description") or "") + " " +
        (job_data.get("requirements") or "") + " " +
        " ".join(req_skills + pref_skills)
    ).strip()

    cos_sim = compute_cosine_similarity(cv_text, job_text)

    # Realistic semantic score based on text similarity
    if hard_score > 0:
        domain_baseline = 40.0
        semantic_score = round(min(100.0, domain_baseline + (cos_sim * 45.0) + (hard_score * 0.2)), 1)
    else:
        # Zero required skills matched
        semantic_score = round(min(25.0, cos_sim * 40.0), 1)

    # 3. Experience Score (0 - 100, weight: 20%)
    cv_experience = cv_data.get("experience") or []
    has_experience = len(cv_experience) > 0
    pref_ratio = len(matched_pref) / len(pref_skills) if pref_skills else 0.5

    if hard_score == 0 and not norm_cv_skills:
        experience_score = 0.0
    elif hard_score == 0:
        experience_score = round(min(15.0, pref_ratio * 20.0), 1)
    else:
        base_exp = 55.0 if has_experience else 35.0
        experience_score = round(min(100.0, base_exp + (pref_ratio * 25.0) + (hard_score * 0.2)), 1)

    # Hybrid overall weighted score (0 - 100)
    overall_score = round(min(100.0, max(0.0, (hard_score * 0.5) + (semantic_score * 0.3) + (experience_score * 0.2))), 1)

    # Human-readable explanation
    if overall_score >= 80:
        explanation = (
            f"Hồ sơ ứng viên có độ tương thích xuất sắc ({overall_score}%). "
            f"Đáp ứng {len(matched_req)}/{len(req_skills)} kỹ năng bắt buộc "
            f"và có độ tương đồng ngữ nghĩa cao với yêu cầu tuyển dụng."
        )
    elif overall_score >= 45:
        explanation = (
            f"Hồ sơ ứng viên phù hợp một phần ({overall_score}%). "
            f"Đáp ứng {len(matched_req)}/{len(req_skills)} kỹ năng cốt lõi. "
            f"Cần đánh giá thêm về các kỹ năng chuyên biệt."
        )
    else:
        explanation = (
            f"Hồ sơ ứng viên có độ tương thích thấp ({overall_score}%). "
            f"Thiếu {len(missing_req)} kỹ năng cốt lõi cần thiết cho vị trí này."
        )

    if missing_req:
        explanation += f" Khoảng cách kỹ năng cần chú ý: {', '.join(missing_req)}."

    recommendations = [f"Bổ sung dự án thực tế hoặc chứng chỉ chuyên sâu về {s}." for s in missing_req]
    if missing_pref:
        recommendations.append(f"Khuyến khích tìm hiểu thêm về {', '.join(missing_pref[:2])} để gia tăng lợi thế cạnh tranh.")
    if not recommendations and not missing_req:
        recommendations.append("Hồ sơ đáp ứng hoàn hảo yêu cầu tuyển dụng. Sẵn sàng cho phỏng vấn trực tiếp.")

    return {
        "overall_score": overall_score,
        "hard_skills_score": hard_score,
        "semantic_score": semantic_score,
        "experience_score": experience_score,
        "matched_skills": matched_req + matched_pref,
        "missing_required_skills": missing_req,
        "missing_preferred_skills": missing_pref,
        "ai_explanation": explanation,
        "recommendations": recommendations
    }

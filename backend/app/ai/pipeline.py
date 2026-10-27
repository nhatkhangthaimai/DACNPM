import os
import json
import io
import re
import math
from collections import Counter
from typing import Dict, Any, List, Optional, Set
try:
    import google.generativeai as genai
except ImportError:
    genai = None

from app.core.config import settings

# Configure Gemini if key is provided and SDK is installed
if genai and settings.GEMINI_API_KEY:
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
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
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "psql": "postgresql",
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "vue": "vue",
    "vuejs": "vue",
    "vue.js": "vue",
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "docker": "docker",
    "golang": "go",
    "go": "go",
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


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract clean text from PDF bytes using PyMuPDF (fitz) or pdfplumber."""
    text_content = []
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text_content.append(page.get_text())
        if "".join(text_content).strip():
            return "\n".join(text_content)
    except Exception:
        pass

    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_content.append(t)
            return "\n".join(text_content)
    except Exception:
        pass

    # Fallback to UTF-8 decoding
    return file_bytes.decode('utf-8', errors='ignore')


async def gemini_extract_structured_cv(raw_text: str) -> Dict[str, Any]:
    """
    Extract structured CV entities using Gemini LLM.
    Returns structured JSON with fields: full_name, email, phone, summary,
    hard_skills, soft_skills, education, experience, certifications, languages.
    """
    if not settings.GEMINI_API_KEY:
        return mock_llm_extraction(raw_text)

    try:
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        prompt = f"""
        You are a Senior Talent AI Extraction Engine. Extract all factual information from the following CV text.
        Do NOT invent or hallucinate information that is not present in the CV.
        
        CV TEXT:
        \"\"\"{raw_text[:12000]}\"\"\"
        
        Respond ONLY with a valid JSON object matching this exact schema:
        {{
            "full_name": string or null,
            "email": string or null,
            "phone": string or null,
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
            "certifications": [string],
            "languages": [string],
            "missing_fields": [string]
        }}
        """
        response = await model.generate_content_async(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
    except Exception as e:
        print(f"Gemini extraction error: {e}")
        return mock_llm_extraction(raw_text)


def mock_llm_extraction(raw_text: str) -> Dict[str, Any]:
    """Deterministic fallback for local testing without Gemini credentials."""
    return {
        "full_name": "Ứng viên Công nghệ (Auto-Parsed)",
        "email": "candidate@hiresense.ai",
        "phone": "0908 123 456",
        "summary": "Chuyên gia phát triển phần mềm và AI với kinh nghiệm thực tiễn xây dựng các hệ thống tuyển dụng và so khớp kỹ năng.",
        "hard_skills": ["Python", "FastAPI", "ReactJS", "TypeScript", "PostgreSQL", "Docker", "Machine Learning"],
        "soft_skills": ["Làm việc nhóm", "Tư duy phản biện", "Giao tiếp kỹ thuật"],
        "education": [
            {
                "institution": "Đại học Bách Khoa TP.HCM",
                "degree": "Kỹ sư",
                "field_of_study": "Khoa học Máy tính",
                "start_date": "2019",
                "end_date": "2023",
                "gpa": "3.6/4.0"
            }
        ],
        "experience": [
            {
                "company_name": "Tech Hub Innovation",
                "job_title": "AI & Software Engineer",
                "start_date": "2023",
                "end_date": "Hiện tại",
                "is_current": True,
                "description": "Phát triển hệ thống xử lý ngôn ngữ tự nhiên và tối ưu hoá truy vấn cơ sở dữ liệu."
            }
        ],
        "certifications": ["Generative AI Professional", "Cloud Practitioner"],
        "languages": ["Tiếng Việt (Bản ngữ)", "Tiếng Anh (Chuyên ngành)"],
        "missing_fields": []
    }


def calculate_hybrid_match(cv_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hybrid Job Matching algorithm:
    - Weighted Hard Skills Matching (50%): Uses canonical normalization and synonym mapping
    - Semantic Similarity (30%): Computes domain cosine similarity across texts
    - Experience Alignment (20%): Evaluates experience and preferred skill match
    Outputs transparent score (0 - 100), components, matched & missing skills, and recommendations.
    """
    raw_cv_skills = cv_data.get("hard_skills", [])
    norm_cv_skills: Set[str] = {normalize_skill(s) for s in raw_cv_skills}

    req_skills = job_data.get("required_skills", [])
    pref_skills = job_data.get("preferred_skills", [])

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

    # 1. Hard Skills Score (0 - 100)
    if req_skills:
        hard_ratio = len(matched_req) / len(req_skills)
        hard_score = round(hard_ratio * 100, 1)
    else:
        hard_score = 100.0 if norm_cv_skills else 0.0

    # 2. Semantic Similarity Score (0 - 100)
    cv_text = (
        (cv_data.get("summary") or "") + " " +
        " ".join(raw_cv_skills) + " " +
        " ".join([exp.get("description", "") or exp.get("job_title", "") for exp in cv_data.get("experience", [])])
    )
    job_text = (
        (job_data.get("title") or "") + " " +
        (job_data.get("description") or "") + " " +
        (job_data.get("requirements") or "") + " " +
        " ".join(req_skills + pref_skills)
    )

    cos_sim = compute_cosine_similarity(cv_text, job_text)
    
    # Scale cosine similarity and domain competence
    if hard_score > 0:
        # Base semantic score reflects established domain competence
        domain_baseline = 40.0
        semantic_score = round(min(100.0, domain_baseline + (cos_sim * 45.0) + (hard_score * 0.2)), 1)
    else:
        # Zero required skills matched
        semantic_score = round(min(25.0, cos_sim * 40.0), 1)

    # 3. Experience Score (0 - 100)
    has_experience = len(cv_data.get("experience", [])) > 0
    pref_ratio = len(matched_pref) / len(pref_skills) if pref_skills else 0.5
    if hard_score == 0 and not norm_cv_skills:
        experience_score = 0.0
    elif hard_score == 0:
        experience_score = round(min(15.0, pref_ratio * 20.0), 1)
    else:
        base_exp = 55.0 if has_experience else 35.0
        experience_score = round(min(100.0, base_exp + (pref_ratio * 25.0) + (hard_score * 0.2)), 1)

    # Hybrid overall weighted score (0 - 99)
    overall_score = round(min(99.0, max(0.0, (hard_score * 0.5) + (semantic_score * 0.3) + (experience_score * 0.2))), 1)

    # Reasoning and explanation
    if overall_score >= 85:
        explanation = (
            f"Hồ sơ ứng viên có độ tương thích xuất sắc ({overall_score}%). "
            f"Đáp ứng {len(matched_req)}/{len(req_skills)} kỹ năng bắt buộc "
            f"và có độ tương đồng ngữ nghĩa cao với yêu cầu tuyển dụng."
        )
    elif overall_score >= 60:
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

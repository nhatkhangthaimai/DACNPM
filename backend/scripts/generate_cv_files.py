"""
Script to generate 30 physical CV files (18 PDF, 12 DOCX) with real readable text
and create 30 Ground Truth JSON files.
"""

import os
import json
import fitz  # PyMuPDF
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from data_definitions import CANDIDATES_DATA

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))
GROUND_TRUTH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tests", "ground_truth"))
REPORT_GT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "reports", "multi-industry-testing", "ground_truth"))

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GROUND_TRUTH_DIR, exist_ok=True)
os.makedirs(REPORT_GT_DIR, exist_ok=True)


def build_cv_text_blocks(cand: dict) -> str:
    """Build natural human-readable text representation for CV content."""
    lines = [
        f"HỌ VÀ TÊN: {cand['full_name']}",
        f"Email: {cand['email']}",
        f"Số điện thoại: {cand['phone']}",
        f"Vị trí mong muốn: {cand['title']}",
        "",
        "--- TÓM TẮT BẢN THÂN ---",
        cand["summary"],
        "",
        "--- HỌC VẤN ---"
    ]

    for edu in cand.get("education", []):
        lines.append(f"• Cơ sở đào tạo: {edu['institution']}")
        lines.append(f"  Văn bằng: {edu.get('degree', 'Cử nhân')} - Chuyên ngành: {edu.get('field_of_study', '')}")
        lines.append(f"  Thời gian: {edu.get('start_date', '')} - {edu.get('end_date', '')} | Điểm GPA: {edu.get('gpa', 'N/A')}")

    lines.append("")
    lines.append("--- KINH NGHIỆM LÀM VIỆC ---")
    for exp in cand.get("experience", []):
        lines.append(f"• Doanh nghiệp: {exp['company_name']}")
        lines.append(f"  Chức danh: {exp['job_title']} ({exp.get('start_date', '')} - {exp.get('end_date', '')})")
        lines.append(f"  Mô tả: {exp['description']}")

    lines.append("")
    lines.append("--- KỸ NĂNG CHUYÊN MÔN (HARD SKILLS) ---")
    lines.append(", ".join(cand.get("hard_skills", [])))

    if cand.get("negative_skills"):
        lines.append("")
        lines.append("--- LƯU Ý VỀ KỸ NĂNG CHƯA CÓ / CHƯA THÀNH THẠO ---")
        for neg in cand["negative_skills"]:
            lines.append(f"• Chưa có kinh nghiệm sử dụng {neg}. Chưa từng làm việc thực tế với {neg}.")

    lines.append("")
    lines.append("--- KỸ NĂNG MỀM (SOFT SKILLS) ---")
    lines.append(", ".join(cand.get("soft_skills", [])))

    if cand.get("certifications"):
        lines.append("")
        lines.append("--- CHỨNG CHỈ NGHỀ NGHIỆP ---")
        for cert in cand["certifications"]:
            lines.append(f"• {cert}")

    return "\n".join(lines)


def generate_pdf_cv(cand: dict, output_path: str):
    """Generate a valid, fully readable PDF with text layer using PyMuPDF."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4 size in points

    # Header title
    font_name = "helv"
    
    # We can write text blocks nicely
    y = 50
    # Name
    page.insert_text(fitz.Point(50, y), cand["full_name"], fontsize=18, fontname=font_name)
    y += 24

    # Title & Contact
    contact_line = f"{cand['title']} | Email: {cand['email']} | ĐT: {cand['phone']}"
    page.insert_text(fitz.Point(50, y), contact_line, fontsize=10, fontname=font_name)
    y += 18

    # Separator line
    page.draw_line(fitz.Point(50, y), fitz.Point(545, y), color=(0.2, 0.4, 0.8), width=1.5)
    y += 25

    # Content
    content = build_cv_text_blocks(cand)
    # Split into paragraphs and insert
    rect = fitz.Rect(50, y, 545, 800)
    
    # Insert textbox to wrap properly
    page.insert_textbox(rect, content, fontsize=9.5, fontname=font_name, lineheight=1.3)
    
    doc.save(output_path)
    doc.close()


def generate_docx_cv(cand: dict, output_path: str):
    """Generate a clean, structured DOCX document using python-docx."""
    doc = docx.Document()
    
    # Set standard margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # Header Name
    p_name = doc.add_paragraph()
    run_name = p_name.add_run(cand["full_name"])
    run_name.font.size = Pt(18)
    run_name.font.bold = True
    run_name.font.color.rgb = RGBColor(12, 26, 45) # Deep navy

    # Subtitle
    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run(f"{cand['title']} | Email: {cand['email']} | ĐT: {cand['phone']}")
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_heading("1. Tóm tắt bản thân (Summary)", level=2)
    doc.add_paragraph(cand["summary"])

    doc.add_heading("2. Học vấn (Education)", level=2)
    for edu in cand.get("education", []):
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f"{edu['institution']} - {edu.get('degree', 'Cử nhân')} ({edu.get('field_of_study', '')})\n").bold = True
        p.add_run(f"Thời gian: {edu.get('start_date', '')} - {edu.get('end_date', '')} | Điểm GPA: {edu.get('gpa', 'N/A')}")

    doc.add_heading("3. Kinh nghiệm làm việc (Experience)", level=2)
    for exp in cand.get("experience", []):
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f"{exp['company_name']} - {exp['job_title']} ({exp.get('start_date', '')} - {exp.get('end_date', '')})\n").bold = True
        p.add_run(exp['description'])

    doc.add_heading("4. Kỹ năng chuyên môn (Hard Skills)", level=2)
    doc.add_paragraph(", ".join(cand.get("hard_skills", [])))

    if cand.get("negative_skills"):
        doc.add_heading("Lưu ý về kỹ năng chưa có (Negative Skills Context)", level=2)
        for neg in cand["negative_skills"]:
            p = doc.add_paragraph(style='List Bullet')
            p.add_run(f"Chưa có kinh nghiệm sử dụng {neg}. Chưa từng làm việc thực tế với {neg}.").italic = True

    doc.add_heading("5. Kỹ năng mềm (Soft Skills)", level=2)
    doc.add_paragraph(", ".join(cand.get("soft_skills", [])))

    if cand.get("certifications"):
        doc.add_heading("6. Chứng chỉ (Certifications)", level=2)
        for cert in cand["certifications"]:
            doc.add_paragraph(cert, style='List Bullet')

    doc.save(output_path)


def generate_all_cv_and_ground_truth():
    print(f"[Generate CVs] Starting generation for {len(CANDIDATES_DATA)} candidate CVs...")
    
    gt_summary = []
    
    for i, cand in enumerate(CANDIDATES_DATA):
        file_name = cand["file_name"]
        file_type = cand["file_type"]
        out_path = os.path.join(UPLOAD_DIR, file_name)
        
        # 1. Generate Binary File
        if file_type == "pdf":
            generate_pdf_cv(cand, out_path)
        else:
            generate_docx_cv(cand, out_path)

        file_size = os.path.getsize(out_path)

        # 2. Build Ground Truth JSON
        gt_data = {
            "candidate_id": cand["id"],
            "expected_name": cand["full_name"],
            "expected_email": cand["email"],
            "expected_phone": cand["phone"],
            "file_name": file_name,
            "file_type": file_type,
            "file_size_bytes": file_size,
            "test_case": cand["test_case"],
            "target_job_id": cand["target_job_id"],
            "expected_title": cand["title"],
            "expected_hard_skills": cand["hard_skills"],
            "expected_soft_skills": cand["soft_skills"],
            "expected_negative_skills": cand.get("negative_skills", []),
            "expected_education_institutions": [e["institution"] for e in cand.get("education", [])],
            "expected_experience_companies": [e["company_name"] for e in cand.get("experience", [])],
            "expected_certifications": cand.get("certifications", []),
            "expected_match_score_range": cand["expected_match_range"],
            "expected_evaluation": cand["expected_evaluation"],
            "source_evidence": {
                "summary": cand["summary"],
                "experience_evidence": cand.get("experience", []),
                "negative_skills_statement": [
                    f"Chưa có kinh nghiệm sử dụng {neg}" for neg in cand.get("negative_skills", [])
                ]
            }
        }

        # Save to both ground truth directories
        gt_filename = f"GT_{cand['id']}_{cand['full_name'].replace(' ', '_')}.json"
        with open(os.path.join(GROUND_TRUTH_DIR, gt_filename), "w", encoding="utf-8") as f:
            json.dump(gt_data, f, ensure_ascii=False, indent=2)

        with open(os.path.join(REPORT_GT_DIR, gt_filename), "w", encoding="utf-8") as f:
            json.dump(gt_data, f, ensure_ascii=False, indent=2)

        gt_summary.append({
            "stt": i + 1,
            "candidate_id": cand["id"],
            "name": cand["full_name"],
            "file_name": file_name,
            "format": file_type.upper(),
            "test_case": cand["test_case"],
            "target_job_id": cand["target_job_id"],
            "expected_range": f"{cand['expected_match_range'][0]}-{cand['expected_match_range'][1]}%"
        })

    # Save Master Ground Truth Registry
    registry_path = os.path.join(REPORT_GT_DIR, "MASTER_GROUND_TRUTH_REGISTRY.json")
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(gt_summary, f, ensure_ascii=False, indent=2)

    print(f"[Generate CVs] Successfully generated 30 physical CV files in '{UPLOAD_DIR}'")
    print(f"[Generate CVs] Successfully saved 30 Ground Truth files in '{GROUND_TRUTH_DIR}' and '{REPORT_GT_DIR}'")


if __name__ == "__main__":
    generate_all_cv_and_ground_truth()


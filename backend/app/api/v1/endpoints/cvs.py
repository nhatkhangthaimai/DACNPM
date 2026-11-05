import os
import uuid
import time
import hmac
import hashlib
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Body, status, Request, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_current_user_payload
from app.core.rate_limiter import upload_rate_limiter
from app.core.audit import log_audit_event
from app.core.storage import get_storage_service
from app.models.entities import CV, CandidateProfile, MatchResult, User, Company
from app.schemas.all_schemas import CVResponse, CVExtractedData, GenericMessageResponse
from app.ai.pipeline import (
    validate_cv_file,
    extract_text_from_cv,
    gemini_extract_structured_cv,
    generate_embedding,
    validate_extracted_text
)

router = APIRouter()


@router.get("", response_model=List[CVResponse])
async def get_candidate_cvs(candidate_id: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(CV)
    if candidate_id:
        prof_res = await db.execute(
            select(CandidateProfile).where(
                (CandidateProfile.id == candidate_id) | (CandidateProfile.user_id == candidate_id)
            )
        )
        prof = prof_res.scalars().first()
        if prof:
            query = query.where((CV.candidate_id == prof.id) | (CV.candidate_id == candidate_id))
        else:
            query = query.where(CV.candidate_id == candidate_id)
    result = await db.execute(query.order_by(CV.created_at.desc()))
    cvs = result.scalars().all()

    return [
        CVResponse(
            id=c.id,
            candidate_id=c.candidate_id,
            file_name=c.file_name,
            file_url=c.file_url,
            file_size=c.file_size,
            is_primary=c.is_primary,
            extraction_status=c.extraction_status,
            extraction_error=c.extraction_error,
            content_validated=c.content_validated or False,
            parsed_data=CVExtractedData(**c.parsed_data) if c.parsed_data and "error" not in c.parsed_data else None,
            created_at=c.created_at
        )
        for c in cvs
    ]


@router.get("/{cv_id}", response_model=CVResponse)
async def get_cv_detail(cv_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CV).where(CV.id == cv_id))
    c = result.scalars().first()
    if not c:
        raise HTTPException(status_code=404, detail="Không tìm thấy CV.")

    return CVResponse(
        id=c.id,
        candidate_id=c.candidate_id,
        file_name=c.file_name,
        file_url=c.file_url,
        file_size=c.file_size,
        is_primary=c.is_primary,
        extraction_status=c.extraction_status,
        extraction_error=c.extraction_error,
        content_validated=c.content_validated or False,
        parsed_data=CVExtractedData(**c.parsed_data) if c.parsed_data and "error" not in c.parsed_data else None,
        created_at=c.created_at
    )


@router.post("/upload", response_model=CVResponse)
async def upload_and_process_cv(
    file: UploadFile = File(...),
    candidate_id: str = Form("test-cand-1"),
    db: AsyncSession = Depends(get_db)
):
    """
    Robust CV Upload and Processing Pipeline:
    Step 1: Validate file format, magic bytes, size (reject invalid immediately)
    Step 2: Extract text using PyMuPDF (fitz) or python-docx
    Step 3: Validate extracted text quality (reject binary %PDF-, unreadable text)
    Step 4: If extraction succeeds, invoke Gemini AI / structured extraction
    Step 5: Generate and store dense vector embedding
    Step 6: Invalidate previous match results for this CV
    """
    contents = await file.read()

    # Step 1: Validate file signature & format
    is_valid_file, file_type, file_err = validate_cv_file(file.filename, contents, file.content_type)
    if not is_valid_file:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=file_err)

    # Save to uploads dir with safe sanitized unique filename (protects against path traversal & non-ASCII filenames)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    import re
    clean_base = re.sub(r'[^a-zA-Z0-9_-]', '_', os.path.splitext(file.filename)[0][:35]) or "cv"
    safe_storage_name = f"cv_{uuid.uuid4().hex[:10]}_{clean_base}.{file_type}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_storage_name)
    with open(file_path, "wb") as f:
        f.write(contents)

    saved_file_url = f"/uploads/{safe_storage_name}"

    # Step 2 & 3: Extract & Validate text quality (Supports PDF, DOCX, and Mobile Image CVs)
    raw_text, ext_ok, ext_err = extract_text_from_cv(contents, file.filename, file.content_type)

    # Resolve target_candidate_id
    target_candidate_id = candidate_id
    prof_res = await db.execute(
        select(CandidateProfile).where(
            (CandidateProfile.id == candidate_id) | (CandidateProfile.user_id == candidate_id)
        )
    )
    prof = prof_res.scalars().first()
    if prof:
        target_candidate_id = prof.id
    else:
        user_res = await db.execute(select(User).where(User.id == candidate_id))
        user_obj = user_res.scalars().first()
        if user_obj:
            new_prof = CandidateProfile(user_id=user_obj.id, title="Candidate Profile")
            db.add(new_prof)
            await db.flush()
            target_candidate_id = new_prof.id
        else:
            any_prof = (await db.execute(select(CandidateProfile))).scalars().first()
            if any_prof:
                target_candidate_id = any_prof.id

    if not ext_ok:
        # Extraction failed - mark CV as extraction_failed, DO NOT call Gemini, DO NOT embed
        cv = CV(
            candidate_id=target_candidate_id,
            file_name=file.filename,
            file_url=saved_file_url,
            file_size=len(contents),
            mime_type=file.content_type or f"application/{file_type}",
            raw_text=None,
            is_primary=True,
            extraction_status="extraction_failed",
            extraction_error=ext_err,
            content_validated=False,
            parsed_data={"error": ext_err, "full_name": None, "missing_fields": [ext_err]},
            embedding=None
        )
        db.add(cv)
        await db.commit()
        await db.refresh(cv)

        return CVResponse(
            id=cv.id,
            candidate_id=cv.candidate_id,
            file_name=cv.file_name,
            file_url=cv.file_url,
            file_size=cv.file_size,
            is_primary=cv.is_primary,
            extraction_status=cv.extraction_status,
            extraction_error=cv.extraction_error,
            content_validated=False,
            parsed_data=None,
            created_at=cv.created_at
        )

    # Step 4: Structured extraction via Gemini / heuristic NLP
    try:
        extracted_json = await gemini_extract_structured_cv(raw_text)
    except Exception as e:
        extracted_json = {"error": str(e), "full_name": None, "missing_fields": ["Lỗi phân tích AI"]}

    # Clean any accidental PDF markers
    candidate_name = extracted_json.get("full_name") or ""
    if "%PDF" in candidate_name or "/" in candidate_name:
        extracted_json["full_name"] = None

    # Step 5: Generate Embedding from valid CV text
    embedding_vec = generate_embedding(raw_text)

    # Step 6: Invalidate previous match results for this candidate CV
    existing_cvs = await db.execute(select(CV).where(CV.candidate_id == target_candidate_id, CV.file_name == file.filename))
    for old_cv in existing_cvs.scalars().all():
        await db.execute(delete(MatchResult).where(MatchResult.cv_id == old_cv.id))

    content_validated = bool(extracted_json.get("full_name") or extracted_json.get("hard_skills"))

    # Persist in DB
    cv = CV(
        candidate_id=target_candidate_id,
        file_name=file.filename,
        file_url=saved_file_url,
        file_size=len(contents),
        mime_type=file.content_type or f"application/{file_type}",
        raw_text=raw_text[:20000],
        is_primary=True,
        extraction_status="completed",
        extraction_error=None,
        content_validated=content_validated,
        parsed_data=extracted_json,
        embedding=embedding_vec
    )
    db.add(cv)
    await db.commit()
    await db.refresh(cv)

    parsed_obj = None
    if "error" not in extracted_json:
        try:
            parsed_obj = CVExtractedData(**extracted_json)
        except Exception:
            parsed_obj = None

    return CVResponse(
        id=cv.id,
        candidate_id=cv.candidate_id,
        file_name=cv.file_name,
        file_url=cv.file_url,
        file_size=cv.file_size,
        is_primary=cv.is_primary,
        extraction_status=cv.extraction_status,
        extraction_error=None,
        content_validated=cv.content_validated,
        parsed_data=parsed_obj,
        created_at=cv.created_at
    )


@router.delete("/{cv_id}")
async def delete_cv(cv_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CV).where(CV.id == cv_id))
    cv = result.scalars().first()
    if not cv:
        raise HTTPException(status_code=404, detail="Không tìm thấy CV.")

    # Remove associated match results
    await db.execute(delete(MatchResult).where(MatchResult.cv_id == cv_id))
    await db.delete(cv)
    await db.commit()

    return {"status": "success", "message": "CV đã được xoá thành công."}


@router.put("/{cv_id}/primary")
async def set_primary_cv(cv_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CV).where(CV.id == cv_id))
    target_cv = result.scalars().first()
    if not target_cv:
        raise HTTPException(status_code=404, detail="Không tìm thấy CV.")

    # Unset other primary CVs for this candidate
    other_cvs = await db.execute(select(CV).where(CV.candidate_id == target_cv.candidate_id))
    for c in other_cvs.scalars().all():
        c.is_primary = (c.id == cv_id)

    await db.commit()
    return {"status": "success", "message": "Đã đặt CV làm CV chính."}


@router.put("/{cv_id}/parsed-data", response_model=CVResponse)
async def update_cv_parsed_data(
    cv_id: str,
    updated_data: Dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Allow candidate to review, correct, and confirm AI-extracted CV information.
    """
    result = await db.execute(select(CV).where(CV.id == cv_id))
    cv = result.scalars().first()
    if not cv:
        raise HTTPException(status_code=404, detail="Không tìm thấy CV.")

    # Merge or overwrite parsed_data
    current_data = dict(cv.parsed_data or {})
    if "error" in current_data:
        del current_data["error"]
    for key, val in updated_data.items():
        if val is not None:
            current_data[key] = val

    # Ensure list defaults
    for list_field in ["hard_skills", "soft_skills", "education", "experience", "projects", "certifications", "languages"]:
        if list_field not in current_data:
            current_data[list_field] = []

    cv.parsed_data = current_data
    cv.content_validated = True
    cv.extraction_status = "completed"
    cv.extraction_error = None

    # Re-generate embedding based on confirmed skills & summary
    skills_text = " ".join(current_data.get("hard_skills", []))
    summary_text = current_data.get("summary", "") or ""
    combined_text = f"{cv.raw_text or ''} {skills_text} {summary_text}".strip()
    if combined_text:
        cv.embedding = generate_embedding(combined_text)

    await db.commit()
    await db.refresh(cv)

    parsed_obj = None
    if "error" not in cv.parsed_data:
        try:
            parsed_obj = CVExtractedData(**cv.parsed_data)
        except Exception:
            parsed_obj = None

    return CVResponse(
        id=cv.id,
        candidate_id=cv.candidate_id,
        file_name=cv.file_name,
        file_url=cv.file_url,
        file_size=cv.file_size,
        is_primary=cv.is_primary,
        extraction_status=cv.extraction_status,
        extraction_error=None,
        content_validated=cv.content_validated,
        parsed_data=parsed_obj,
        created_at=cv.created_at
    )


# ================= AVATAR & COMPANY LOGO UPLOAD ENDPOINTS =================
@router.post("/upload-avatar")
async def upload_candidate_avatar(
    file: UploadFile = File(...),
    user_id: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and sanitize candidate avatar (JPG, PNG, WEBP, HEIC/HEIF).
    Fixes mobile orientation, crops to square, and limits to 5MB.
    """
    contents = await file.read()
    from app.ai.pipeline import process_and_save_image

    ok, img_url, err = process_and_save_image(contents, file.filename, max_size_mb=5, is_avatar=True)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    return {
        "status": "success",
        "file_url": img_url,
        "message": "Tải ảnh đại diện thành công."
    }


@router.post("/upload-logo")
async def upload_company_logo(
    file: UploadFile = File(...),
    company_id: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and sanitize company logo (JPG, PNG, WEBP, HEIC/HEIF).
    """
    contents = await file.read()
    from app.ai.pipeline import process_and_save_image

    ok, img_url, err = process_and_save_image(contents, file.filename, max_size_mb=5, is_logo=True)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    if company_id:
        res = await db.execute(select(Company).where(Company.id == company_id))
        comp = res.scalars().first()
        if comp:
            comp.logo_url = img_url
            await db.commit()

    return {
        "status": "success",
        "logo_url": img_url,
        "message": "Tải logo công ty thành công."
    }


# ================= CV MANAGEMENT & SECURE DOWNLOAD =================
@router.delete("/{cv_id}", response_model=GenericMessageResponse)
async def delete_cv(
    cv_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: Optional[dict] = Depends(get_current_user_payload)
):
    """
    Deletes CV, associated match results, and physical storage object.
    Complies with Phase 5 candidate control & Phase 3 right to erasure.
    """
    res = await db.execute(select(CV).where(CV.id == cv_id))
    cv = res.scalars().first()
    if not cv:
        raise HTTPException(status_code=404, detail="Không tìm thấy CV.")

    # Remove physical storage file
    if cv.file_url:
        storage = get_storage_service()
        await storage.delete_file(cv.file_url.replace("/uploads/", ""))

    await db.execute(delete(MatchResult).where(MatchResult.cv_id == cv.id))
    await db.delete(cv)

    await log_audit_event(
        db,
        action="cv.deleted",
        user_id=auth_payload.get("sub") if auth_payload else None,
        target_type="cv",
        target_id=cv_id,
        details={"file_name": cv.file_name},
        request=request
    )
    await db.commit()
    return GenericMessageResponse(message="Đã xóa CV thành công.", status="success")


@router.put("/{cv_id}/primary", response_model=CVResponse)
async def set_primary_cv(
    cv_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    auth_payload: Optional[dict] = Depends(get_current_user_payload)
):
    """Sets the designated CV as the primary CV for automatic job matching."""
    res = await db.execute(select(CV).where(CV.id == cv_id))
    cv = res.scalars().first()
    if not cv:
        raise HTTPException(status_code=404, detail="Không tìm thấy CV.")

    all_cand_cvs = await db.execute(select(CV).where(CV.candidate_id == cv.candidate_id))
    for c in all_cand_cvs.scalars().all():
        c.is_primary = (c.id == cv.id)

    await log_audit_event(
        db,
        action="cv.set_primary",
        user_id=auth_payload.get("sub") if auth_payload else None,
        target_type="cv",
        target_id=cv_id,
        request=request
    )
    await db.commit()
    await db.refresh(cv)

    return CVResponse(
        id=cv.id,
        candidate_id=cv.candidate_id,
        file_name=cv.file_name,
        file_url=cv.file_url,
        file_size=cv.file_size,
        is_primary=cv.is_primary,
        extraction_status=cv.extraction_status,
        extraction_error=cv.extraction_error,
        content_validated=cv.content_validated or False,
        parsed_data=CVExtractedData(**cv.parsed_data) if cv.parsed_data and "error" not in cv.parsed_data else None,
        created_at=cv.created_at
    )


@router.get("/download/{storage_key}")
async def download_cv_file(
    storage_key: str,
    expires: int = Query(...),
    sig: str = Query(...)
):
    """
    OWASP secure token-protected CV download.
    Validates HMAC-SHA256 signature and expiration timestamp.
    """
    now = int(time.time())
    if now > expires:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Liên kết tải tệp tin đã hết hạn (quá 15 phút). Vui lòng yêu cầu liên kết mới."
        )

    sig_data = f"{storage_key}:{expires}".encode("utf-8")
    expected_sig = hmac.new(settings.SECRET_KEY.encode("utf-8"), sig_data, hashlib.sha256).hexdigest()[:16]

    if not hmac.compare_digest(sig, expected_sig):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chữ ký xác thực tệp không hợp lệ."
        )

    safe_name = os.path.basename(storage_key)
    file_path = os.path.join(settings.UPLOAD_DIR, safe_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Tệp tin không tồn tại trên hệ thống.")

    return FileResponse(file_path, filename=safe_name)




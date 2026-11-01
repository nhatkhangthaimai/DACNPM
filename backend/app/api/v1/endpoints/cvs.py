import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.core.database import get_db
from app.core.config import settings
from app.models.entities import CV, CandidateProfile, MatchResult, User
from app.schemas.all_schemas import CVResponse, CVExtractedData
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

    # Save to uploads dir
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Step 2 & 3: Extract & Validate text quality
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
            file_url=f"/uploads/{file.filename}",
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
        file_url=f"/uploads/{file.filename}",
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


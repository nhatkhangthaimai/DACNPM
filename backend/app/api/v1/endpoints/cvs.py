import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.config import settings
from app.models.entities import CV, CandidateProfile
from app.schemas.all_schemas import CVResponse, CVExtractedData
from app.ai.pipeline import extract_text_from_pdf, gemini_extract_structured_cv

router = APIRouter()


@router.get("", response_model=List[CVResponse])
async def get_candidate_cvs(candidate_id: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(CV)
    if candidate_id:
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
            parsed_data=CVExtractedData(**c.parsed_data) if c.parsed_data else None,
            created_at=c.created_at
        )
        for c in cvs
    ]


@router.post("/upload", response_model=CVResponse)
async def upload_and_process_cv(
    file: UploadFile = File(...),
    candidate_id: str = Form("user-cand-1"),
    db: AsyncSession = Depends(get_db)
):
    # Verify file extension
    ext = file.filename.split(".")[-1].lower() if file.filename else ""
    if ext not in ["pdf", "docx", "doc"]:
        raise HTTPException(status_code=400, detail="Định dạng tệp không được hỗ trợ. Vui lòng tải PDF hoặc DOCX.")

    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Kích thước tệp vượt quá 10MB.")

    # Save to uploads dir
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    # Extract text & invoke Gemini LLM extraction pipeline
    raw_text = extract_text_from_pdf(contents)
    extracted_json = await gemini_extract_structured_cv(raw_text)

    # Persist in DB
    cv = CV(
        candidate_id=candidate_id,
        file_name=file.filename,
        file_url=f"/uploads/{file.filename}",
        file_size=len(contents),
        mime_type=file.content_type or "application/pdf",
        raw_text=raw_text[:20000],
        is_primary=True,
        extraction_status="completed",
        parsed_data=extracted_json,
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
        parsed_data=CVExtractedData(**extracted_json),
        created_at=cv.created_at
    )

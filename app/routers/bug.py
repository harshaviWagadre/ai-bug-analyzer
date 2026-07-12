import json
import os
import shutil
from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Bug
from app.schemas import AnalyzeResponse, BugListResponse, BugRecord
from app.services.gemini import analyze_bug

router = APIRouter()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".txt", ".log", ".md"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _save_uploaded_file(upload_file: UploadFile) -> str:
    filename = upload_file.filename or "uploaded_file"
    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Please upload a .txt, .log, or .md file.",
        )

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return filepath


def _read_uploaded_content(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as handle:
        return handle.read().strip()


def _serialize_analysis(ai_analysis: Any) -> dict[str, Any]:
    if isinstance(ai_analysis, str):
        try:
            return json.loads(ai_analysis)
        except json.JSONDecodeError:
            return {"raw_analysis": ai_analysis}
    if isinstance(ai_analysis, dict):
        return ai_analysis
    return {}


async def _process_bug_submission(
    title: str,
    description: str,
    bug_file: UploadFile | None,
    db: Session,
) -> dict[str, Any]:
    cleaned_title = (title or "").strip()
    cleaned_description = (description or "").strip()

    if not cleaned_title and not cleaned_description and bug_file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a title, description, or upload a file.",
        )

    if not cleaned_title:
        cleaned_title = "Untitled Bug Report"

    filename = None
    file_content = ""

    if bug_file is not None:
        if bug_file.filename is None or not bug_file.filename.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file is missing a name.",
            )

        filepath = _save_uploaded_file(bug_file)
        filename = os.path.basename(filepath)
        file_content = _read_uploaded_content(filepath)

        if not file_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file is empty. Please add content and try again.",
            )

    combined_text = "\n\n".join(
        part for part in [cleaned_description, file_content] if part
    ).strip()
    if not combined_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide a bug description or upload a file.",
        )

    try:
        ai_result = analyze_bug(combined_text)
    except Exception as exc:  # pragma: no cover - defensive path
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI analysis failed: {exc}",
        ) from exc

    new_bug = Bug(
        title=cleaned_title,
        description=cleaned_description or combined_text,
        filename=filename,
        ai_analysis=json.dumps(ai_result),
    )

    db.add(new_bug)
    try:
        db.commit()
        db.refresh(new_bug)
    except Exception as exc:  # pragma: no cover - defensive path
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not save the bug to the database: {exc}",
        ) from exc

    return {
        "message": "Bug Submitted Successfully",
        "bug_id": new_bug.id,
        "title": new_bug.title,
        "filename": new_bug.filename,
        "ai_analysis": _serialize_analysis(ai_result),
    }


@router.post("/analyze", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK)
async def analyze_bug_endpoint(
    title: str = Form(default=""),
    description: str = Form(default=""),
    bug_file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    result = await _process_bug_submission(title, description, bug_file, db)
    return result


@router.post(
    "/submit-bug", response_model=AnalyzeResponse, status_code=status.HTTP_200_OK
)
async def submit_bug(
    title: str = Form(default=""),
    description: str = Form(default=""),
    bug_file: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
):
    return await analyze_bug_endpoint(
        title=title, description=description, bug_file=bug_file, db=db
    )


@router.get("/bugs", response_model=BugListResponse)
def list_bugs(db: Session = Depends(get_db)):
    bugs = db.query(Bug).order_by(Bug.created_at.desc()).all()
    return {
        "bugs": [
            BugRecord(
                id=bug.id,
                title=bug.title,
                description=bug.description,
                filename=bug.filename,
                ai_analysis=_serialize_analysis(bug.ai_analysis),
                created_at=bug.created_at.isoformat() if bug.created_at else None,
            ).model_dump()
            for bug in bugs
        ]
    }


@router.get("/bugs/{bug_id}", response_model=BugRecord)
def get_bug(bug_id: int, db: Session = Depends(get_db)):
    bug = db.query(Bug).filter(Bug.id == bug_id).first()
    if bug is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bug not found"
        )

    return BugRecord(
        id=bug.id,
        title=bug.title,
        description=bug.description,
        filename=bug.filename,
        ai_analysis=_serialize_analysis(bug.ai_analysis),
        created_at=bug.created_at.isoformat() if bug.created_at else None,
    )

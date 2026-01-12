from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models_program import Lesson, Term
from app.deps import require_role

router = APIRouter(prefix="/cms/lessons", tags=["Lessons"])

@router.post("/")
def create_lesson(data: dict, db: Session = Depends(get_db), role: str = Depends(require_role)):
    if role not in ("admin", "editor"):
        raise HTTPException(status_code=403, detail="Insufficient privileges")

    term_id = data.get("term_id")
    if not term_id:
        raise HTTPException(status_code=400, detail="term_id is required")

    lesson = Lesson(
        title=data.get("title"),
        lesson_number=data.get("lesson_number", 1),
        content_type=data.get("content_type", "video"),
        content_language_primary=data.get("content_language_primary", "en"),
        duration_ms=data.get("duration_ms", 60000),
        status="draft",
        term_id=term_id,
        created_at=datetime.utcnow(),
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return {"message": "Lesson created", "id": lesson.id}

@router.put("/{lesson_id}/status")
def update_lesson_status(lesson_id: str, data: dict, db: Session = Depends(get_db), role: str = Depends(require_role)):
    """Publish, schedule, or archive lesson"""
    if role not in ("admin", "editor"):
        raise HTTPException(status_code=403, detail="Insufficient privileges")

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    new_status = data.get("status")
    if new_status not in ["draft", "scheduled", "published", "archived"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    if new_status == "scheduled":
        lesson.publish_at = data.get("publish_at")
        if not lesson.publish_at:
            raise HTTPException(status_code=400, detail="publish_at is required for scheduling")

    if new_status == "published":
        lesson.published_at = datetime.utcnow()

    lesson.status = new_status
    db.commit()
    return {"message": f"Lesson {new_status}"}

@router.get("/term/{term_id}")
def get_lessons_by_term(term_id: str, db: Session = Depends(get_db), role: str = Depends(require_role)):
    query = db.query(Lesson).filter(Lesson.term_id == term_id)
    if role == "viewer":
        query = query.filter(Lesson.status == "published")

    lessons = query.all()
    return [
        {
            "id": l.id,
            "title": l.title,
            "status": l.status,
            "lesson_number": l.lesson_number,
            "publish_at": l.publish_at,
            "published_at": l.published_at,
        }
        for l in lessons
    ]

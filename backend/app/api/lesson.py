from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models_program import Lesson
from app.api.auth import require_editor_or_admin

router = APIRouter(prefix="/cms", tags=["lessons"])

@router.post("/lessons/{lesson_id}/archive")
def archive_lesson(
    lesson_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_editor_or_admin),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    if lesson.status == "archived":
        return {"message": "Lesson already archived"}

    lesson.status = "archived"
    lesson.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(lesson)

    return {"message": "Lesson archived", "lesson_id": lesson_id, "status": "archived"}

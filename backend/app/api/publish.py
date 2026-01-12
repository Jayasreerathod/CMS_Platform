from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models_program import Lesson
from app.deps import require_role

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/run")
def publish_scheduled(db: Session = Depends(get_db), user=Depends(require_role(["admin"]))):
    lessons = db.query(Lesson).filter(Lesson.status == "scheduled", Lesson.publish_at <= datetime.utcnow()).all()
    for lesson in lessons:
        lesson.status = "published"
        lesson.published_at = datetime.utcnow()
    db.commit()
    return {"published": len(lessons)}

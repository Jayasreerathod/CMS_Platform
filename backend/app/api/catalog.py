from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models_program import Program, Lesson, StatusEnum

router = APIRouter(tags=["Catalog"])

@router.get("/programs")
def get_catalog_programs(db: Session = Depends(get_db)):
    programs = (
        db.query(Program)
        .filter(Program.status == StatusEnum.published)
        .order_by(Program.published_at.desc())
        .all()
    )
    return programs

@router.get("/programs/{program_id}")
def get_program_lessons(program_id: str, db: Session = Depends(get_db)):
    program = (
        db.query(Program)
        .filter(Program.id == program_id, Program.status == StatusEnum.published)
        .first()
    )
    if not program:
        return {"error": "Program not found or unpublished"}
    lessons = (
        db.query(Lesson)
        .filter(Lesson.program_id == program_id, Lesson.status == StatusEnum.published)
        .order_by(Lesson.lesson_number)
        .all()
    )
    return {"program": program, "lessons": lessons or []}

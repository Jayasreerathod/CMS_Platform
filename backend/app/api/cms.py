from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models_program import Program, Lesson, StatusEnum

router = APIRouter(tags=["CMS"])

# -------------------------------
# ROLE-BASED ACCESS CONTROL (RBAC)
# -------------------------------
def get_current_user():
    """
    Temporary role simulation.
    You can later connect this to real JWT auth (admin@cms.com / editor@cms.com).
    """
    return {"email": "editor@cms.com", "role": "editor"}  # or admin

def require_role(required_role: str):
    def checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role.capitalize()} role required.",
            )
        return user
    return checker

def require_admin_or_editor(user=Depends(get_current_user)):
    if user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user

# -------------------------------
# PROGRAM ENDPOINTS
# -------------------------------

@router.get("/programs")
def list_programs(db: Session = Depends(get_db)):
    programs = db.query(Program).all()
    return programs


@router.post("/programs")
def create_program(
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(require_admin_or_editor),
):
    new_program = Program(
        title=data.get("title"),
        description=data.get("description", ""),
        status=StatusEnum.draft,
    )
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program


@router.post("/programs/{program_id}/publish")
def publish_program(
    program_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin")),  #  only admin can publish
):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    program.status = StatusEnum.published
    program.published_at = datetime.utcnow()
    db.commit()
    db.refresh(program)
    return {"message": "Program published", "program": program}


@router.post("/programs/{program_id}/schedule")
def schedule_program_publish(
    program_id: str,
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(require_role("editor")),  #  only editors schedule
):
    """Schedule a program to be auto-published later."""
    publish_at_str = data.get("publish_at")
    if not publish_at_str:
        raise HTTPException(status_code=400, detail="publish_at is required")

    try:
        publish_at = datetime.fromisoformat(publish_at_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid datetime format")

    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    program.status = StatusEnum.scheduled
    program.published_at = publish_at
    db.commit()
    db.refresh(program)
    return {"message": f"Program scheduled for {publish_at}", "program": program}


@router.delete("/programs/{program_id}")
def delete_program(
    program_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_admin_or_editor),
):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    db.delete(program)
    db.commit()
    return {"message": "Program deleted"}


@router.get("/programs/{program_id}")
def get_program_details(program_id: str, db: Session = Depends(get_db)):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    lessons = db.query(Lesson).filter(Lesson.program_id == program_id).all()
    return {"program": program, "lessons": lessons or []}

# -------------------------------
# LESSON ENDPOINTS
# -------------------------------

@router.post("/programs/{program_id}/lessons")
def add_lesson(
    program_id: str,
    data: dict,
    db: Session = Depends(get_db),
    user=Depends(require_admin_or_editor),
):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    lesson = Lesson(
        title=data.get("title"),
        program_id=program_id,
        lesson_number=len(program.lessons) + 1,
        status=StatusEnum.draft,
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson


@router.delete("/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_admin_or_editor),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted"}

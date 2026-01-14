from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy import and_
from app.database import get_db
from app.models_program import Program, Lesson, StatusEnum, Term
from app.worker import run_scheduled_publisher

router = APIRouter(tags=["CMS"])

# --- Dummy auth for now (replaceable with JWT later) ---
def get_current_user():
    # default to admin for local testing
    return {"role": "admin"}

def require_admin_or_editor(user=Depends(get_current_user)):
    if user["role"] not in ["admin", "editor"]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return user


# ================= PROGRAMS =================
@router.get("/programs")
def list_programs(db: Session = Depends(get_db)):
    programs = db.query(Program).all()
    return programs


@router.post("/programs")
def create_program(data: dict, db: Session = Depends(get_db), user=Depends(require_admin_or_editor)):
    if not data.get("title"):
        raise HTTPException(status_code=400, detail="Program title required")

    new_program = Program(
        title=data["title"],
        description=data.get("description", ""),
        status=StatusEnum.draft,
        language_primary=data.get("language_primary", "en"),
        languages_available=data.get("languages_available", ["en"]),
    )
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    return new_program


@router.post("/programs/{program_id}/publish")
def publish_program(program_id: str, db: Session = Depends(get_db), user=Depends(require_admin_or_editor)):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    # Validate media requirements
    validate_program_assets(program)

    program.status = StatusEnum.published
    program.published_at = datetime.utcnow()
    db.commit()
    db.refresh(program)
    ...

    return {"message": "Program published", "program": program}


@router.delete("/programs/{program_id}")
def delete_program(program_id: str, db: Session = Depends(get_db), user=Depends(require_admin_or_editor)):
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

    terms = db.query(Term).filter(Term.program_id == program.id).all()
    lessons = db.query(Lesson).join(Term).filter(Term.program_id == program.id).all()
    return {"program": program, "terms": terms, "lessons": lessons}


# ================= LESSONS =================
@router.post("/programs/{program_id}/lessons")
def add_lesson(program_id: str, data: dict, db: Session = Depends(get_db), user=Depends(require_admin_or_editor)):
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")

    term = db.query(Term).filter(Term.program_id == program_id).first()
    if not term:
        # auto-create term 1 if missing
        term = Term(program_id=program_id, term_number=1, title="Default Term")
        db.add(term)
        db.commit()
        db.refresh(term)

    next_lesson_num = (db.query(Lesson).filter(Lesson.term_id == term.id).count() or 0) + 1

    new_lesson = Lesson(
        program_id=program_id,  # THIS FIXES THE ERROR
        title=data.get("title", f"Lesson {next_lesson_num}"),
        term_id=term.id,
        lesson_number=next_lesson_num,
        content_type=data.get("content_type", "video"),
        content_language_primary=data.get("content_language_primary", "en"),
        content_languages_available=data.get("content_languages_available", ["en"]),
        content_urls_by_language=data.get("content_urls_by_language", {"en": data.get("content_url", "")}),
        status=StatusEnum.draft,
    )

    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

@router.post("/lessons/{lesson_id}/schedule")
def schedule_lesson_publish(lesson_id: str, data: dict, background_tasks: BackgroundTasks,
                            db: Session = Depends(get_db), user=Depends(require_admin_or_editor)):
    """
    Schedule a lesson for publishing in the future.
    Payload example: { "publish_in_minutes": 2 }
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    publish_delay = data.get("publish_in_minutes", 1)
    lesson.status = StatusEnum.scheduled
    lesson.publish_at = datetime.utcnow() + timedelta(minutes=publish_delay)
    db.commit()

    background_tasks.add_task(run_scheduled_publisher)
    return {"message": f"Lesson scheduled to publish in {publish_delay} minutes."}


@router.post("/lessons/{lesson_id}/publish")
def publish_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return {"error": "Lesson not found"}, 404

    # ✅ Validate that required fields exist before publishing
    errors = []

    # Content URLs validation
    if not lesson.content_urls_by_language or not lesson.content_urls_by_language.get(lesson.content_language_primary):
        errors.append("Missing content URL for primary language.")

    # Thumbnail validation
    if not lesson.thumbnail_assets_by_language:
        errors.append("Missing thumbnails.")
    else:
        lang_assets = lesson.thumbnail_assets_by_language.get(lesson.content_language_primary, {})
        if not lang_assets.get("portrait") or not lang_assets.get("landscape"):
            errors.append("Portrait or landscape thumbnail missing for primary language.")

    # If errors exist, block publish
    if errors:
        return {"status": "error", "message": "Cannot publish", "details": errors}, 400

    # ✅ Update status and publish time
    lesson.status = StatusEnum.published
    lesson.published_at = datetime.utcnow()
    db.commit()

    return {"status": "success", "message": f"Lesson '{lesson.title}' published successfully."}

@router.post("/lessons/{lesson_id}/archive")
def archive_lesson(lesson_id: str, db: Session = Depends(get_db), user=Depends(require_admin_or_editor)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    lesson.status = StatusEnum.archived
    db.commit()
    db.refresh(lesson)
    return {"message": "Lesson archived", "lesson": lesson}

def validate_program_assets(program: Program):
    lang = program.language_primary
    posters = program.poster_assets_by_language or {}
    lang_assets = posters.get(lang, {})

    required_variants = ["portrait", "landscape"]
    for variant in required_variants:
        if not lang_assets.get(variant):
            raise HTTPException(
                status_code=400,
                detail=f"Missing required program poster '{variant}' for {lang}."
            )

def validate_lesson_assets(lesson: Lesson):
    lang = lesson.content_language_primary
    thumbs = lesson.thumbnail_assets_by_language or {}
    lang_assets = thumbs.get(lang, {})

    required_variants = ["portrait", "landscape"]
    for variant in required_variants:
        if not lang_assets.get(variant):
            raise HTTPException(
                status_code=400,
                detail=f"Missing required lesson thumbnail '{variant}' for {lang}."
            )

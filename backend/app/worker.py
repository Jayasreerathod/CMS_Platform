import time
from datetime import datetime, timezone
from sqlalchemy import and_
from app.database import SessionLocal
from app.models_program import Program, Lesson, StatusEnum


def run_worker_once():
    """Run one background publishing cycle."""
    db = SessionLocal()
    now = datetime.now(timezone.utc)

    try:
        print(f"[Worker] Running at {now.isoformat()}...")

        # Step 1: Find lessons scheduled for publishing
        scheduled_lessons = (
            db.query(Lesson)
            .filter(
                and_(
                    Lesson.status == StatusEnum.scheduled,
                    Lesson.publish_at <= now,
                )
            )
            .all()
        )

        if not scheduled_lessons:
            print("[Worker] No lessons to publish.")
        else:
            for lesson in scheduled_lessons:
                print(f"[Worker] Publishing lesson: {lesson.title}")
                lesson.status = StatusEnum.published
                lesson.published_at = now
                db.add(lesson)

                # Step 2: Auto-publish parent program if needed
                program = db.query(Program).filter(Program.id == lesson.program_id).first()
                if program and program.status != StatusEnum.published:
                    published_count = (
                        db.query(Lesson)
                        .filter(
                            Lesson.program_id == program.id,
                            Lesson.status == StatusEnum.published,
                        )
                        .count()
                    )
                    if published_count >= 1:
                        print(f"[Worker] Auto-publishing program: {program.title}")
                        program.status = StatusEnum.published
                        program.published_at = now
                        db.add(program)

            db.commit()
            print("[Worker]  Publishing cycle complete.")

    except Exception as e:
        db.rollback()
        print(f"[Worker]- Error: {e}")

    finally:
        db.close()


def start_worker():
    """Start infinite background worker loop."""
    print("Starting background worker... (Press Ctrl+C to stop)")
    while True:
        run_worker_once()
        time.sleep(60)  # check every 60 seconds


# --- Prevent auto-run when imported by FastAPI ---
if __name__ == "__main__":
    start_worker()
run_scheduled_publisher = run_worker_once
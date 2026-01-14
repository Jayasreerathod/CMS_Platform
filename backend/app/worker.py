import time
from datetime import datetime, timezone
from sqlalchemy import and_
from app.database import SessionLocal
from app.models_program import Program, Lesson, StatusEnum


def run_worker_once():
    """Runs a single background publishing cycle (idempotent)."""
    db = SessionLocal()
    now = datetime.now(timezone.utc)  # timezone-aware UTC

    try:
        print(f"[Worker] Running at {now.isoformat()}...")

        # Step 1: Find lessons that are scheduled and ready to publish
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

                # Step 2: Check if parent program should become published
                program = (
                    db.query(Program)
                    .filter(Program.id == lesson.program_id)
                    .first()
                )

                if program and program.status != StatusEnum.published:
                    # Only publish if there is at least one published lesson
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
            print("[Worker] - Publishing cycle complete.")

    except Exception as e:
        db.rollback()
        print(f"[Worker] ❌ Error: {e}")

    finally:
        db.close()


# --- Background loop for manual or deployment run ---
def start_worker():
    """Starts an infinite background loop to run every 60 seconds."""
    print(" Starting background worker... (Press Ctrl+C to stop)")
    while True:
        run_worker_once()
        time.sleep(60)  # run every minute


# --- Alias for backward compatibility ---
run_scheduled_publisher = run_worker_once


# --- Run manually if executed directly ---
if __name__ == "__main__":
    start_worker()

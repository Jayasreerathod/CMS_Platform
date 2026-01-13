import threading
import time
from datetime import datetime
from app.database import SessionLocal
from app.models_program import Program, StatusEnum

def run_scheduler():
    """Auto-publish scheduled programs when their publish time arrives."""
    db = SessionLocal()
    now = datetime.utcnow()
    programs = db.query(Program).filter(
        Program.status == StatusEnum.scheduled,
        Program.published_at <= now
    ).all()

    for p in programs:
        p.status = StatusEnum.published
        print(f"[Worker] Auto-published program: {p.title}")
    db.commit()
    db.close()

def start_worker():
    """Run the worker every 60 seconds."""
    def background():
        while True:
            try:
                run_scheduler()
            except Exception as e:
                print("[Worker Error]", e)
            time.sleep(60)
    threading.Thread(target=background, daemon=True).start()

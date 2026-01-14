from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, cms, catalog
from app.worker import start_worker
from app.database import SessionLocal, Base, engine
from app.models_program import Program
import threading
import traceback

app = FastAPI(title="LessonCMS Backend")

# --- CORS Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
app.include_router(auth.router, prefix="/auth")
app.include_router(cms.router, prefix="/cms")
app.include_router(catalog.router, prefix="/catalog")

# --- Import seeding script ---
from seed_data import db, Program  # reuses your logic safely

def auto_seed():
    """Automatically seed database if it's empty (Render safe)."""
    try:
        session = SessionLocal()
        if session.query(Program).first():
            print("Dtabase already has programs — skipping auto-seed.")
            session.close()
            return
        print(" Auto-seeding database...")
        import seed_data  # runs the seeding logic
        print(" Auto-seed completed successfully.")
        session.close()
    except Exception as e:
        print(" Auto-seed failed:", str(e))
        traceback.print_exc()


# --- Run background worker and auto-seed ---
@app.on_event("startup")
def startup_event():
    # Create tables if not exist
    Base.metadata.create_all(bind=engine)

    # Start background publishing worker
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()
    print(" Background worker thread started successfully!")

    # Run seed automatically
    auto_seed()


@app.get("/")
def home():
    return {"message": "LessonCMS backend running successfully 🚀"}

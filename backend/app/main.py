from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, cms, catalog
import threading
from app.worker import start_worker
from app.database import SessionLocal, engine, Base
from app.models_program import Program
from seed_data import main as run_seed  # assuming your seeding script is named seed_data.py

app = FastAPI(title="LessonCMS Backend")

# --- CORS ---
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


@app.on_event("startup")
def on_startup():
    """Ensure DB seeded and background worker starts without blocking Render."""
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        if not db.query(Program).first():
            print("Seeding database (Render startup)...")
            run_seed()
        else:
            print(" Database already has data — skipping seed.")
        db.close()
    except Exception as e:
        print(f" Seeding skipped: {e}")

    # Start worker safely
    threading.Thread(target=start_worker, daemon=True).start()
    print(" Background worker thread started successfully!")


@app.get("/")
def home():
    return {"message": "LessonCMS backend running successfully 🚀"}

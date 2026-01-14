from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine, Base, SessionLocal
from app.models_program import Program
from app.api import auth, cms, catalog
import threading
from app.worker import start_worker  # background publisher
from seed_data import main as run_seed

# ---------------------------------------------------------
# Initialize FastAPI app
# ---------------------------------------------------------
app = FastAPI(title="LessonCMS Backend")

# ---------------------------------------------------------
# CORS (frontend access)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cms-platform-phi.vercel.app",  # your deployed frontend
        "http://localhost:4173",                # local dev preview
        "http://localhost:5173",                # vite dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Routers
# ---------------------------------------------------------
app.include_router(auth.router, prefix="/auth")
app.include_router(cms.router, prefix="/cms")
app.include_router(catalog.router, prefix="/catalog")

# ---------------------------------------------------------
# Startup events
# ---------------------------------------------------------
@app.on_event("startup")
def start_background_worker():
    # --- Auto-run seeding logic ---
    try:
        db = SessionLocal()
        if not db.query(Program).first():
            print(" programs found — running auto-seed...")
            run_seed()
            print("Auto-seed complete.")
        else:
            print("rograms already exist — skipping auto-seed.")
        db.close()
    except Exception as e:
        print(f"Auto-seed failed: {e}")

    # --- Start background publishing worker ---
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()
    print("Background worker thread started successfully!")

@app.get("/")
def home():
    return {"message": "LessonCMS backend running successfully 🚀"}

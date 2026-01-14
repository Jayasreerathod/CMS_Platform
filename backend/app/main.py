from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine, Base
from app.api import auth, cms, catalog
import threading
from app.worker import start_worker  # background publisher

# ---------------------------------------------------------
# Initialize FastAPI app
# ---------------------------------------------------------
app = FastAPI(title="LessonCMS Backend")

# ---------------------------------------------------------
# Temporary DB Reset (runs once when deployed)
# ---------------------------------------------------------
@app.on_event("startup")
def reset_and_start():
    with engine.begin() as conn:
        # ⚠️ WARNING: This will drop old tables on every deploy
        conn.execute(text("""
            DROP TABLE IF EXISTS programs CASCADE;
            DROP TABLE IF EXISTS lessons CASCADE;
            DROP TABLE IF EXISTS terms CASCADE;
            DROP TABLE IF EXISTS program_assets CASCADE;
            DROP TABLE IF EXISTS lesson_assets CASCADE;
        """))
        print("✅ Dropped old tables successfully!")

    # Recreate tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database schema recreated successfully!")

    # Start background worker thread
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()
    print("✅ Background worker started successfully!")

# ---------------------------------------------------------
# CORS (important for frontend on Vercel)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://cms-platform-phi.vercel.app",  # your Vercel frontend
        "http://localhost:4173",                # for local testing
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

@app.get("/")
def home():
    return {"message": "LessonCMS backend running successfully 🚀"}

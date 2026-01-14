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
    # Ensure tables exist (but don't drop them anymore!)
    Base.metadata.create_all(bind=engine)
    print(" Database schema ensured.")

    # Start the background worker safely
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()
    print(" Background worker started successfully!")


@app.get("/")
def home():
    return {"message": "LessonCMS backend running successfully 🚀"}

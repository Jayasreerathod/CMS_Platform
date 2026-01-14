from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, cms, catalog
from app.database import Base, engine
from app.models_program import *  # Ensure models are registered
import threading
from app.worker import start_worker  # background publisher

app = FastAPI(title="LessonCMS Backend")

# --- Auto-create tables if not exist ---
Base.metadata.create_all(bind=engine)

# --- CORS (allow frontend access) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # for testing; replace with your Vercel domain for security
        "https://cms-platform-phi.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include routers ---
app.include_router(auth.router, prefix="/auth")
app.include_router(cms.router, prefix="/cms")
app.include_router(catalog.router, prefix="/catalog")

# --- Background worker ---
@app.on_event("startup")
def start_background_worker():
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()
    print(" Background worker started successfully!")

@app.get("/")
def home():
    return {"message": "LessonCMS backend running successfully 🚀"}

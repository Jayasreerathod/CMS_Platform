from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, cms, catalog
from app.database import Base, engine
from app.models_program import *
import threading
from app.worker import start_worker

app = FastAPI(title="LessonCMS Backend")

#  Auto-create tables (helps on first deploy)
Base.metadata.create_all(bind=engine)

# Allow both Vercel + localhost
origins = [
    "https://cms-platform-phi.vercel.app",
    "http://localhost:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(auth.router, prefix="/auth")
app.include_router(cms.router, prefix="/cms")
app.include_router(catalog.router, prefix="/catalog")

# --- Background Worker ---
@app.on_event("startup")
def start_background_worker():
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()
    print(" Background worker started successfully!")

@app.get("/")
def home():
    return {"message": "LessonCMS backend running successfully 🚀"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, cms, catalog
import threading
from app.worker import start_worker  # background publisher

app = FastAPI(title="LessonCMS Backend")

# --- CORS (for frontend to access API) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lessoncms.vercel.app","*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include routers ---
app.include_router(auth.router, prefix="/auth")
app.include_router(cms.router, prefix="/cms")
app.include_router(catalog.router, prefix="/catalog")

# --- Run background worker in a thread ---
@app.on_event("startup")
def start_background_worker():
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()
    print("Background worker thread started successfully!")


@app.get("/")
def home():
    return {"message": "LessonCMS backend running successfully 🚀"}

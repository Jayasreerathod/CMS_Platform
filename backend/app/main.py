from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, cms, catalog

app = FastAPI(title="LessonCMS")

@app.get("/")
def root():
    return {"message": "Welcome to LessonCMS API"}

origins = [
    "https://cms-platform-phi.vercel.app",  # your main frontend
    "https://cms-platform-4hq4cij8t-jayasree-rathods-projects.vercel.app",  # preview builds
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes
app.include_router(auth.router)
app.include_router(cms.router, prefix="/cms")
app.include_router(catalog.router, prefix="/catalog")

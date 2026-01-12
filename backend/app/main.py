from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, cms, catalog
from app.database import Base, engine  

app = FastAPI(title="LessonCMS")

#  Create DB tables if they don't exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to LessonCMS API"}

origins = [
    "https://cms-platform-phi.vercel.app",  # main frontend
    "https://cms-platform-4hq4cij8t-jayasree-rathods-projects.vercel.app",  # preview builds
    "http://localhost:5173",  # for local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ⬅ use list, not "*", for security and stability
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(cms.router, prefix="/cms")
app.include_router(catalog.router, prefix="/catalog")

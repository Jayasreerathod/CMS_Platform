from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, cms, catalog

#  First, define the FastAPI app
app = FastAPI(title="LessonCMS")

#  Then define your CORS origins
origins = [
    "https://cms-platform-phi.vercel.app",
    "https://cms-platform-byufhuv0k-jayasree-rathods-projects.vercel.app",
    "http://localhost:5173",
]

#  Then add the middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to LessonCMS API"}

app.include_router(auth.router)
app.include_router(cms.router, prefix="/cms")
app.include_router(catalog.router, prefix="/catalog")

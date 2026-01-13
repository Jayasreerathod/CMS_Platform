from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, cms, catalog
from app.worker import start_worker 

app = FastAPI(title="LessonCMS")

@app.get("/")
def root():
    return {"message": "Welcome to LessonCMS API"}

origins = [
    "https://cms-platform-phi.vercel.app",
    "https://cms-platform-*.vercel.app",
    "https://cms-platform-byufhuv0k-jayasree-rathods-projects.vercel.app"
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  start worker on app launch
@app.on_event("startup")
def startup_event():
    start_worker()

#  include existing routers
app.include_router(auth.router)
app.include_router(cms.router, prefix="/cms")
app.include_router(catalog.router, prefix="/catalog")

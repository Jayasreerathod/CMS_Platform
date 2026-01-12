from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://cms-platform-phi.vercel.app",
    "https://cms-platform-byufhuv0k-jayasree-rathods-projects.vercel.app",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

# Simple fake user database
USERS = {
    "admin@cms.com": {"password": "admin123", "role": "admin"},
    "editor@cms.com": {"password": "editor123", "role": "editor"},
    "viewer@cms.com": {"password": "viewer123", "role": "viewer"},
}

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    user = USERS.get(data.email)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Fake JWT token for simplicity
    token = f"fake-token-for-{data.email}"
    return {"token": token, "role": user["role"]}

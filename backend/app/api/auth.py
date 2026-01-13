from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["Auth"])

# Dummy login data
USERS = {
    "admin@cms.com": {"password": "admin123", "role": "admin"},
    "editor@cms.com": {"password": "editor123", "role": "editor"},
}

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/login")
def login(data: LoginRequest):
    user = USERS.get(data.email)
    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "token": f"fake-token-for-{data.email}",
        "role": user["role"],
    }

from fastapi import Depends, HTTPException, status
from app.auth import decode_token

def require_role(required: list):
    def wrapper(user: dict = Depends(decode_token)):
        role = user.get("role")
        if role not in required:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return user

    return wrapper

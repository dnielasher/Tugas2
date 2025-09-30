# app/deps.py
from fastapi import Header, Depends, HTTPException, status
from app.database import get_session
from app.crud import get_user_by_username
from sqlmodel import Session

def get_db():
    yield from get_session()

def optional_current_user(x_username: str | None = Header(None), x_role: str | None = Header(None), db: Session = Depends(get_db)):
    if not x_username:
        return None
    user = get_user_by_username(db, x_username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User header not found")
    # simple role check
    if user.role.value != x_role:
        # jika header role mismatch -> forbidden
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Role header mismatch")
    return user

def require_admin(current_user = Depends(optional_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin header required")
    if current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin only")
    return current_user

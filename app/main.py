# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from app.database import init_db, get_session
from app import schemas, crud
from app.deps import get_db, optional_current_user, require_admin
from sqlmodel import Session
from typing import List

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # check username/email uniqueness
    if crud.get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already used")
    # optionally check email unique similar
    user = crud.create_user(db, user_in.username, user_in.email, user_in.password, user_in.role)
    return user

@app.get("/users/", response_model=List[schemas.UserRead])
def read_users(db: Session = Depends(get_db), admin = Depends(require_admin)):
    return crud.get_users(db)

@app.get("/users/me", response_model=schemas.UserRead)
def read_own(current_user = Depends(optional_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return current_user

@app.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(optional_current_user)):
    target = crud.get_user(db, user_id)
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # admin can view any
    if current_user and current_user.role.value == "admin":
        return target
    # staff can view only own
    if current_user and current_user.id == user_id:
        return target
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

@app.put("/users/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, update_in: schemas.UserUpdate, db: Session = Depends(get_db), admin = Depends(require_admin)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    updated = crud.update_user(db, user, **update_in.dict(exclude_unset=True))
    return updated

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), admin = Depends(require_admin)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    crud.delete_user(db, user)
    return {}

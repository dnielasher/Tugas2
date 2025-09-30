# app/crud.py
from sqlmodel import Session, select
from app.models import User
from passlib.context import CryptContext
from datetime import datetime

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(plain, hashed) -> bool:
    return pwd_ctx.verify(plain, hashed)

def create_user(db: Session, username: str, email: str, password: str, role):
    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    stmt = select(User).where(User.username == username)
    return db.exec(stmt).first()

def get_user(db: Session, user_id: int):
    return db.get(User, user_id)

def get_users(db: Session, offset: int = 0, limit: int = 100):
    stmt = select(User).offset(offset).limit(limit)
    return db.exec(stmt).all()

def update_user(db: Session, user: User, **kwargs):
    for k, v in kwargs.items():
        if k == "password" and v is not None:
            setattr(user, "hashed_password", hash_password(v))
        elif v is not None and hasattr(user, k):
            setattr(user, k, v)
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()

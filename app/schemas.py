# app/schemas.py
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re
from datetime import datetime
from app.models import Role

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Role

    @validator("username")
    def username_rule(cls, v):
        if not re.match(r'^[a-z0-9]{6,15}$', v):
            raise ValueError("username harus lowercase alfanumerik 6-15 karakter")
        return v

    @validator("password")
    def password_rule(cls, v):
        if not re.match(r'^[A-Za-z0-9!@]{8,20}$', v):
            raise ValueError("password: only letters, numbers, ! and @; panjang 8-20")
        if not re.search(r'[A-Z]', v):
            raise ValueError("password harus mengandung 1 huruf kapital")
        if not re.search(r'[a-z]', v):
            raise ValueError("password harus mengandung 1 huruf kecil")
        if not re.search(r'[0-9]', v):
            raise ValueError("password harus mengandung 1 angka")
        if not re.search(r'[!@]', v):
            raise ValueError("password harus mengandung 1 karakter khusus (! atau @)")
        return v

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Role
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Role] = None

    @validator("password")
    def password_rule_optional(cls, v):
        if v is None:
            return v
        # reuse same checks as create
        if not re.match(r'^[A-Za-z0-9!@]{8,20}$', v):
            raise ValueError("password: only letters, numbers, ! and @; panjang 8-20")
        if not re.search(r'[A-Z]', v):
            raise ValueError("password harus mengandung 1 huruf kapital")
        if not re.search(r'[a-z]', v):
            raise ValueError("password harus mengandung 1 huruf kecil")
        if not re.search(r'[0-9]', v):
            raise ValueError("password harus mengandung 1 angka")
        if not re.search(r'[!@]', v):
            raise ValueError("password harus mengandung 1 karakter khusus (! atau @)")
        return v

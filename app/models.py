# app/models.py
from sqlmodel import SQLModel, Field, Column, String
from typing import Optional
from enum import Enum
from datetime import datetime

class Role(str, Enum):
    admin = "admin"
    staff = "staff"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column(String, unique=True, nullable=False), index=True)
    email: str = Field(sa_column=Column(String, unique=True, nullable=False))
    hashed_password: str = Field(nullable=False)
    role: Role = Field(sa_column=Column(String, nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

from sqlmodel import SQLModel, Field , select ,Session
from apk.database.session import get_session
from fastapi import Depends
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import uuid

class UserRole(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(SQLModel):
    nama: str
    roles: UserRole = UserRole.user 

# Table User
class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    nama: str
    password: str
    roles: UserRole = Field(default=UserRole.user)


# schema Register User
class UserCreate(UserBase):
    nama: str
    password: str
    

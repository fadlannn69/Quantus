from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

class Category(str , Enum):
    EDUCATION = "education"
    ECONOMY = "economy"
    HOBBY = "hobby"
    LIFESTYLE = "lifestyle"
    CULINARY = "culinary"
    TRAVEL = "travel"
    OTHER = "other"

class Status(str,Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class Journal(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    category: Category = Field(default=Category.OTHER)
    status : Status = Field(default=Status.DRAFT)
    content : str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at : datetime | None = None
    cover_image: Optional[str] = Field(default=None, max_length=255)
    view_count: Optional[int] = Field(default=0)
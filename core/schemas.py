from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Users
class UserCreate(BaseModel):
    username: str
    email: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    created_at: datetime

class UserLogin(BaseModel):
    username: str

class UserProgressResponse(BaseModel):
    user_id: int
    term_id: int
    repetitions: int
    starred: bool
    difficulty: float
    last_practiced_at: datetime

# Sets
class SetCreate(BaseModel):
    name: str
    is_public: bool = False
    creator_id: int

class SetUpdate(BaseModel):
    name: Optional[str] = None
    is_public: Optional[bool] = None

class SetResponse(BaseModel):
    set_id: int
    name: str
    creator_id: int
    parent_set_id: Optional[int]
    is_public: bool
    created_at: datetime

# Fork
class SetForkCreate(BaseModel):
    name: str
    is_public: bool = False
    creator_id: int

# User-Set Relationship (user_sets)
class UserSetResponse(BaseModel):
    user_id: int
    set_id: int
    starred: bool
    last_accessed_at: Optional[datetime]
    added_at: datetime

# Terms
class TermUpdate(BaseModel):
    word: Optional[str] = None
    definition: Optional[str] = None

class TermCreate(BaseModel):
    word: str
    definition: str
    order_in_set: Optional[int] = None

class TermResponse(TermCreate):
    term_id: int
    set_id: int
    created_at: datetime

    class Config:
        orm_mode = True
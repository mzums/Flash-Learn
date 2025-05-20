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

# Sets
class SetCreate(BaseModel):
    name: str
    is_public: bool = False

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

# User-Set Relationship (user_sets)
class UserSetResponse(BaseModel):
    user_id: int
    set_id: int
    starred: bool
    last_accessed_at: Optional[datetime]
    added_at: datetime

# Terms
class TermCreate(BaseModel):
    word: str
    definition: str

class TermUpdate(BaseModel):
    word: Optional[str] = None
    definition: Optional[str] = None

class TermResponse(BaseModel):
    term_id: int
    word: str
    definition: str
    set_id: int
    order_in_set: Optional[int]
    created_at: datetime
    
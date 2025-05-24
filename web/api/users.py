# web/api/users.py
from fastapi import APIRouter, Depends, HTTPException
from core.repositories.users import create_user
from core.schemas import UserCreate, UserResponse, UserProgressResponse
from core.repositories.users import create_user, get_user_progress

router = APIRouter(prefix="/users")

@router.post("/", response_model=UserResponse)
def create_user_endpoint(user_data: UserCreate):
    try:
        return create_user(user_data)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    

@router.get("/{user_id}/progress", response_model=UserProgressResponse)
def get_user_progress_endpoint(user_id: int):
    try:
        return get_user_progress(user_id)
    except ValueError as e:
        raise HTTPException(500, detail=str(e))
    except Exception as e:
        raise HTTPException(404, detail="User not found")
from fastapi import APIRouter, Depends, HTTPException
from core.database import get_db
from core import schemas
import psycopg2
import psycopg2.extras

router = APIRouter()

@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user_data: schemas.UserCreate,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO users (username, email)
            VALUES (%s, %s)
            RETURNING user_id, username, email, created_at
            """,
            (user_data.username, user_data.email)
        )
        result = cursor.fetchone()
        return dict(zip([desc[0] for desc in cursor.description], result))
    except psycopg2.IntegrityError as e:
        raise HTTPException(400, "Username/email already exists")
    finally:
        cursor.close()

@router.get("/{user_id}/progress")
def get_user_progress(user_id: int, db: psycopg2.extensions.connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT t.word, utp.repetitions 
        FROM user_term_progress utp
        JOIN terms t ON utp.term_id = t.term_id
        WHERE utp.user_id = %s
    """, (user_id,))
    progress = cursor.fetchall()
    cursor.close()
    return {"user_id": user_id, "progress": progress}

@router.post("/login", response_model=schemas.UserResponse)
def login(
    user_data: schemas.UserLogin,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute(
            "SELECT user_id, username, email, created_at FROM users WHERE username = %s",
            (user_data.username,)
        )
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(404, "User not found")
            
        columns = [desc[0] for desc in cursor.description]
        user_dict = dict(zip(columns, user))
        
        return dict(user)
        
    except psycopg2.Error as e:
        raise HTTPException(500, "Database error")
    finally:
        cursor.close()
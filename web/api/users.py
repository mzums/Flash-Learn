from fastapi import APIRouter, Depends, HTTPException
from core.database import get_db
from core import schemas
import psycopg2
import psycopg2.extras

router = APIRouter()

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate):
    with get_db() as db:
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (username, email)
                VALUES (%s, %s)
                RETURNING user_id, username, email, created_at
                """,
                (user.username, user.email)
            )
            result = cursor.fetchone()
            db.commit()
            
            return {
                "user_id": result[0],
                "username": result[1],
                "email": result[2],
                "created_at": result[3]
            }
        except psycopg2.IntegrityError as e:
            db.rollback()
            raise HTTPException(400, "Username/email already exists")
        except Exception as e:
            db.rollback()
            raise HTTPException(500, f"Database error: {str(e)}")
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
def login(user_data: schemas.UserLogin):
    with get_db() as db:
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute(
                "SELECT user_id, username, email, created_at FROM users WHERE username = %s",
                (user_data.username,)
            )
            user = cursor.fetchone()
            
            if not user:
                raise HTTPException(404, detail="User not found")
                
            return dict(user)
            
        except psycopg2.Error as e:
            print(f"Database error: {str(e)}")
            raise HTTPException(500, "Internal server error")
        finally:
            cursor.close()
# core/repositories/users.py
from core.database import get_db
from core.schemas import UserCreate, UserResponse, UserProgressResponse
import psycopg2

def create_user(user_data: UserCreate) -> UserResponse:
    with get_db() as db:
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING user_id",
                (user_data.username, user_data.email))
            user_id = cursor.fetchone()[0]
            db.commit()
            return {"user_id": user_id, **user_data.dict()}
        except psycopg2.IntegrityError as e:
            raise ValueError("Username/email already exists")
        finally:
            cursor.close()


def get_user_progress(user_id: int) -> UserProgressResponse:
    with get_db() as db:
        cursor = db.cursor()
        try:
            cursor.execute("""
                SELECT t.word, utp.repetitions 
                FROM user_term_progress utp
                JOIN terms t ON utp.term_id = t.term_id
                WHERE utp.user_id = %s
            """, (user_id,))
            progress = cursor.fetchall()
            return {"user_id": user_id, "progress": progress}
        except psycopg2.Error as e:
            raise ValueError("Database error") from e
        finally:
            cursor.close()

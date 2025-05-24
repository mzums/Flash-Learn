from fastapi import FastAPI, Depends, HTTPException
from core.database import get_db
import psycopg2
from core import schemas

app = FastAPI()


@app.get("/sets", response_model=list[schemas.SetResponse])
def get_public_sets(db: psycopg2.extensions.connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sets WHERE is_public = TRUE")
    sets = cursor.fetchall()
    cursor.close()
    return [{"set_id": s[0], "name": s[3], "creator_id": s[1]} for s in sets]


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate):
    with get_db() as db:
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING user_id, username, email, created_at",
                (user.username, user.email)
            )
            result = cursor.fetchone()
            return {
                "user_id": result[0],
                "username": result[1],
                "email": result[2],
                "created_at": result[3]
            }
        except psycopg2.IntegrityError as e:
            raise HTTPException(400, "Username/email already exists")
        finally:
            cursor.close()


@app.get("/users/{user_id}/progress")
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


@app.post("/login")
def login(user_data: schemas.UserLogin):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (user_data.username,))
        user = cursor.fetchone()
        cursor.close()

    if not user:
        raise HTTPException(404, "User not found")
    
    return {"message": "Logged in"}


@app.post("/create_set")
def create_set(name: schemas.SetCreate, is_public: schemas.SetCreate):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO sets (name, is_public) VALUES(%s, %s) RETURNING set_id, name, creator_id, parent_set_id")
        set = cursor.fetchone()
        cursor.close()

    if not set:
        raise HTTPException(404, "Set not found")
    
    return {"message": "Set created"}


"""
from fastapi import FastAPI
from core.database import get_db
from web.api import users, sets

app = FastAPI()

app.include_router(users.router, prefix="/api/v1/users")
app.include_router(sets.router, prefix="/api/v1/sets")
"""

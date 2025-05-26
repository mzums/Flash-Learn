from fastapi import APIRouter, Depends, HTTPException, Request, Path, Body, Header
from core.database import get_db
from core import schemas
from core.schemas import TermCreate, TermResponse
from core.repositories.terms import create_term
import psycopg2
import psycopg2.extras

router = APIRouter()

@router.get("/", response_model=list[schemas.SetResponse])
def get_public_sets(db: psycopg2.extensions.connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM sets WHERE is_public = TRUE")
    sets = cursor.fetchall()
    cursor.close()
    return [{"set_id": s[0], "name": s[3], "creator_id": s[1]} for s in sets]


@router.post("/", response_model=schemas.SetResponse)
def create_set(
    set_data: schemas.SetCreate,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO sets (name, is_public, creator_id)
            VALUES (%s, %s, %s)
            RETURNING set_id, name, creator_id, parent_set_id, is_public, created_at
            """,
            (set_data.name, set_data.is_public, set_data.creator_id)
        )
        result = cursor.fetchone()
        
        return {
            "set_id": result[0],
            "name": result[1],
            "creator_id": result[2],
            "parent_set_id": result[3],
            "is_public": result[4],
            "created_at": result[5]
        }
        
    except psycopg2.IntegrityError as e:
        raise HTTPException(400, "Set name already exists")
    finally:
        cursor.close()


@router.post("/{parent_set_id}/fork", response_model=schemas.SetResponse)
def fork_set_endpoint(
    parent_set_id: int,
    fork_data: schemas.SetForkCreate,
    db: psycopg2.extensions.connection = Depends(get_db)
):
    try:
        from core.repositories.sets import fork_set
        new_set = fork_set(
            db=db,
            user_id=fork_data.creator_id,
            parent_set_id=parent_set_id,
            name=fork_data.name,
            is_public=fork_data.is_public
        )
        return new_set
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=str(e))


@router.post("/{set_id}/terms", response_model=schemas.TermResponse)
def add_term(
    set_id: int,
    term_data: schemas.TermCreate,
    x_user_id: int = Header(..., alias="X-User-ID"),
    db: psycopg2.extensions.connection = Depends(get_db)
):
    cursor = None
    try:
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cursor.execute("SELECT creator_id FROM sets WHERE set_id = %s", (set_id,))
        result = cursor.fetchone()
        if not result or result["creator_id"] != x_user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        from core.repositories.terms import create_term
        term = create_term(db, set_id, term_data)
        db.commit()
        return term
        
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except psycopg2.Error as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        if cursor:
            cursor.close()

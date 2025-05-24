# core/repositories/sets.py
from core.database import get_db
from core.schemas import SetResponse, SetCreate
import psycopg2


def fork_set(parent_set_id: int, name: str, is_public: bool) -> SetResponse:
    with get_db() as db:
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM sets WHERE set_id = %s", (parent_set_id,))
        original_set = cursor.fetchone()
        
        cursor.execute("""
            INSERT INTO sets (name, creator_id, parent_set_id, is_public)
            VALUES (%s, %s, %s, %s)
            RETURNING set_id, name, creator_id, parent_set_id, is_public, created_at
        """, (name, original_set["creator_id"], parent_set_id, is_public))
        
        new_set = cursor.fetchone()
        db.commit()
        
        return new_set
    

def create_set(creator_id: int, set_data: SetCreate) -> SetResponse:
    with get_db() as db:
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO sets (name, is_public, creator_id)
                VALUES (%s, %s, %s)
                RETURNING set_id, name, is_public, creator_id, created_at
                """,
                (set_data.name, set_data.is_public, creator_id)
            )
            result = cursor.fetchone()
            db.commit()
            
            return {
                "set_id": result[0],
                "name": result[1],
                "is_public": result[2],
                "creator_id": result[3],
                "created_at": result[4]
            }
        except psycopg2.IntegrityError as e:
            raise ValueError("Set name must be unique")
        finally:
            cursor.close()
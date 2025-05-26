from core.schemas import TermCreate, TermResponse
import psycopg2
import psycopg2.extras

def create_term(db, set_id: int, term_data: TermCreate) -> TermResponse:
    cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cursor.execute("SELECT 1 FROM sets WHERE set_id = %s", (set_id,))
        if not cursor.fetchone():
            raise ValueError(f"Set ID {set_id} not found")

        cursor.execute(
            """
            INSERT INTO terms (set_id, word, definition, order_in_set)
            VALUES (
                %s,
                %s,
                %s,
                COALESCE(%s, (SELECT COUNT(*) FROM terms WHERE set_id = %s) + 1)
            )
            RETURNING term_id, set_id, word, definition, order_in_set, created_at
            """,
            (
                set_id,
                term_data.word,
                term_data.definition,
                term_data.order_in_set,
                set_id
            )
        )
        
        term = dict(cursor.fetchone())
        return term
        
    except psycopg2.IntegrityError as e:
        db.rollback()
        raise ValueError(f"Integrity error: {str(e)}")
    except psycopg2.Error as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")
    finally:
        cursor.close()
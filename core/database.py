import psycopg2
from psycopg2 import pool
from contextlib import contextmanager

DB_CONFIG = {
    "host": "localhost",
    "database": "flashlearn",
    "user": "postgres",
    "password": ""
}

connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)


@contextmanager
def get_db():
    conn = connection_pool.getconn()
    try:
        yield conn  # 👈 Zwracamy BEZPOŚREDNIO połączenie
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection_pool.putconn(conn)
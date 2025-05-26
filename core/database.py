import psycopg2
from psycopg2 import pool
from fastapi import Depends
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

def get_db():
    conn = connection_pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connection_pool.putconn(conn)
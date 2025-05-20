import psycopg2
from psycopg2 import pool

DB_CONFIG = {
    "dbname": "flashlearn",
    "user": "postgres",
    "password": "",
    "host": "localhost"
}

connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **DB_CONFIG)

def get_db():
    conn = connection_pool.getconn()
    try:
        yield conn
    finally:
        connection_pool.putconn(conn)
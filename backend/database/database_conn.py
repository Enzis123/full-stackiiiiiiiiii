import os
import sqlite3


db = "db.db"


def get_db():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = sqlite3.connect(db)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS servicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servicio TEXT NOT NULL,
            descripcion TEXT,
            precio REAL,
            categoria TEXT
        )
    """)
    conn.commit()
    conn.close()

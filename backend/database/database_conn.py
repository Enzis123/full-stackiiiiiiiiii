import sqlite3

db = "database/db.db"


def get_db():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    yield conn
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

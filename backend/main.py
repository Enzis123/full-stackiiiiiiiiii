from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import database.database_conn as db_conn
from models.modelServicios import modelServicios
import managers.manager as manager
import sqlite3

app = FastAPI()
db_conn.init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ver_servicios")
def listar_servicios(db: sqlite3.Connection = Depends(db_conn.get_db)):
    return manager.listar(db)


@app.post("/agregar_servicios")
def agregar_servicio(s: modelServicios, db: sqlite3.Connection = Depends(db_conn.get_db)):
    return manager.crear(db, s)


@app.put("/editar_servicio/{id}")
def editar_servicio(id: int, s: modelServicios, db: sqlite3.Connection = Depends(db_conn.get_db)):
    return manager.editar(db, id, s)


@app.delete("/borrar_servicio/{id}")
def borrar_servicio(id: int, db: sqlite3.Connection = Depends(db_conn.get_db)):
    return manager.borrar(db, id)
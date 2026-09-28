from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import database.database_conn as db_conn
from models.modelServicios import modelServicios
import managers.manager as manager

app = FastAPI()
db_conn.init_db()

origenes_permitidos = [
    "https://greenscapesproyect.netlify.app",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "null",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)


@app.get("/ver_servicios")
def listar_servicios(db=Depends(db_conn.get_db)):
    return manager.listar(db)


@app.post("/agregar_servicios")
def agregar_servicio(s: modelServicios, db=Depends(db_conn.get_db)):
    return manager.crear(db, s)


@app.get("/ver_servicio/{id}")
def buscar_servicio(id: int, db=Depends(db_conn.get_db)):
    return manager.buscar(db, id)


@app.put("/editar_servicio/{id}")
def editar_servicio(id: int, s: modelServicios, db=Depends(db_conn.get_db)):
    return manager.editar(db, id, s)


@app.delete("/borrar_servicio/{id}")
def borrar_servicio(id: int, db=Depends(db_conn.get_db)):
    return manager.borrar(db, id)

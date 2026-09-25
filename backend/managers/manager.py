from fastapi import HTTPException
from models.modelServicios import modelServicios


def listar(db):
    filas = db.execute("SELECT * FROM servicios").fetchall()
    return [dict(f) for f in filas]


def crear(db, s: modelServicios):
    cursor = db.execute(
        "INSERT INTO servicios (servicio, descripcion, precio, categoria) VALUES (?, ?, ?, ?)",
        (s.servicio, s.descripcion, s.precio, s.categoria)
    )
    db.commit()
    return {"ok": True, "id": cursor.lastrowid}


def editar(db, id, s: modelServicios):
    cursor = db.execute(
        "UPDATE servicios SET servicio = ?, descripcion = ?, precio = ?, categoria = ? WHERE id = ?",
        (s.servicio, s.descripcion, s.precio, s.categoria, id)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db.commit()
    return {"ok": True}


def borrar(db, id):
    cursor = db.execute("DELETE FROM servicios WHERE id = ?", (id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db.commit()
    return {"ok": True}

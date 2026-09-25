from fastapi import HTTPException


def listar(db):
    filas = db.execute("SELECT * FROM servicios").fetchall()
    lista = []
    for fila in filas:
        lista.append(dict(fila))
    return lista


def crear(db, s):
    cursor = db.execute(
        "INSERT INTO servicios (servicio, descripcion, precio, categoria) VALUES (?, ?, ?, ?)",
        (s.servicio, s.descripcion, s.precio, s.categoria)
    )
    db.commit()
    return {"mensaje": "Servicio agregado", "id": cursor.lastrowid}


def editar(db, id, s):
    cursor = db.execute(
        "UPDATE servicios SET servicio = ?, descripcion = ?, precio = ?, categoria = ? WHERE id = ?",
        (s.servicio, s.descripcion, s.precio, s.categoria, id)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db.commit()
    return {"mensaje": "Servicio editado"}


def borrar(db, id):
    cursor = db.execute("DELETE FROM servicios WHERE id = ?", (id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db.commit()
    return {"mensaje": "Servicio borrado"}

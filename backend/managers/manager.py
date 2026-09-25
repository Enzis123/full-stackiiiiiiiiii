from models.modelServicios import modelServicios


def listar(db):
    filas = db.execute("SELECT * FROM servicios").fetchall()
    return [dict(f) for f in filas]


def crear(db, s: modelServicios):
    db.execute(
        "INSERT INTO servicios (servicio, descripcion, precio, categoria) VALUES (?, ?, ?, ?)",
        (s.servicio, s.descripcion, s.precio, s.categoria)
    )
    db.commit()
    return {"ok": True}


def editar(db, id, s: modelServicios):
    db.execute(
        "UPDATE servicios SET servicio = ?, descripcion = ?, precio = ?, categoria = ? WHERE id = ?",
        (s.servicio, s.descripcion, s.precio, s.categoria, id)
    )
    db.commit()
    return {"ok": True}


def borrar(db, id):
    db.execute("DELETE FROM servicios WHERE id = ?", (id,))
    db.commit()
    return {"ok": True}
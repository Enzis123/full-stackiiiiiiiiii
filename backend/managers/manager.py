def listar(db):
    filas = db.execute("SELECT * FROM servicios").fetchall()
    lista = []
    for fila in filas:
        lista.append(dict(fila))
    return lista


def crear(db, s):
    db.execute(
        "INSERT INTO servicios (servicio, descripcion, precio, categoria) VALUES (?, ?, ?, ?)",
        (s.servicio, s.descripcion, s.precio, s.categoria)
    )
    db.commit()
    return {"mensaje": "Servicio agregado"}


def buscar(db, id):
    fila = db.execute("SELECT * FROM servicios WHERE id = ?", (id,)).fetchone()
    if fila == None:
        return {"mensaje": "No existe un servicio con ese id"}
    return dict(fila)


def editar(db, id, s):
    db.execute(
        "UPDATE servicios SET servicio = ?, descripcion = ?, precio = ?, categoria = ? WHERE id = ?",
        (s.servicio, s.descripcion, s.precio, s.categoria, id)
    )
    db.commit()
    return {"mensaje": "Servicio editado"}


def borrar(db, id):
    db.execute("DELETE FROM servicios WHERE id = ?", (id,))
    db.commit()
    return {"mensaje": "Servicio borrado"}

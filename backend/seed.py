import sqlite3
import database.database_conn as db_conn

# Catálogo inicial: (servicio, descripcion, precio, categoria)
SERVICIOS = [
    # Parque
    ("Corte de pasto chico", "Corte de pasto hasta 100m2, incluye bordeado y retiro de restos", 60000, "Parque"),
    ("Corte de pasto mediano", "Corte de pasto de 100m2 a 300m2, incluye bordeado y retiro de restos", 110000, "Parque"),
    ("Corte de pasto grande", "Corte de pasto de 300m2 a 1000m2, incluye bordeado y retiro de restos", 200000, "Parque"),
    ("Poda de árboles", "Poda de formación o limpieza de árboles de hasta 6 metros, por unidad", 80000, "Parque"),
    ("Poda de cercos y arbustos", "Recorte y emprolijado de cercos vivos y arbustos, por metro lineal", 5000, "Parque"),
    ("Desmalezado de terreno", "Limpieza de malezas y yuyos en terrenos o lotes baldíos, por cada 100m2", 70000, "Parque"),
    ("Colocación de césped en panes", "Nivelado del suelo y colocación de panes de césped, por m2", 9000, "Parque"),
    ("Fertilización de césped", "Aplicación de fertilizante para césped, por cada 100m2", 35000, "Parque"),
    ("Control de plagas en jardín", "Fumigación contra hormigas, pulgones y otras plagas del jardín", 50000, "Parque"),
    ("Retiro de ramas y residuos verdes", "Carga y retiro de ramas, hojas y restos de poda, por viaje", 45000, "Parque"),

    # Pileta
    ("Limpieza de pileta", "Barrido de fondo, limpieza de paredes y línea de flote, aspirado y control de cloro", 55000, "Pileta"),
    ("Mantenimiento mensual de pileta", "4 visitas al mes con limpieza y control de químicos (químicos no incluidos)", 180000, "Pileta"),
    ("Recuperación de agua verde", "Tratamiento de shock para recuperar el agua de la pileta, incluye químicos", 120000, "Pileta"),
    ("Vaciado y lavado de pileta", "Vaciado completo, hidrolavado de paredes y fondo, y llenado", 250000, "Pileta"),
    ("Puesta a punto de temporada", "Limpieza profunda, revisión de filtro y bomba, y ajuste de químicos para arrancar la temporada", 150000, "Pileta"),
    ("Cambio de arena del filtro", "Reemplazo de la arena del filtro de la pileta (arena incluida)", 90000, "Pileta"),
    ("Cobertor de invierno", "Colocación o retiro del cobertor de invierno de la pileta", 40000, "Pileta"),

    # Mantenimiento general
    ("Limpieza de canaletas", "Limpieza de canaletas y bajadas pluviales", 50000, "Mantenimiento"),
    ("Hidrolavado de patios y veredas", "Hidrolavado de pisos exteriores, patios y veredas, por cada 50m2", 60000, "Mantenimiento"),
    ("Pintura de rejas y portones", "Lijado y pintura de rejas, portones o cercos metálicos, por metro lineal", 12000, "Mantenimiento"),
    ("Tratamiento de deck de madera", "Lijado y aplicación de protector o barniz en decks, por m2", 15000, "Mantenimiento"),
    ("Reparación de sistema de riego", "Revisión y reparación de aspersores, mangueras y programador de riego", 70000, "Mantenimiento"),
    ("Instalación de riego automático", "Instalación de sistema de riego automático, por cada 100m2", 450000, "Mantenimiento"),
    ("Instalación de luces de jardín", "Instalación de luminarias exteriores, por unidad (luminaria no incluida)", 25000, "Mantenimiento"),
    ("Mantenimiento general mensual", "Visita quincenal con corte de pasto, limpieza de pileta y revisión general del parque", 300000, "Mantenimiento"),
]


def cargar():
    db_conn.init_db()
    conn = sqlite3.connect(db_conn.DB_PATH)
    existentes = {fila[0].lower() for fila in conn.execute("SELECT servicio FROM servicios")}

    agregados = 0
    for servicio, descripcion, precio, categoria in SERVICIOS:
        if servicio.lower() in existentes:
            continue
        conn.execute(
            "INSERT INTO servicios (servicio, descripcion, precio, categoria) VALUES (?, ?, ?, ?)",
            (servicio, descripcion, precio, categoria)
        )
        agregados += 1

    conn.commit()
    conn.close()
    print(f"Se agregaron {agregados} servicios ({len(SERVICIOS) - agregados} ya existían).")


if __name__ == "__main__":
    cargar()

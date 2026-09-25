import pydantic


class modelServicios(pydantic.BaseModel):
    id: int | None = None
    servicio: str
    descripcion: str
    precio: float
    categoria: str
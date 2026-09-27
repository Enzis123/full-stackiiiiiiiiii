import pydantic


class modelServicios(pydantic.BaseModel):
    servicio: str
    descripcion: str
    precio: float
    categoria: str

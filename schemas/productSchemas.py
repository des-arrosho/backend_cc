from pydantic import BaseModel, HttpUrl
from enum import Enum

class CategoriaProducto(str, Enum):
    alimentos = "Alimentos"
    ropa = "Ropa"
    tecnologia = "Tecnologia"
    limpieza = "Limpieza"
    hogar = "Hogar"
    salud = "Salud"
    papeleria = "Papeleria"
    otro = "Otro"

class StatusProducto(str, Enum):
    disponible = "disponible"
    agotado = "agotado"

class ProductBase(BaseModel):
    name: str
    category: CategoriaProducto
    carbon_footprint: float
    recyclable_packaging: bool
    local_origin: bool
    price: float
    quantity: int = 1
    status: StatusProducto = StatusProducto.disponible

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    image_url: HttpUrl | None = None

    class Config:
        from_attributes = True

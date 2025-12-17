from pydantic import BaseModel, HttpUrl

class CartBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartCreate(CartBase):
    pass

# Este schema es para la respuesta del carrito con datos de producto
class CartItemResponse(BaseModel):
    product_id: int
    name: str
    price: float
    image_url: HttpUrl | None
    quantity: int

    class Config:
        orm_mode = True

from pydantic import BaseModel

class BuyRequest(BaseModel):
    product_id: int
    quantity: int
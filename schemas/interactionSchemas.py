from pydantic import BaseModel
from datetime import datetime

class InteractionCreate(BaseModel):
    product_id: int


class InteractionOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    interaction: int
    created_at: datetime  # incluir timestamp

    class Config:
        from_attributes = True


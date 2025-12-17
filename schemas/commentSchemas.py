from pydantic import BaseModel
from datetime import datetime

class UserSimple(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    product_id: int
    content: str

class CommentOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    content: str
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True

class CommentWithUser(BaseModel):
    id: int
    user_id: int
    product_id: int
    content: str
    created_at: datetime
    updated_at: datetime | None = None
    user: UserSimple  # ahora Pydantic serializa automáticamente

    class Config:
        from_attributes = True

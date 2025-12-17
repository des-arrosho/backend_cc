from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    status: str

class UserCreate(UserBase):
    password: str
    profile_picture: Optional[str] = None  # Campo opcional al crear usuario

class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    status: str
    registration_date: datetime
    profile_picture: Optional[str]= None  # Campo obligatorio en respuesta

    class Config:
        from_attributes = True  # Para trabajar con ORM

class UserLogin(BaseModel):
    username: str
    password: str

class UserSimple(BaseModel):
    id: int
    username: str
    status: str

    class Config:
        from_attributes = True

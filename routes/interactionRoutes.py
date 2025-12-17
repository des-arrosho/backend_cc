from fastapi import APIRouter, HTTPException, Depends
from schemas.interactionSchemas import InteractionCreate, InteractionOut
from controller.interactionController import crear_interaccion, obtener_interacciones_por_usuario
from typing import List
from schemas.userSchemas import User
from config.jwt import get_current_user
from sqlalchemy.orm import Session
from config.db import get_db

interaction = APIRouter()

@interaction.post("/interacciones", response_model=InteractionOut, tags=["Interacciones"])
def registrar_interaccion(
    interaccion: InteractionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crear_interaccion(db=db, interaccion=interaccion, user_id=current_user.id)


@interaction.get("/interacciones", response_model=List[InteractionOut], tags=["Interacciones"])
def listar_mis_interacciones(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return obtener_interacciones_por_usuario(user_id=current_user.id, db=db)

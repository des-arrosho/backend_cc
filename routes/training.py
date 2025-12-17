from fastapi import APIRouter, Depends
from config.db import get_db
from config.jwt import get_current_user
from sqlalchemy.orm import Session
from schemas.userSchemas import User
from services.training import entrenar_recomendaciones

training_router = APIRouter(prefix="/modelo", tags=["Modelo"])

# Ruta GET protegida con JWT
@training_router.get("/entrenar")
def entrenar_modelo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    recomendaciones = entrenar_recomendaciones(db, current_user.id)
    return {"recomendaciones": recomendaciones}

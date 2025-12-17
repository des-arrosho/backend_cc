from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from config.db import get_db
from models.interactionModel import Interaccion
from typing import List

# Crear nueva interacción
from sqlalchemy.orm import Session
from models.interactionModel import Interaccion
from schemas.interactionSchemas import InteractionCreate, InteractionOut


from sqlalchemy.orm import Session
from models.interactionModel import Interaccion

def crear_interaccion(db: Session, interaccion: InteractionCreate, user_id: int):
    # Contar interacciones previas para este usuario y producto
    count = db.query(Interaccion).filter(
        Interaccion.user_id == user_id,
        Interaccion.product_id == interaccion.product_id
    ).count()

    nueva = Interaccion(
        user_id=user_id,
        product_id=interaccion.product_id,
        interaction=count + 1  # Siguiente interacción automática
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# Obtener interacciones por usuario
def obtener_interacciones_por_usuario(user_id: int, db: Session = Depends(get_db)) -> List[Interaccion]:
    interacciones = db.query(Interaccion).filter(Interaccion.user_id == user_id).all()
    if not interacciones:
        raise HTTPException(status_code=404, detail="No se encontraron interacciones para este usuario.")
    return interacciones

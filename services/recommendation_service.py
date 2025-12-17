from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from services.training import entrenar_recomendaciones
from config.db import get_db
import asyncio
import json

def get_best_recommendation(db: Session, user_id: int):
    resultados = entrenar_recomendaciones(db, user_id)

    # Si tu entrenar_recomendaciones devuelve un dict con varias claves
    # (ej: silhouette_score, clusters, recomendaciones), usamos solo "recomendaciones"
    if isinstance(resultados, dict) and "recomendaciones" in resultados:
        recomendaciones = resultados["recomendaciones"]
    else:
        recomendaciones = resultados  # lista simple como antes

    if recomendaciones and len(recomendaciones) > 0:
        return recomendaciones[0]  # el mejor producto (primero de la lista)
    return None


async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            # Obtener la mejor recomendación (la primera)
            recomendacion = get_best_recommendation(db, user_id)
            if recomendacion:
                mensaje = {
                    "type": "recommendation",
                    "data": recomendacion
                }
                await websocket.send_text(json.dumps(mensaje))
            else:
                await websocket.send_text(json.dumps({"type": "info", "data": "No recommendations available"}))

            await asyncio.sleep(10)  # Esperar 10 segundos antes de la siguiente notificación
    except WebSocketDisconnect:
        print(f"Cliente desconectado: user_id={user_id}")

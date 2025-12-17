from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from services.recommendation_service import get_best_recommendation
from config.db import get_db
import asyncio
import json

async def websocket_endpoint(websocket: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            recomendacion = get_best_recommendation(db, user_id)
            if recomendacion:
                mensaje = {
                    "type": "recommendation",
                    "data": recomendacion,
                    "message": f"✨ Nuevo: {recomendacion['name']} ({recomendacion['category']}) ¡Recomendado para ti!"
                }
                await websocket.send_text(json.dumps(mensaje))
            else:
                await websocket.send_text(json.dumps({
                    "type": "info",
                    "message": "No hay recomendaciones disponibles"
                }))
            await asyncio.sleep(10)
    except WebSocketDisconnect:
        print(f"Cliente desconectado: user_id={user_id}")

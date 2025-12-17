# routes/notification_routes.py
from fastapi import APIRouter, Depends, Query, WebSocket
from sqlalchemy.orm import Session
from controller.notificationController import websocket_endpoint
from config.db import get_db

notification_routes = APIRouter()

@notification_routes.websocket("/ws/notifications")
async def notifications_ws(websocket: WebSocket, user_id: int = Query(...), db: Session = Depends(get_db)):
    await websocket_endpoint(websocket, user_id, db)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_db
from controller.mls_controller import get_ml_dashboard_data

ml_super = APIRouter()

@ml_super.get("/ml/dashboard")
def ml_dashboard(db: Session = Depends(get_db)):
    data = get_ml_dashboard_data(db)
    return data

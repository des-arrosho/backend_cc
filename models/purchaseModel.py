from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base

class Purchase(Base):
    __tablename__ = "tbd_purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbb_users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("tbb_products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    user = relationship("User", back_populates="purchases")
    product = relationship("Product", back_populates="purchases")


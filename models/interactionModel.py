from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from config.db import Base

class Interaccion(Base):
    __tablename__ = "tbd_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbb_users.id"))
    product_id = Column(Integer, ForeignKey("tbb_products.id"))
    interaction = Column(Integer)  # 1: vista, 2: clic, 3: favorito, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # timestamp automático

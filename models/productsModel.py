from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, ForeignKey
from config.db import Base
from schemas.productSchemas import CategoriaProducto, StatusProducto
from sqlalchemy.orm import relationship
import enum

class Product(Base):
    __tablename__ = "tbb_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    category = Column(String(100))
    carbon_footprint = Column(Float)
    recyclable_packaging = Column(Boolean)
    local_origin = Column(Boolean)
    image_url = Column(String(500))
    price = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), default=StatusProducto.disponible.value)
    quantity = Column(Integer, nullable=False, default=1)

    created_by = Column(Integer, ForeignKey("tbb_users.id"))  
    creator = relationship("User", back_populates="products")
    purchases = relationship("Purchase", back_populates="product")



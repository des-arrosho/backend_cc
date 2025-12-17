from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from config.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "tbb_users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="Unique user ID")
    username = Column(String(60), nullable=False, comment="Username")
    email = Column(String(100), nullable=False, comment="User email")
    profile_picture = Column(String(255), nullable=True, comment="Profile image URL")
    password = Column(String(128), nullable=False, comment="Hashed password")
    status = Column(Enum("Active", "Inactive"), nullable=False, comment="Current user status")
    registration_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    update_date = Column(DateTime, nullable=True)

    products = relationship("Product", back_populates="creator")
    purchases = relationship("Purchase", back_populates="user")
    carts = relationship("Cart", back_populates="user")
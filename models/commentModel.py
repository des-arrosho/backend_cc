from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from config.db import Base
from sqlalchemy.orm import relationship

class Comment(Base):
    __tablename__ = "tbd_comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("tbb_users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("tbb_products.id"), nullable=False)
    content = Column(Text, nullable=False)  # Texto del comentario
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # Opcional: si quieres un campo para moderación o estado del comentario
    # status = Column(Enum("Pending", "Approved", "Rejected"), default="Pending")
    user = relationship("User", lazy="joined")

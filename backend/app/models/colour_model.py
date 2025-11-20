"""
Lookup Tables - Colour Model
顏色查找表
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Colour(Base):
    __tablename__ = "colours"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(50), unique=True, nullable=False, comment="Black, White, Blue, etc."
    )
    display_name = Column(String(50), nullable=False, comment="顯示名稱（中文）")
    hex_code = Column(String(7), comment="HEX 顏色碼 (#000000)")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    products = relationship("Product", back_populates="base_colour")

    def __repr__(self):
        return f"<Colour(id={self.id}, name='{self.name}', display_name='{self.display_name}')>"

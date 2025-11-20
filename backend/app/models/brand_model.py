"""
Lookup Tables - Brand Model
品牌資料表
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, comment="品牌名稱")
    display_name = Column(String(200), comment="品牌顯示名稱（中文/英文）")
    description = Column(Text, comment="品牌簡介")
    logo_url = Column(String(1000), comment="品牌 Logo URL")
    is_active = Column(Boolean, default=True, comment="是否啟用")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    products = relationship("Product", back_populates="brand")

    def __repr__(self):
        return f"<Brand(id={self.id}, name='{self.name}', is_active={self.is_active})>"

"""
Lookup Tables - Master Category Model
主分類表
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class MasterCategory(Base):
    __tablename__ = "master_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(100),
        unique=True,
        nullable=False,
        comment="Apparel, Accessories, Footwear, etc.",
    )
    display_name = Column(String(100), nullable=False, comment="顯示名稱（中文）")
    description = Column(Text, comment="分類說明")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    products = relationship("Product", back_populates="master_category")
    sub_categories = relationship("SubCategory", back_populates="master_category")

    def __repr__(self):
        return f"<MasterCategory(id={self.id}, name='{self.name}', display_name='{self.display_name}')>"

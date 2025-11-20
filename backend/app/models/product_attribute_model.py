"""
Extended Table - Product Attribute Model
商品屬性資料表
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ProductAttribute(Base):
    __tablename__ = "product_attributes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id"), nullable=False, comment="所屬商品"
    )
    attribute_key = Column(
        String(100), nullable=False, comment="屬性鍵（Pattern, Fit Type, etc.）"
    )
    attribute_value = Column(Text, nullable=False, comment="屬性值")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="attributes")

    # Indexes
    __table_args__ = (Index("idx_product_attr", "product_id", "attribute_key"),)

    def __repr__(self):
        return f"<ProductAttribute(id={self.id}, product_id={self.product_id}, key='{self.attribute_key}')>"

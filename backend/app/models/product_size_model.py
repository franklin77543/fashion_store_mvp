"""
Extended Table - Product Size Model
商品尺寸與庫存資料表
"""

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ProductSize(Base):
    __tablename__ = "product_sizes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id"), nullable=False, comment="所屬商品"
    )
    size_name = Column(String(50), nullable=False, comment="S, M, L, XL, 2YRS, etc.")
    stock_count = Column(Integer, default=0, comment="該尺寸庫存")
    is_available = Column(Boolean, default=True, comment="是否可購買")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="sizes")

    # Indexes
    __table_args__ = (
        Index("idx_product_size_unique", "product_id", "size_name", unique=True),
    )

    def __repr__(self):
        return f"<ProductSize(id={self.id}, product_id={self.product_id}, size='{self.size_name}', stock={self.stock_count})>"

"""
Extended Table - Product Image Model
商品多圖片資料表
"""

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id"), nullable=False, comment="所屬商品"
    )
    image_type = Column(
        String(50), nullable=False, comment="default, front, back, search, etc."
    )
    image_url = Column(String(1000), nullable=False, comment="圖片 URL")
    resolution = Column(String(20), comment="解析度 (1080X1440, 360X480, etc.)")
    is_primary = Column(Boolean, default=False, comment="是否為主圖")
    display_order = Column(Integer, default=0, comment="顯示順序")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    product = relationship("Product", back_populates="images")

    # Indexes
    __table_args__ = (
        Index("idx_product_image_type", "product_id", "image_type"),
        Index("idx_product_primary_image", "product_id", "is_primary"),
    )

    def __repr__(self):
        return f"<ProductImage(id={self.id}, product_id={self.product_id}, type='{self.image_type}')>"

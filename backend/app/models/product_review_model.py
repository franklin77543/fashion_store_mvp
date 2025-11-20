"""
Review System - Product Review Model (Phase 2)
商品評論資料表
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    Index,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ProductReview(Base):
    __tablename__ = "product_reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer, ForeignKey("products.id"), nullable=False, comment="所屬商品"
    )

    # 評論者資訊
    reviewer_name = Column(String(200), nullable=False, comment="評論者姓名")
    reviewer_email = Column(String(200), comment="評論者 Email")

    # 評論內容
    rating = Column(Integer, nullable=False, comment="評分 (1-5)")
    title = Column(String(200), comment="評論標題")
    content = Column(Text, nullable=False, comment="評論內容")

    # 審核狀態
    is_verified = Column(Boolean, default=False, comment="是否驗證購買")
    is_approved = Column(Boolean, default=False, comment="是否通過審核")

    # 互動統計
    helpful_count = Column(Integer, default=0, comment="有幫助票數")

    # 時間戳記
    created_at = Column(TIMESTAMP, server_default=func.now())
    approved_at = Column(TIMESTAMP, comment="審核通過時間")

    # Relationships
    product = relationship("Product", back_populates="reviews")

    # Indexes
    __table_args__ = (
        Index("idx_review_product", "product_id"),
        Index("idx_review_approved", "product_id", "is_approved"),
        Index("idx_review_rating", "rating"),
    )

    def __repr__(self):
        return f"<ProductReview(id={self.id}, product_id={self.product_id}, rating={self.rating}, approved={self.is_approved})>"

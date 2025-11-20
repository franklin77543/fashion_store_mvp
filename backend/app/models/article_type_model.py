"""
Lookup Tables - Article Type Model
商品類型查找表（最細分類）
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ArticleType(Base):
    __tablename__ = "article_types"

    id = Column(Integer, primary_key=True, index=True)
    sub_category_id = Column(
        Integer,
        ForeignKey("sub_categories.id"),
        nullable=True,
        comment="所屬子分類（可為空）",
    )
    name = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="Tshirts, Jeans, Watches, etc.",
    )
    display_name = Column(String(100), nullable=False, comment="顯示名稱（中文）")
    description = Column(Text, comment="類型說明")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    sub_category = relationship("SubCategory", back_populates="article_types")
    products = relationship("Product", back_populates="article_type")

    # Indexes (移除複合 unique index，改用 name unique)
    __table_args__ = tuple()

    def __repr__(self):
        return f"<ArticleType(id={self.id}, name='{self.name}', display_name='{self.display_name}')>"

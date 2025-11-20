"""
Lookup Tables - Sub Category Model
子分類查找表
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class SubCategory(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True, index=True)
    master_category_id = Column(
        Integer,
        ForeignKey("master_categories.id"),
        nullable=False,
        comment="所屬主分類",
    )
    name = Column(
        String(100), nullable=False, comment="Topwear, Bottomwear, Shoes, etc."
    )
    display_name = Column(String(100), nullable=False, comment="顯示名稱（中文）")
    description = Column(Text, comment="分類說明")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    master_category = relationship("MasterCategory", back_populates="sub_categories")
    products = relationship("Product", back_populates="sub_category")
    article_types = relationship("ArticleType", back_populates="sub_category")

    # Indexes
    __table_args__ = (
        Index("idx_master_sub_unique", "master_category_id", "name", unique=True),
    )

    def __repr__(self):
        return f"<SubCategory(id={self.id}, name='{self.name}', display_name='{self.display_name}')>"

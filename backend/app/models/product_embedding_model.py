"""
AI Recommendation - Product Embedding Model (Phase 3)
商品語義向量資料表
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    Index,
    LargeBinary,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ProductEmbedding(Base):
    __tablename__ = "product_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        unique=True,
        nullable=False,
        comment="所屬商品",
    )
    embedding_model = Column(
        String(100), nullable=False, comment="使用的 embedding 模型"
    )
    embedding_vector = Column(
        LargeBinary, nullable=False, comment="向量資料（序列化存儲）"
    )
    embedding_text = Column(Text, comment="用於生成向量的文本")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="embedding")

    # Indexes
    __table_args__ = (Index("idx_embedding_product", "product_id"),)

    def __repr__(self):
        return f"<ProductEmbedding(id={self.id}, product_id={self.product_id}, model='{self.embedding_model}')>"

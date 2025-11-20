"""
Order System - Order Item Model
訂單項目明細
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Index, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        Integer, ForeignKey("orders.id"), nullable=False, comment="所屬訂單"
    )
    product_id = Column(
        Integer, ForeignKey("products.id"), nullable=False, comment="商品"
    )

    # 商品資訊快照（防止後續價格變動）
    product_name = Column(String(500), nullable=False, comment="商品名稱（快照）")
    size_name = Column(String(50), comment="尺寸")
    unit_price = Column(DECIMAL(10, 2), nullable=False, comment="單價（快照）")
    quantity = Column(Integer, nullable=False, default=1, comment="數量")
    subtotal = Column(DECIMAL(10, 2), nullable=False, comment="小計")

    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    # Indexes
    __table_args__ = (
        Index("idx_order_items_order", "order_id"),
        Index("idx_order_items_product", "product_id"),
    )

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product='{self.product_name[:30]}...', qty={self.quantity})>"

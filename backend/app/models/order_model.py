"""
Order System - Order Model
訂單主表
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Index, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, comment="用戶ID")
    order_number = Column(String(50), unique=True, nullable=False, comment="訂單編號")

    # 收件人資訊
    customer_name = Column(String(200), nullable=False, comment="收件人姓名")
    customer_email = Column(String(200), comment="收件人 Email")
    customer_phone = Column(String(50), nullable=False, comment="收件人電話")
    shipping_address = Column(Text, nullable=False, comment="收件地址")

    # 訂單金額
    subtotal = Column(DECIMAL(10, 2), nullable=False, comment="商品小計")
    shipping_fee = Column(DECIMAL(10, 2), default=0, comment="運費")
    discount_amount = Column(DECIMAL(10, 2), default=0, comment="折扣金額")
    total_amount = Column(DECIMAL(10, 2), nullable=False, comment="訂單總額")

    # 訂單狀態
    status = Column(
        String(50),
        nullable=False,
        default="pending",
        comment="pending, confirmed, shipped, delivered, cancelled",
    )
    payment_status = Column(
        String(50), default="unpaid", comment="unpaid, paid, refunded"
    )
    payment_method = Column(String(50), comment="cash_on_delivery, credit_card, etc.")

    # 備註
    customer_note = Column(Text, comment="客戶備註")
    admin_note = Column(Text, comment="管理員備註")

    # 時間戳記
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="訂單建立時間")
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        comment="最後更新時間",
    )
    confirmed_at = Column(TIMESTAMP, comment="訂單確認時間")
    shipped_at = Column(TIMESTAMP, comment="出貨時間")
    delivered_at = Column(TIMESTAMP, comment="送達時間")

    # Relationships
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (
        Index("idx_order_number", "order_number"),
        Index("idx_order_status", "status"),
        Index("idx_created_status", "created_at", "status"),
    )

    def __repr__(self):
        return f"<Order(id={self.id}, number='{self.order_number}', status='{self.status}', total={self.total_amount})>"

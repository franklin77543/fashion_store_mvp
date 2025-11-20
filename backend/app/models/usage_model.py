"""
Lookup Tables - Usage Model
使用場合分類查找表
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Usage(Base):
    __tablename__ = "usages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(100),
        unique=True,
        nullable=False,
        comment="Casual, Formal, Sports, Ethnic, etc.",
    )
    display_name = Column(String(100), nullable=False, comment="顯示名稱（中文）")
    description = Column(Text, comment="使用場合說明")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    products = relationship("Product", back_populates="usage")

    def __repr__(self):
        return f"<Usage(id={self.id}, name='{self.name}', display_name='{self.display_name}')>"

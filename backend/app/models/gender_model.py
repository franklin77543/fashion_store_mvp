"""
Lookup Tables - Gender Model
性別分類查找表
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Gender(Base):
    __tablename__ = "genders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(
        String(50),
        unique=True,
        nullable=False,
        comment="Men, Women, Boys, Girls, Unisex",
    )
    display_name = Column(String(50), nullable=False, comment="顯示名稱（中文）")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    products = relationship("Product", back_populates="gender")

    def __repr__(self):
        return f"<Gender(id={self.id}, name='{self.name}', display_name='{self.display_name}')>"

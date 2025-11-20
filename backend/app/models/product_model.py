"""
Core Table - Product Model
商品主表
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
    DECIMAL,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Product(Base):
    __tablename__ = "products"

    # Primary Key
    id = Column(Integer, primary_key=True, comment="商品唯一識別碼（來自 CSV）")
    product_display_name = Column(String(500), nullable=False, comment="商品顯示名稱")

    # 分類關聯
    gender_id = Column(Integer, ForeignKey("genders.id"), comment="性別分類")
    master_category_id = Column(
        Integer, ForeignKey("master_categories.id"), comment="主分類"
    )
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id"), comment="子分類")
    article_type_id = Column(
        Integer, ForeignKey("article_types.id"), comment="商品類型"
    )

    # 商品屬性
    base_colour_id = Column(Integer, ForeignKey("colours.id"), comment="基礎顏色")
    season_id = Column(Integer, ForeignKey("seasons.id"), comment="適用季節")
    usage_id = Column(Integer, ForeignKey("usages.id"), comment="使用場合")
    year = Column(Integer, comment="年份")

    # 品牌與價格
    brand_id = Column(Integer, ForeignKey("brands.id"), comment="品牌")
    price = Column(DECIMAL(10, 2), comment="原價")
    discounted_price = Column(DECIMAL(10, 2), comment="折扣價")
    discount_percent = Column(Integer, comment="折扣百分比")

    # 商品描述
    description = Column(Text, comment="商品詳細描述（來自 JSON）")

    # 圖片資訊
    image_url = Column(String(1000), comment="主圖片 URL")
    has_front_image = Column(Boolean, default=False, comment="是否有正面圖")
    has_back_image = Column(Boolean, default=False, comment="是否有背面圖")
    has_search_image = Column(Boolean, default=False, comment="是否有搜尋用圖")

    # 商品狀態
    is_active = Column(Boolean, default=True, comment="是否上架")
    stock_count = Column(Integer, default=0, comment="庫存數量")

    # 評分與銷售
    rating = Column(DECIMAL(3, 2), default=0, comment="平均評分 (0-5)")
    review_count = Column(Integer, default=0, comment="評論數量")
    view_count = Column(Integer, default=0, comment="瀏覽次數")

    # 時間戳記
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="建立時間")
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="更新時間"
    )

    # Relationships
    gender = relationship("Gender", back_populates="products")
    master_category = relationship("MasterCategory", back_populates="products")
    sub_category = relationship("SubCategory", back_populates="products")
    article_type = relationship("ArticleType", back_populates="products")
    base_colour = relationship("Colour", back_populates="products")
    season = relationship("Season", back_populates="products")
    usage = relationship("Usage", back_populates="products")
    brand = relationship("Brand", back_populates="products")

    # Extended relationships
    images = relationship(
        "ProductImage", back_populates="product", cascade="all, delete-orphan"
    )
    attributes = relationship(
        "ProductAttribute", back_populates="product", cascade="all, delete-orphan"
    )
    sizes = relationship(
        "ProductSize", back_populates="product", cascade="all, delete-orphan"
    )
    reviews = relationship(
        "ProductReview", back_populates="product", cascade="all, delete-orphan"
    )
    embedding = relationship(
        "ProductEmbedding",
        back_populates="product",
        uselist=False,
        cascade="all, delete-orphan",
    )
    order_items = relationship("OrderItem", back_populates="product")

    # Indexes
    __table_args__ = (
        Index("idx_gender_master_category", "gender_id", "master_category_id"),
        Index("idx_colour_season", "base_colour_id", "season_id"),
        Index("idx_price", "price", "discounted_price"),
        Index("idx_active_created", "is_active", "created_at"),
        Index("idx_product_name", "product_display_name"),
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.product_display_name[:30]}...', is_active={self.is_active})>"

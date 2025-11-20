"""
Models Package
導入所有資料庫模型
"""

# Lookup Tables
from app.models.gender_model import Gender
from app.models.master_category_model import MasterCategory
from app.models.sub_category_model import SubCategory
from app.models.article_type_model import ArticleType
from app.models.colour_model import Colour
from app.models.season_model import Season
from app.models.usage_model import Usage
from app.models.brand_model import Brand

# Core Table
from app.models.product_model import Product

# Extended Tables
from app.models.product_image_model import ProductImage
from app.models.product_attribute_model import ProductAttribute
from app.models.product_size_model import ProductSize

# Order System
from app.models.order_model import Order
from app.models.order_item_model import OrderItem

# Review System (Phase 2)
from app.models.product_review_model import ProductReview

# AI Recommendation (Phase 3)
from app.models.product_embedding_model import ProductEmbedding

__all__ = [
    # Lookup Tables
    "Gender",
    "Category",
    "SubCategory",
    "ArticleType",
    "Colour",
    "Season",
    "Usage",
    "Brand",
    # Core Table
    "Product",
    # Extended Tables
    "ProductImage",
    "ProductAttribute",
    "ProductSize",
    # Order System
    "Order",
    "OrderItem",
    # Review System
    "ProductReview",
    # AI Recommendation
    "ProductEmbedding",
]

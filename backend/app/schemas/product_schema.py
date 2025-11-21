from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    id: Optional[int] = None
    product_display_name: Optional[str] = None
    gender_id: Optional[int] = None
    master_category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    article_type_id: Optional[int] = None
    base_colour_id: Optional[int] = None
    season_id: Optional[int] = None
    usage_id: Optional[int] = None
    brand_id: Optional[int] = None
    year: Optional[int] = None
    price: Optional[float] = None
    discounted_price: Optional[float] = None
    discount_percent: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    has_front_image: Optional[bool] = None
    has_back_image: Optional[bool] = None
    has_search_image: Optional[bool] = None
    is_active: Optional[bool] = None
    stock_count: Optional[int] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    view_count: Optional[int] = None

    model_config = {'from_attributes': True}

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_display_name: Optional[str] = None
    gender_id: Optional[int] = None
    master_category_id: Optional[int] = None
    sub_category_id: Optional[int] = None
    article_type_id: Optional[int] = None
    base_colour_id: Optional[int] = None
    season_id: Optional[int] = None
    year: Optional[int] = None
    usage_id: Optional[int] = None
    brand_id: Optional[int] = None
    price: Optional[float] = None
    discounted_price: Optional[float] = None
    discount_percent: Optional[float] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    has_front_image: Optional[bool] = None
    has_back_image: Optional[bool] = None
    has_search_image: Optional[bool] = None
    is_active: Optional[bool] = None
    stock_count: Optional[int] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    view_count: Optional[int] = None


class ProductImage(BaseModel):
    image_type: str
    image_url: str
    is_primary: bool
    display_order: int
    model_config = {
        "from_attributes": True
    }

class ProductAttribute(BaseModel):
    attribute_key: str
    attribute_value: str
    model_config = {
        "from_attributes": True
    }

class ProductDetail(ProductBase):
    id: int
    model_config = {'from_attributes': True}
    images: List[ProductImage] = []
    attributes: List[ProductAttribute] = []
    description: Optional[str]
    model_config = {
        "from_attributes": True
    }


class ProductList(BaseModel):
    total: int
    items: List[ProductBase]

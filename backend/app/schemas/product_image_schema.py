from pydantic import BaseModel
from typing import Optional



class ProductImageBase(BaseModel):
    product_id: int
    image_type: Optional[str] = None
    image_url: Optional[str] = None
    resolution: Optional[str] = None
    is_primary: Optional[bool] = None
    display_order: Optional[int] = None

class ProductImage(ProductImageBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class ProductImageCreate(ProductImageBase):
    pass


class ProductImageUpdate(BaseModel):
    image_type: Optional[str] = None
    image_url: Optional[str] = None
    resolution: Optional[str] = None
    is_primary: Optional[bool] = None
    display_order: Optional[int] = None

class ProductImageOut(ProductImage):
    model_config = {
        "from_attributes": True
    }

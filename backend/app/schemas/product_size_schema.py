from pydantic import BaseModel
from typing import Optional





class ProductSizeBase(BaseModel):
    product_id: int
    size_name: str
    stock_count: Optional[int] = None
    is_available: Optional[bool] = None

class ProductSize(ProductSizeBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class ProductSizeCreate(ProductSizeBase):
    pass


class ProductSizeUpdate(BaseModel):
    size_name: Optional[str] = None
    stock_count: Optional[int] = None
    is_available: Optional[bool] = None

class ProductSizeOut(ProductSize):
    model_config = {
        "from_attributes": True
    }

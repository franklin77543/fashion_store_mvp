from pydantic import BaseModel
from typing import Optional


class ProductAttribute(BaseModel):
    id: int
    product_id: int
    attribute_key: str
    attribute_value: str

class ProductAttributeCreate(BaseModel):
    product_id: int
    attribute_key: str
    attribute_value: str

class ProductAttributeUpdate(BaseModel):
    attribute_key: Optional[str] = None
    attribute_value: Optional[str] = None

class ProductAttributeOut(ProductAttribute):
    model_config = {
        "from_attributes": True
    }

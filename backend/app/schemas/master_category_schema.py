from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MasterCategoryBase(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None

class MasterCategory(MasterCategoryBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = {
        "from_attributes": True
    }

class MasterCategoryCreate(BaseModel):
    name: str
    display_name: str
    description: Optional[str] = None

class MasterCategoryUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None


class ProductBrief(BaseModel):
    id: int
    product_display_name: str

    model_config = {
        "from_attributes": True
    }


class SubCategoryBrief(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class MasterCategoryOut(MasterCategoryBase):
    id: int
    created_at: Optional[datetime] = None
    products: Optional[List[ProductBrief]] = None
    sub_categories: Optional[List[SubCategoryBrief]] = None

    model_config = {
        "from_attributes": True
    }

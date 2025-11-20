from pydantic import BaseModel
from typing import Optional



class BrandBase(BaseModel):
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: Optional[bool] = True

class Brand(BrandBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class BrandCreate(BaseModel):
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: Optional[bool] = True

class BrandUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: Optional[bool] = None

class BrandList(BaseModel):
    total: int
    items: list[Brand]
    model_config = {
        "from_attributes": True
    }

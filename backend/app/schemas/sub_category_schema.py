from pydantic import BaseModel
from typing import Optional



class SubCategory(BaseModel):
    id: int
    name: str
    master_category_id: int
    display_name: Optional[str]

class SubCategoryCreate(BaseModel):
    name: str
    master_category_id: int
    display_name: Optional[str] = None

class SubCategoryUpdate(BaseModel):
    name: Optional[str] = None
    master_category_id: Optional[int] = None
    display_name: Optional[str] = None

class SubCategoryOut(SubCategory):
    model_config = {
        "from_attributes": True
    }

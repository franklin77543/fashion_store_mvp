from pydantic import BaseModel
from typing import Optional



class GenderBase(BaseModel):
    name: str
    display_name: Optional[str] = None

class Gender(GenderBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class GenderCreate(BaseModel):
    name: str
    display_name: Optional[str] = None

class GenderUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None

class GenderList(BaseModel):
    total: int
    items: list[Gender]
    model_config = {
        "from_attributes": True
    }

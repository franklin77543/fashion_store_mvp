from pydantic import BaseModel
from typing import Optional




class SeasonBase(BaseModel):
    name: str
    display_name: Optional[str] = None

class Season(SeasonBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class SeasonCreate(SeasonBase):
    pass

class SeasonUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None

class SeasonOut(Season):
    model_config = {
        "from_attributes": True
    }

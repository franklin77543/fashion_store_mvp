from pydantic import BaseModel
from typing import Optional



class ColourBase(BaseModel):
    name: str
    display_name: Optional[str] = None

class Colour(ColourBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class ColourCreate(BaseModel):
    name: str
    display_name: Optional[str] = None

class ColourUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None

class ColourOut(Colour):
    model_config = {
        "from_attributes": True
    }

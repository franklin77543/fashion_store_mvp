from pydantic import BaseModel
from typing import Optional



class Usage(BaseModel):
    id: int
    name: str
    display_name: Optional[str]

class UsageCreate(BaseModel):
    name: str
    display_name: Optional[str] = None

class UsageUpdate(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None

class UsageOut(Usage):
    model_config = {
        "from_attributes": True
    }

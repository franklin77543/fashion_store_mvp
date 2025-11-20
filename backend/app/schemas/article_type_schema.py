from pydantic import BaseModel
from typing import Optional




class ArticleTypeBase(BaseModel):
    name: str
    sub_category_id: int
    display_name: Optional[str] = None

class ArticleType(ArticleTypeBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class ArticleTypeCreate(ArticleTypeBase):
    pass

class ArticleTypeUpdate(BaseModel):
    name: Optional[str] = None
    sub_category_id: Optional[int] = None
    display_name: Optional[str] = None

class ArticleTypeOut(ArticleType):
    model_config = {
        "from_attributes": True
    }

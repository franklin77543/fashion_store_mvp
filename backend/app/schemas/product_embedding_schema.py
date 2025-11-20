from pydantic import BaseModel
from typing import Optional





class ProductEmbeddingBase(BaseModel):
    product_id: int
    embedding_model: Optional[str] = None
    embedding_vector: Optional[bytes] = None
    embedding_text: Optional[str] = None

class ProductEmbedding(ProductEmbeddingBase):
    id: int
    model_config = {
        "from_attributes": True
    }

class ProductEmbeddingCreate(ProductEmbeddingBase):
    pass


class ProductEmbeddingUpdate(BaseModel):
    embedding_model: Optional[str] = None
    embedding_vector: Optional[bytes] = None
    embedding_text: Optional[str] = None

class ProductEmbeddingOut(ProductEmbedding):
    model_config = {
        "from_attributes": True
    }

from sqlalchemy.orm import Session
from app.models.product_embedding_model import ProductEmbedding
from typing import List, Optional


class ProductEmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_product_embeddings(self) -> List[ProductEmbedding]:
        return self.db.query(ProductEmbedding).all()

    def get_product_embedding_by_id(self, embedding_id: int) -> Optional[ProductEmbedding]:
        return (
            self.db.query(ProductEmbedding)
            .filter(ProductEmbedding.id == embedding_id)
            .first()
        )

    def create_product_embedding(self, data) -> ProductEmbedding:
        obj = ProductEmbedding(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_product_embedding(self, embedding_id: int, data) -> ProductEmbedding:
        obj = self.db.query(ProductEmbedding).filter(ProductEmbedding.id == embedding_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_product_embedding(self, embedding_id: int) -> None:
        obj = self.db.query(ProductEmbedding).filter(ProductEmbedding.id == embedding_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

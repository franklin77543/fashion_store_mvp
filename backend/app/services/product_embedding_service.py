from typing import List, Optional
from app.repositories.product_embedding_repository import ProductEmbeddingRepository
from app.schemas.product_embedding_schema import ProductEmbeddingOut


class ProductEmbeddingService:
    def __init__(self, repo: ProductEmbeddingRepository):
        self.repo = repo

    def create_product_embedding(self, data) -> ProductEmbeddingOut:
        embedding = self.repo.create_product_embedding(data)
        return ProductEmbeddingOut.model_validate(embedding)

    def update_product_embedding(self, embedding_id: int, data) -> ProductEmbeddingOut:
        embedding = self.repo.update_product_embedding(embedding_id, data)
        return ProductEmbeddingOut.model_validate(embedding)

    def delete_product_embedding(self, embedding_id: int) -> None:
        self.repo.delete_product_embedding(embedding_id)

    def get_product_embedding(self, embedding_id: int) -> Optional[ProductEmbeddingOut]:
        embedding = self.repo.get_product_embedding_by_id(embedding_id)
        if not embedding:
            return None
        return ProductEmbeddingOut.model_validate(embedding)

    def list_product_embeddings(self) -> List[ProductEmbeddingOut]:
        embeddings = self.repo.get_all_product_embeddings()
        return [ProductEmbeddingOut.model_validate(e) for e in embeddings]

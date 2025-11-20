from typing import List, Optional
from app.repositories.product_size_repository import ProductSizeRepository
from app.schemas.product_size_schema import ProductSizeOut


class ProductSizeService:
    def __init__(self, repo: ProductSizeRepository):
        self.repo = repo

    def create_product_size(self, data) -> ProductSizeOut:
        size = self.repo.create_product_size(data)
        return ProductSizeOut.model_validate(size)

    def update_product_size(self, size_id: int, data) -> ProductSizeOut:
        size = self.repo.update_product_size(size_id, data)
        return ProductSizeOut.model_validate(size)

    def delete_product_size(self, size_id: int) -> None:
        self.repo.delete_product_size(size_id)

    def get_product_size(self, size_id: int) -> Optional[ProductSizeOut]:
        size = self.repo.get_product_size_by_id(size_id)
        if not size:
            return None
        return ProductSizeOut.model_validate(size)

    def list_product_sizes(self) -> List[ProductSizeOut]:
        sizes = self.repo.get_all_product_sizes()
        return [ProductSizeOut.model_validate(s) for s in sizes]

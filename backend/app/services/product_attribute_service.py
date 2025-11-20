from typing import List, Optional
from app.repositories.product_attribute_repository import ProductAttributeRepository
from app.schemas.product_attribute_schema import (
    ProductAttributeCreate,
    ProductAttributeUpdate,
    ProductAttributeOut,
)


class ProductAttributeService:
    def __init__(self, repo: ProductAttributeRepository):
        self.repo = repo

    def create_attribute(self, data: ProductAttributeCreate) -> ProductAttributeOut:
        attr = self.repo.create_product_attribute(data)
        return ProductAttributeOut.model_validate(attr)

    def update_attribute(self, attribute_id: int, data: ProductAttributeUpdate) -> ProductAttributeOut:
        attr = self.repo.update_product_attribute(attribute_id, data)
        return ProductAttributeOut.model_validate(attr)

    def delete_attribute(self, attribute_id: int) -> None:
        self.repo.delete_product_attribute(attribute_id)

    def get_attribute(self, attribute_id: int) -> Optional[ProductAttributeOut]:
        attr = self.repo.get_product_attribute_by_id(attribute_id)
        if not attr:
            return None
        return ProductAttributeOut.model_validate(attr)

    def list_attributes(self, limit: int = 10) -> List[ProductAttributeOut]:
        attrs = self.repo.get_all_product_attributes(limit=limit)
        return [ProductAttributeOut.model_validate(a) for a in attrs]

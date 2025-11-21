from typing import List, Optional
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductDetail, ProductBase


class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    def create_product(self, data) -> ProductDetail:
        product = self.repo.create_product(data)
        return ProductDetail.model_validate(product)

    def update_product(self, product_id: int, data) -> ProductDetail:
        product = self.repo.update_product(product_id, data)
        return ProductDetail.model_validate(product)

    def delete_product(self, product_id: int) -> None:
        self.repo.delete_product(product_id)

    def get_product_detail(self, product_id: int) -> Optional[ProductDetail]:
        product = self.repo.get_product_by_id(product_id)
        if not product:
            return None
        return ProductDetail.model_validate(product)

    def list_products(self, skip: int = 0, limit: int = 20) -> List[ProductBase]:
        products = self.repo.get_products(skip=skip, limit=limit)
        return [ProductBase.model_validate(p) for p in products]

    def search_products(self, query: str, skip: int = 0, limit: int = 20) -> List[ProductBase]:
        products = self.repo.search_products(query=query, skip=skip, limit=limit)
        return [ProductBase.model_validate(p) for p in products]

    def filter_products(self, filters: dict, skip: int = 0, limit: int = 20) -> List[ProductBase]:
        products = self.repo.get_products(skip=skip, limit=limit)
        for key, value in filters.items():
            products = [p for p in products if getattr(p, key, None) == value]
        return [ProductBase.model_validate(p) for p in products]

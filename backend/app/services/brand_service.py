from typing import List, Optional
from app.repositories.brand_repository import BrandRepository
from app.schemas.brand_schema import Brand


class BrandService:
    def __init__(self, repo: BrandRepository):
        self.repo = repo

    def list_brands(self) -> List[Brand]:
        brands = self.repo.get_all_brands()
        return [Brand.model_validate(b) for b in brands]

    def get_brand(self, brand_id: int) -> Optional[Brand]:
        brand = self.repo.get_brand_by_id(brand_id)
        if not brand:
            return None
        return Brand.model_validate(brand)

    def create_brand(self, data) -> Brand:
        brand = self.repo.create_brand(data)
        return Brand.model_validate(brand)

    def update_brand(self, brand_id: int, data) -> Brand:
        brand = self.repo.update_brand(brand_id, data)
        return Brand.model_validate(brand)

    def delete_brand(self, brand_id: int) -> None:
        self.repo.delete_brand(brand_id)

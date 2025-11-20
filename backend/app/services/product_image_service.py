from typing import List, Optional
from app.repositories.product_image_repository import ProductImageRepository
from app.schemas.product_image_schema import ProductImageOut


class ProductImageService:
    def __init__(self, repo: ProductImageRepository):
        self.repo = repo

    def create_product_image(self, data) -> ProductImageOut:
        image = self.repo.create_product_image(data)
        return ProductImageOut.model_validate(image)

    def update_product_image(self, image_id: int, data) -> ProductImageOut:
        image = self.repo.update_product_image(image_id, data)
        return ProductImageOut.model_validate(image)

    def delete_product_image(self, image_id: int) -> None:
        self.repo.delete_product_image(image_id)

    def get_product_image(self, image_id: int) -> Optional[ProductImageOut]:
        image = self.repo.get_product_image_by_id(image_id)
        if not image:
            return None
        return ProductImageOut.model_validate(image)

    def list_product_images(self) -> List[ProductImageOut]:
        images = self.repo.get_all_product_images()
        return [ProductImageOut.model_validate(img) for img in images]

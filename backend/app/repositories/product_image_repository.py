from sqlalchemy.orm import Session
from app.models.product_image_model import ProductImage
from typing import List, Optional


class ProductImageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_product_images(self) -> List[ProductImage]:
        return self.db.query(ProductImage).all()

    def get_product_image_by_id(self, image_id: int) -> Optional[ProductImage]:
        return self.db.query(ProductImage).filter(ProductImage.id == image_id).first()

    def create_product_image(self, data) -> ProductImage:
        obj = ProductImage(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_product_image(self, image_id: int, data) -> ProductImage:
        obj = self.db.query(ProductImage).filter(ProductImage.id == image_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_product_image(self, image_id: int) -> None:
        obj = self.db.query(ProductImage).filter(ProductImage.id == image_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

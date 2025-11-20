from sqlalchemy.orm import Session
from app.models.product_attribute_model import ProductAttribute
from typing import List, Optional


class ProductAttributeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_product_attributes(self, limit: int = 100) -> List[ProductAttribute]:
        return self.db.query(ProductAttribute).limit(limit).all()

    def get_product_attribute_by_id(self, attribute_id: int) -> Optional[ProductAttribute]:
        return (
            self.db.query(ProductAttribute)
            .filter(ProductAttribute.id == attribute_id)
            .first()
        )

    def create_product_attribute(self, data) -> ProductAttribute:
        obj = ProductAttribute(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_product_attribute(self, attribute_id: int, data) -> ProductAttribute:
        obj = self.db.query(ProductAttribute).filter(ProductAttribute.id == attribute_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_product_attribute(self, attribute_id: int) -> None:
        obj = self.db.query(ProductAttribute).filter(ProductAttribute.id == attribute_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

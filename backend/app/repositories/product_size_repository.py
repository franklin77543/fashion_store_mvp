from sqlalchemy.orm import Session
from app.models.product_size_model import ProductSize
from typing import List, Optional


class ProductSizeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_product_sizes(self) -> List[ProductSize]:
        return self.db.query(ProductSize).all()

    def get_product_size_by_id(self, size_id: int) -> Optional[ProductSize]:
        return self.db.query(ProductSize).filter(ProductSize.id == size_id).first()

    def create_product_size(self, data) -> ProductSize:
        obj = ProductSize(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_product_size(self, size_id: int, data) -> ProductSize:
        obj = self.db.query(ProductSize).filter(ProductSize.id == size_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_product_size(self, size_id: int) -> None:
        obj = self.db.query(ProductSize).filter(ProductSize.id == size_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

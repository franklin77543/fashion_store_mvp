from sqlalchemy.orm import Session
from app.models.brand_model import Brand
from typing import List, Optional


class BrandRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_brands(self) -> List[Brand]:
        return self.db.query(Brand).all()

    def get_brand_by_id(self, brand_id: int) -> Optional[Brand]:
        return self.db.query(Brand).filter(Brand.id == brand_id).first()

    def create_brand(self, data) -> Brand:
        obj = Brand(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_brand(self, brand_id: int, data) -> Brand:
        obj = self.db.query(Brand).filter(Brand.id == brand_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_brand(self, brand_id: int) -> None:
        obj = self.db.query(Brand).filter(Brand.id == brand_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

from sqlalchemy.orm import Session
from app.models.sub_category_model import SubCategory
from typing import List, Optional


class SubCategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_sub_categories(self) -> List[SubCategory]:
        return self.db.query(SubCategory).all()

    def get_sub_category_by_id(self, sub_category_id: int) -> Optional[SubCategory]:
        return self.db.query(SubCategory).filter(SubCategory.id == sub_category_id).first()

    def create_sub_category(self, data) -> SubCategory:
        obj = SubCategory(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_sub_category(self, sub_category_id: int, data) -> SubCategory:
        obj = self.db.query(SubCategory).filter(SubCategory.id == sub_category_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_sub_category(self, sub_category_id: int) -> None:
        obj = self.db.query(SubCategory).filter(SubCategory.id == sub_category_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

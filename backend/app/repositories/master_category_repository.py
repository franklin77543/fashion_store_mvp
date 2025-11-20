from sqlalchemy.orm import Session
from app.models.master_category_model import MasterCategory
from typing import List, Optional


class MasterCategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_master_categories(self) -> List[MasterCategory]:
        return self.db.query(MasterCategory).all()

    def get_master_category_by_id(self, master_category_id: int) -> Optional[MasterCategory]:
        return (
            self.db.query(MasterCategory)
            .filter(MasterCategory.id == master_category_id)
            .first()
        )

    def create_master_category(self, data) -> MasterCategory:
        obj = MasterCategory(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_master_category(self, master_category_id: int, data) -> MasterCategory:
        obj = self.db.query(MasterCategory).filter(MasterCategory.id == master_category_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_master_category(self, master_category_id: int) -> None:
        obj = self.db.query(MasterCategory).filter(MasterCategory.id == master_category_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

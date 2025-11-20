from sqlalchemy.orm import Session
from app.models.usage_model import Usage
from typing import List, Optional


class UsageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_usages(self) -> List[Usage]:
        return self.db.query(Usage).all()

    def get_usage_by_id(self, usage_id: int) -> Optional[Usage]:
        return self.db.query(Usage).filter(Usage.id == usage_id).first()

    def create_usage(self, data) -> Usage:
        obj = Usage(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_usage(self, usage_id: int, data) -> Usage:
        obj = self.db.query(Usage).filter(Usage.id == usage_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_usage(self, usage_id: int) -> None:
        obj = self.db.query(Usage).filter(Usage.id == usage_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

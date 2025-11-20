from sqlalchemy.orm import Session
from app.models.gender_model import Gender
from typing import List, Optional


class GenderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_genders(self) -> List[Gender]:
        return self.db.query(Gender).all()

    def get_gender_by_id(self, gender_id: int) -> Optional[Gender]:
        return self.db.query(Gender).filter(Gender.id == gender_id).first()

    def create_gender(self, data) -> Gender:
        obj = Gender(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_gender(self, gender_id: int, data) -> Gender:
        obj = self.db.query(Gender).filter(Gender.id == gender_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_gender(self, gender_id: int) -> None:
        obj = self.db.query(Gender).filter(Gender.id == gender_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

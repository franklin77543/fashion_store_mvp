from sqlalchemy.orm import Session
from app.models.season_model import Season
from typing import List, Optional


class SeasonRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_seasons(self) -> List[Season]:
        return self.db.query(Season).all()

    def get_season_by_id(self, season_id: int) -> Optional[Season]:
        return self.db.query(Season).filter(Season.id == season_id).first()

    def create_season(self, data) -> Season:
        obj = Season(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_season(self, season_id: int, data) -> Season:
        obj = self.db.query(Season).filter(Season.id == season_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_season(self, season_id: int) -> None:
        obj = self.db.query(Season).filter(Season.id == season_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

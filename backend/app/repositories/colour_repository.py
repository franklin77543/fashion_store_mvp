from sqlalchemy.orm import Session
from app.models.colour_model import Colour
from typing import List, Optional


class ColourRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_colours(self) -> List[Colour]:
        return self.db.query(Colour).all()

    def get_colour_by_id(self, colour_id: int) -> Optional[Colour]:
        return self.db.query(Colour).filter(Colour.id == colour_id).first()

    def create_colour(self, data) -> Colour:
        obj = Colour(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_colour(self, colour_id: int, data) -> Colour:
        obj = self.db.query(Colour).filter(Colour.id == colour_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_colour(self, colour_id: int) -> None:
        obj = self.db.query(Colour).filter(Colour.id == colour_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

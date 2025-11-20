from sqlalchemy.orm import Session
from app.models.article_type_model import ArticleType
from typing import List, Optional


class ArticleTypeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_article_types(self) -> List[ArticleType]:
        return self.db.query(ArticleType).all()

    def get_article_type_by_id(self, article_type_id: int) -> Optional[ArticleType]:
        return self.db.query(ArticleType).filter(ArticleType.id == article_type_id).first()

    def create_article_type(self, data) -> ArticleType:
        obj = ArticleType(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_article_type(self, article_type_id: int, data) -> ArticleType:
        obj = self.db.query(ArticleType).filter(ArticleType.id == article_type_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_article_type(self, article_type_id: int) -> None:
        obj = self.db.query(ArticleType).filter(ArticleType.id == article_type_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

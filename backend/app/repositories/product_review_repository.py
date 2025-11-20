from sqlalchemy.orm import Session
from app.models.product_review_model import ProductReview
from typing import List, Optional


class ProductReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_product_reviews(self) -> List[ProductReview]:
        return self.db.query(ProductReview).all()

    def get_product_review_by_id(self, review_id: int) -> Optional[ProductReview]:
        return self.db.query(ProductReview).filter(ProductReview.id == review_id).first()

    def create_product_review(self, data) -> ProductReview:
        obj = ProductReview(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_product_review(self, review_id: int, data) -> ProductReview:
        obj = self.db.query(ProductReview).filter(ProductReview.id == review_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_product_review(self, review_id: int) -> None:
        obj = self.db.query(ProductReview).filter(ProductReview.id == review_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

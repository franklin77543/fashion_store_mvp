from typing import List, Optional
from app.repositories.product_review_repository import ProductReviewRepository
from app.schemas.product_review_schema import (
    ProductReviewCreate,
    ProductReviewUpdate,
    ProductReviewOut,
)


class ProductReviewService:
    def __init__(self, repo: ProductReviewRepository):
        self.repo = repo

    def create_product_review(self, data) -> ProductReviewOut:
        review = self.repo.create_product_review(data)
        return ProductReviewOut.model_validate(review)

    def update_product_review(self, review_id: int, data) -> ProductReviewOut:
        review = self.repo.update_product_review(review_id, data)
        return ProductReviewOut.model_validate(review)

    def delete_product_review(self, review_id: int) -> None:
        self.repo.delete_product_review(review_id)

    def get_product_review(self, review_id: int) -> Optional[ProductReviewOut]:
        review = self.repo.get_product_review_by_id(review_id)
        if not review:
            return None
        return ProductReviewOut.model_validate(review)

    def list_product_reviews(self) -> List[ProductReviewOut]:
        reviews = self.repo.get_all_product_reviews()
        return [ProductReviewOut.model_validate(r) for r in reviews]

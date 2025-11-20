from pydantic import BaseModel
from typing import Optional




class ProductReview(BaseModel):
    id: int
    product_id: int
    reviewer_name: Optional[str]
    reviewer_email: Optional[str]
    rating: Optional[int]
    title: Optional[str]
    content: str
    is_verified: Optional[bool]
    is_approved: Optional[bool]
    helpful_count: Optional[int]
    approved_at: Optional[str]


class ProductReviewCreate(BaseModel):
    product_id: int
    reviewer_name: Optional[str]
    reviewer_email: Optional[str]
    rating: Optional[int]
    title: Optional[str]
    content: str
    is_verified: Optional[bool] = None
    is_approved: Optional[bool] = None
    helpful_count: Optional[int] = None
    approved_at: Optional[str] = None


class ProductReviewUpdate(BaseModel):
    reviewer_name: Optional[str] = None
    reviewer_email: Optional[str] = None
    rating: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    is_verified: Optional[bool] = None
    is_approved: Optional[bool] = None
    helpful_count: Optional[int] = None
    approved_at: Optional[str] = None

class ProductReviewOut(ProductReview):
    model_config = {'from_attributes': True}

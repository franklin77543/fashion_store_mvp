from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from app.services.recommendation_service import RecommendationService

class RecommendationRequest(BaseModel):
    query: str
    limit: int = 10

class ProductRecommendation(BaseModel):
    product_id: int
    matchScore: float
    reason: str

router = APIRouter(prefix="/recommend", tags=["recommend"])

# Dependency
recommendation_service = RecommendationService()

@router.post("", response_model=List[ProductRecommendation])
async def recommend_api(request: RecommendationRequest):
    results = await recommendation_service.recommend(request.query, request.limit)
    return results

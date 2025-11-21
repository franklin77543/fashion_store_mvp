from fastapi import APIRouter, Depends, Query
from typing import List, Optional

from app.services.product_service import ProductService
from app.schemas.product_schema import ProductBase, ProductDetail
from app.dependencies import get_product_service



router = APIRouter(prefix="/products", tags=["products"])



@router.get("", response_model=List[ProductBase])
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    service: ProductService = Depends(get_product_service)
):
    return service.list_products(skip=(page-1)*limit, limit=limit)

@router.get("/search", response_model=List[ProductBase])
def search_products(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    service: ProductService = Depends(get_product_service)
):
    return service.search_products(query=q, skip=(page-1)*limit, limit=limit)

@router.get("/filter", response_model=List[ProductBase])
def filter_products(
    gender: Optional[str] = None,
    master_category: Optional[str] = None,
    sub_category: Optional[str] = None,
    article_type: Optional[str] = None,
    base_colour: Optional[str] = None,
    season: Optional[str] = None,
    usage: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    service: ProductService = Depends(get_product_service)
):
    filters = {
        "gender": gender,
        "master_category": master_category,
        "sub_category": sub_category,
        "article_type": article_type,
        "base_colour": base_colour,
        "season": season,
        "usage": usage,
        "min_price": min_price,
        "max_price": max_price,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    return service.filter_products(filters=filters, skip=(page-1)*limit, limit=limit)

@router.get("/{product_id}", response_model=ProductDetail)
def get_product_detail(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    return service.get_product_detail(product_id)

from fastapi import APIRouter, Depends
from typing import List
from app.services.master_category_service import MasterCategoryService
from app.schemas.master_category_schema import MasterCategoryBase
from app.dependencies import get_master_category_service

router = APIRouter(prefix="/master-categories", tags=["master-categories"])

@router.get("", response_model=List[MasterCategoryBase])
def list_master_categories(
    service: MasterCategoryService = Depends(get_master_category_service)
):
    return service.list_master_categories()

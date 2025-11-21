from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.repositories.master_category_repository import MasterCategoryRepository
from app.services.master_category_service import MasterCategoryService

def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    repo = ProductRepository(db)
    return ProductService(repo)

def get_master_category_service(db: Session = Depends(get_db)) -> MasterCategoryService:
    repo = MasterCategoryRepository(db)
    return MasterCategoryService(repo)

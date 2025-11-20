from sqlalchemy.orm import Session
from app.models.product_model import Product
from typing import List, Optional


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create_product(self, data) -> Product:
        obj = Product(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_product(self, product_id: int, data) -> Product:
        obj = self.db.query(Product).filter(Product.id == product_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_product(self, product_id: int) -> None:
        obj = self.db.query(Product).filter(Product.id == product_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

    def get_products(self, skip: int = 0, limit: int = 20) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def search_products(self, query: str, skip: int = 0, limit: int = 20) -> List[Product]:
        return (
            self.db.query(Product)
            .filter(Product.product_display_name.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def filter_products(
        self,
        gender: Optional[str] = None,
        category: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Product]:
        q = self.db.query(Product)
        if gender:
            q = q.filter(Product.gender.has(name=gender))
        if category:
            q = q.filter(Product.master_category.has(name=category))
        if price_min is not None:
            q = q.filter(Product.price >= price_min)
        if price_max is not None:
            q = q.filter(Product.price <= price_max)
        return q.offset(skip).limit(limit).all()

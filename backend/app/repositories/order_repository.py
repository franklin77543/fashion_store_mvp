from sqlalchemy.orm import Session
from app.models.order_model import Order
from typing import Optional


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def update_order(self, order_id: int, data) -> Order:
        obj = self.db.query(Order).filter(Order.id == order_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_order(self, order_id: int) -> None:
        obj = self.db.query(Order).filter(Order.id == order_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

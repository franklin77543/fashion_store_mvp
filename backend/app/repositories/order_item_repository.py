from sqlalchemy.orm import Session
from app.models.order_item_model import OrderItem
from typing import List, Optional


class OrderItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_order_items(self) -> List[OrderItem]:
        return self.db.query(OrderItem).all()

    def get_order_item_by_id(self, item_id: int) -> Optional[OrderItem]:
        return self.db.query(OrderItem).filter(OrderItem.id == item_id).first()

    def create_order_item(self, data) -> OrderItem:
        obj = OrderItem(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update_order_item(self, item_id: int, data) -> OrderItem:
        obj = self.db.query(OrderItem).filter(OrderItem.id == item_id).first()
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_order_item(self, item_id: int) -> None:
        obj = self.db.query(OrderItem).filter(OrderItem.id == item_id).first()
        if obj:
            self.db.delete(obj)
            self.db.commit()

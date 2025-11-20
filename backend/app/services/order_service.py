from typing import List, Optional
from app.repositories.order_repository import OrderRepository
from app.schemas.order_schema import OrderDetail, OrderBase


class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_new_order(self, order_data: dict) -> OrderDetail:
        from app.models.order_model import Order
        db_order = self.repo.create_order(Order(**order_data))
        return OrderDetail.model_validate(db_order)

    def update_order(self, order_id: int, data) -> OrderDetail:
        order = self.repo.update_order(order_id, data)
        return OrderDetail.model_validate(order)

    def delete_order(self, order_id: int) -> None:
        self.repo.delete_order(order_id)

    def get_order_detail(self, order_id: int) -> Optional[OrderDetail]:
        order = self.repo.get_order_by_id(order_id)
        if not order:
            return None
        return OrderDetail.model_validate(order)

from typing import List, Optional
from app.repositories.order_item_repository import OrderItemRepository
from app.schemas.order_item_schema import OrderItemCreate, OrderItemUpdate, OrderItemOut


class OrderItemService:
    def __init__(self, repo: OrderItemRepository):
        self.repo = repo

    def create_order_item(self, data) -> OrderItemOut:
        item = self.repo.create_order_item(data)
        return OrderItemOut.model_validate(item)

    def update_order_item(self, item_id: int, data) -> OrderItemOut:
        item = self.repo.update_order_item(item_id, data)
        return OrderItemOut.model_validate(item)

    def delete_order_item(self, item_id: int) -> None:
        self.repo.delete_order_item(item_id)

    def get_order_item(self, item_id: int) -> Optional[OrderItemOut]:
        item = self.repo.get_order_item_by_id(item_id)
        if not item:
            return None
        return OrderItemOut.model_validate(item)

    def list_order_items(self) -> List[OrderItemOut]:
        items = self.repo.get_all_order_items()
        return [OrderItemOut.model_validate(item) for item in items]

from pydantic import BaseModel
from typing import Optional


class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    product_name: Optional[str]
    unit_price: Optional[float]
    quantity: Optional[int]
    subtotal: Optional[float]


class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    product_name: Optional[str]
    unit_price: Optional[float]
    quantity: Optional[int]
    subtotal: Optional[float]


class OrderItemUpdate(BaseModel):
    product_name: Optional[str] = None
    unit_price: Optional[float] = None
    quantity: Optional[int] = None
    subtotal: Optional[float] = None


class OrderItemOut(OrderItem):
    model_config = {
        "from_attributes": True
    }

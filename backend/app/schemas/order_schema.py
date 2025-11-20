from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float



class OrderBase(BaseModel):
    id: int
    model_config = {'from_attributes': True}
    user_id: int
    order_number: Optional[str]
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_phone: Optional[str]
    shipping_address: Optional[str]
    subtotal: Optional[float]
    shipping_fee: Optional[float]
    discount_amount: Optional[float]
    total_amount: Optional[float]
    status: Optional[str]
    payment_status: Optional[str]
    payment_method: Optional[str]
    customer_note: Optional[str]
    admin_note: Optional[str]
    
class OrderCreate(BaseModel):
    user_id: int
    order_number: str
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str
    subtotal: float
    shipping_fee: float
    discount_amount: float
    total_amount: float
    status: str
    payment_status: str
    payment_method: str
    customer_note: Optional[str] = None
    admin_note: Optional[str] = None

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None
    payment_method: Optional[str] = None
    customer_note: Optional[str] = None
    admin_note: Optional[str] = None


class OrderDetail(OrderBase):
    items: List[OrderItem]
    model_config = {
        "from_attributes": True
    }


class OrderList(BaseModel):
    total: int
    items: List[OrderBase]
    model_config = {
        "from_attributes": True
    }

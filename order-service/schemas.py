from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class PlaceOrderRequest(BaseModel):
    customer_id: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    order_status: str
    total_amount: Decimal
    created_at: datetime
    items: list[OrderItemResponse]


class ErrorResponse(BaseModel):
    detail: str

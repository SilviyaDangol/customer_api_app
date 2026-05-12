from datetime import date
from typing import Optional, Literal

from pydantic import BaseModel, field_validator

OrderStatus = Literal[
    "Shipped",
    "Resolved",
    "Cancelled",
    "On Hold",
    "Disputed",
    "In Process",
]


class OrderCreate(BaseModel):
    orderNumber: int
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: OrderStatus
    comments: Optional[str] = None
    customerNumber: int

    @field_validator("requiredDate")
    @classmethod
    def validate_required_date(cls, value, info):
        order_date = info.data.get("orderDate")

        if order_date and value < order_date:
            raise ValueError("requiredDate must be after orderDate")

        return value


class OrderOut(OrderCreate):
    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    orderDate: Optional[date] = None
    requiredDate: Optional[date] = None
    shippedDate: Optional[date] = None
    status: Optional[OrderStatus] = None
    comments: Optional[str] = None
    customerNumber: Optional[int] = None

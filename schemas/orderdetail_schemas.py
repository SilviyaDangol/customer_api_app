from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class OrderDetailCreate(BaseModel):
    orderNumber: int
    productCode: str
    quantityOrdered: int = Field(..., gt=0)
    priceEach: Decimal
    orderLineNumber: int = Field(..., ge=1, le=32767)


class OrderDetailOut(OrderDetailCreate):
    model_config = ConfigDict(from_attributes=True)


class OrderDetailUpdate(BaseModel):
    quantityOrdered: Optional[int] = Field(None, gt=0)
    priceEach: Optional[Decimal] = None
    orderLineNumber: Optional[int] = Field(None, ge=1, le=32767)


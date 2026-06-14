from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict


class PaymentCreate(BaseModel):
    customerNumber: int
    checkNumber: str = Field(..., max_length=50)
    paymentDate: date
    amount: Decimal = Field(..., gt=0)

    @field_validator("paymentDate")
    @classmethod
    def validate_payment_date(cls, value):
        if value > date.today():
            raise ValueError("paymentDate cannot be in the future")

        return value


class PaymentOut(PaymentCreate):
    model_config = ConfigDict(from_attributes=True)


class PaymentUpdate(BaseModel):
    paymentDate: Optional[date] = None
    amount: Optional[Decimal] = Field(None, gt=0)

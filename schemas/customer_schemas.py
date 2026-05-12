from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date
from decimal import Decimal

class OrderOut(BaseModel):
    orderNumber: int
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: str
    comments: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PaymentOut(BaseModel):
    checkNumber: str
    paymentDate: date
    amount: Decimal

    model_config = ConfigDict(from_attributes=True)

class CustomerBase(BaseModel):
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

class CustomerCreate(CustomerBase):
    customerNumber: Optional[int] = None

class CustomerUpdate(BaseModel):
    customerName: Optional[str] = None
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[Decimal] = None

class CustomerOut(CustomerBase):
    customerNumber: int
    orders: List[OrderOut] = []
    payments: List[PaymentOut] = []

    model_config = ConfigDict(from_attributes=True)






    
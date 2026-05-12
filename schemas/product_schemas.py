from decimal import Decimal
from typing import Optional

from pydantic import field_validator, BaseModel, Field


class ProductCreate(BaseModel):
    productCode: str = Field(..., max_length=15)
    productName: str = Field(..., max_length=70)
    productLine: str
    productScale: str
    productVendor: str = Field(..., max_length=50)
    productDescription: str
    quantityInStock: int = Field(..., ge=0)
    buyPrice: Decimal
    MSRP: Decimal

    @field_validator("MSRP")
    @classmethod
    def validate_msrp(cls, value, info):
        buy_price = info.data.get("buyPrice")

        if buy_price is not None and value < buy_price:
            raise ValueError("MSRP must be >= buyPrice")

        return value


class ProductOut(ProductCreate):
    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    productName: Optional[str] = None
    productLine: Optional[str] = None
    productScale: Optional[str] = None
    productVendor: Optional[str] = None
    productDescription: Optional[str] = None
    quantityInStock: Optional[int] = Field(None, ge=0)
    buyPrice: Optional[Decimal] = None
    MSRP: Optional[Decimal] = None

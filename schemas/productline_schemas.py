from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ProductLineCreate(BaseModel):
    productLine: str = Field(max_length=50)
    textDescription: Optional[str] = Field(default=None, max_length=4000)
    htmlDescription: Optional[str] = None


class ProductLineOut(ProductLineCreate):
    model_config = ConfigDict(from_attributes=True)


class ProductLineUpdate(BaseModel):
    textDescription: Optional[str] = Field(default=None, max_length=4000)
    htmlDescription: Optional[str] = None
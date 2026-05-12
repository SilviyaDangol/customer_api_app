from pydantic import BaseModel


class CountResponse(BaseModel):
    count: int


class OverallCountsResponse(BaseModel):
    customers: int
    orders: int
    products: int
    employees: int
    offices: int
    payments: int
    orderdetails: int
    productlines: int

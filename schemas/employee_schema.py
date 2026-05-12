from typing import Optional

from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    employeeNumber: int
    lastName: str
    firstName: str
    extension: str
    email: str
    officeCode: str
    reportsTo: Optional[int] = None
    jobTitle: str


class EmployeeOut(EmployeeCreate):
    class Config:
        from_attributes = True


class EmployeeUpdate(BaseModel):
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    extension: Optional[str] = None
    email: Optional[str] = None
    officeCode: Optional[str] = None
    reportsTo: Optional[int] = None
    jobTitle: Optional[str] = None


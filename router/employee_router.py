# routers/employee_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db

from crud.employee_crud import (
    get_employees,
    get_employee,
    create_employee,
    update_employee,
    delete_employee,
    get_employee_with_customers,
    get_employee_reports,
)

from schemas.employee_schema import (
    EmployeeCreate,
    EmployeeOut,
    EmployeeUpdate,
)

from config.logger import logger

router = APIRouter()


@router.get("/", response_model=list[EmployeeOut])
def read_employees(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logger.info("GET /employees")

    return get_employees(db, skip, limit)


@router.get("/{employee_number}",
response_model=EmployeeOut)
def read_employee(
    employee_number: int,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /employees/{employee_number}"
    )

    return get_employee(db, employee_number)


@router.get("/{employee_number}/customers")
def read_employee_customers(
    employee_number: int,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /employees/{employee_number}/customers"
    )

    return get_employee_with_customers(
        db,
        employee_number
    )


@router.get("/{employee_number}/reports")
def read_employee_reports(
    employee_number: int,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /employees/{employee_number}/reports"
    )

    return get_employee_reports(
        db,
        employee_number
    )


@router.post("/", response_model=EmployeeOut)
def create_new_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
):
    logger.info("POST /employees")

    return create_employee(db, employee)


@router.put("/{employee_number}",
response_model=EmployeeOut)
def update_existing_employee(
    employee_number: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
):
    logger.info(
        f"PUT /employees/{employee_number}"
    )

    return update_employee(
        db,
        employee_number,
        employee
    )


@router.delete("/{employee_number}")
def remove_employee(
    employee_number: int,
    db: Session = Depends(get_db),
):
    logger.info(
        f"DELETE /employees/{employee_number}"
    )

    return delete_employee(
        db,
        employee_number
    )
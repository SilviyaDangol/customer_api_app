# crud/employee_crud.py

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.model import (
    Employee,
    Office,
    Customer,
)

from config.logger import logger


def get_employees(
    db: Session,
    skip=0,
    limit=100
):
    logger.info("Fetching employees")

    return (
        db.query(Employee)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_employee(
    db: Session,
    employee_number: int
):
    employee = (
        db.query(Employee)
        .filter(
            Employee.employeeNumber
            == employee_number
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


def create_employee(
    db: Session,
    employee_data
):

    office = (
        db.query(Office)
        .filter(
            Office.officeCode
            == employee_data.officeCode
        )
        .first()
    )

    if not office:
        raise HTTPException(
            status_code=422,
            detail="Invalid officeCode"
        )

    if employee_data.reportsTo:

        manager = (
            db.query(Employee)
            .filter(
                Employee.employeeNumber
                == employee_data.reportsTo
            )
            .first()
        )

        if not manager:
            raise HTTPException(
                status_code=422,
                detail="Invalid reportsTo"
            )

    db_employee = Employee(
        **employee_data.model_dump()
    )

    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)

        logger.info(
            f"Created employee "
            f"{employee_data.employeeNumber}"
        )

        return db_employee

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail="Employee creation failed"
        )


def update_employee(
    db: Session,
    employee_number: int,
    employee_data
):

    employee = get_employee(
        db,
        employee_number
    )

    update_data = employee_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    logger.info(
        f"Updated employee "
        f"{employee_number}"
    )

    return employee


def delete_employee(
    db: Session,
    employee_number: int
):

    employee = get_employee(
        db,
        employee_number
    )

    direct_reports = (
        db.query(Employee)
        .filter(
            Employee.reportsTo
            == employee_number
        )
        .count()
    )

    if direct_reports > 0:
        raise HTTPException(
            status_code=409,
            detail="Employee has direct reports"
        )

    customers = (
        db.query(Customer)
        .filter(
            Customer.salesRepEmployeeNumber
            == employee_number
        )
        .count()
    )

    if customers > 0:
        raise HTTPException(
            status_code=409,
            detail="Employee manages customers"
        )

    db.delete(employee)
    db.commit()

    logger.info(
        f"Deleted employee "
        f"{employee_number}"
    )

    return {
        "message": "Employee deleted successfully"
    }


def get_employee_with_customers(
    db: Session,
    employee_number: int
):

    employee = (
        db.query(Employee)
        .options(joinedload(Employee.customers))
        .filter(
            Employee.employeeNumber
            == employee_number
        )
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


def get_employee_reports(
    db: Session,
    employee_number: int
):

    return (
        db.query(Employee)
        .filter(
            Employee.reportsTo
            == employee_number
        )
        .all()
    )
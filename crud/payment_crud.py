# crud/payment_crud.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.model import (
    Payment,
    Customer,
)

from config.logger import logger


def get_payments(
    db: Session,
    skip=0,
    limit=100
):
    logger.info("Fetching payments")

    return (
        db.query(Payment)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_payment(
    db: Session,
    customer_number: int,
    check_number: str
):
    payment = (
        db.query(Payment)
        .filter(
            Payment.customerNumber
            == customer_number,
            Payment.checkNumber
            == check_number
        )
        .first()
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


def create_payment(
    db: Session,
    payment_data
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.customerNumber
            == payment_data.customerNumber
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=422,
            detail="Invalid customerNumber"
        )

    db_payment = Payment(
        **payment_data.model_dump()
    )

    try:
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)

        logger.info(
            f"Created payment "
            f"{payment_data.customerNumber} "
            f"{payment_data.checkNumber}"
        )

        return db_payment

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail="Payment creation failed"
        )


def update_payment(
    db: Session,
    customer_number: int,
    check_number: str,
    payment_data
):

    payment = get_payment(
        db,
        customer_number,
        check_number
    )

    update_data = payment_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)

    logger.info(
        f"Updated payment "
        f"{customer_number} "
        f"{check_number}"
    )

    return payment


def delete_payment(
    db: Session,
    customer_number: int,
    check_number: str
):

    payment = get_payment(
        db,
        customer_number,
        check_number
    )

    db.delete(payment)
    db.commit()

    logger.info(
        f"Deleted payment "
        f"{customer_number} "
        f"{check_number}"
    )

    return {
        "message": "Payment deleted successfully"
    }


def get_customer_payments(
    db: Session,
    customer_number: int
):

    return (
        db.query(Payment)
        .filter(
            Payment.customerNumber
            == customer_number
        )
        .all()
    )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db

from crud.payment_crud import (
    get_payments,
    get_payment,
    create_payment,
    update_payment,
    delete_payment,
    get_customer_payments,
)

from schemas.payment_schema import (
    PaymentCreate,
    PaymentOut,
    PaymentUpdate,
)

from config.logger import logger

router = APIRouter()


@router.get("/", response_model=list[PaymentOut])
def read_payments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logger.info("GET /payments")

    return get_payments(db, skip, limit)


@router.get(
    "/{customer_number}/{check_number}",
    response_model=PaymentOut
)
def read_payment(
    customer_number: int,
    check_number: str,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /payments/"
        f"{customer_number}/{check_number}"
    )

    return get_payment(
        db,
        customer_number,
        check_number
    )


@router.get("/customer/{customer_number}")
def read_customer_payments(
    customer_number: int,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /payments/customer/"
        f"{customer_number}"
    )

    return get_customer_payments(
        db,
        customer_number
    )


@router.post("/", response_model=PaymentOut)
def create_new_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
):
    logger.info("POST /payments")

    return create_payment(db, payment)


@router.put(
    "/{customer_number}/{check_number}",
    response_model=PaymentOut
)
def update_existing_payment(
    customer_number: int,
    check_number: str,
    payment: PaymentUpdate,
    db: Session = Depends(get_db),
):
    logger.info(
        f"PUT /payments/"
        f"{customer_number}/{check_number}"
    )

    return update_payment(
        db,
        customer_number,
        check_number,
        payment
    )


@router.delete("/{customer_number}/{check_number}")
def remove_payment(
    customer_number: int,
    check_number: str,
    db: Session = Depends(get_db),
):
    logger.info(
        f"DELETE /payments/"
        f"{customer_number}/{check_number}"
    )

    return delete_payment(
        db,
        customer_number,
        check_number
    )
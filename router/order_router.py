# routers/order_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db

from crud.order_crud import (
    get_orders,
    get_order,
    create_order,
    update_order,
    delete_order,
    get_order_with_orderdetails,
    get_customer_orders,
)

from schemas.order_schemas import (
    OrderCreate,
    OrderOut,
    OrderUpdate,
)

from config.logger import logger

router = APIRouter()


@router.get("/", response_model=list[OrderOut])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logger.info("GET /orders")

    return get_orders(db, skip, limit)


@router.get("/{order_number}",
response_model=OrderOut)
def read_order(
    order_number: int,
    db: Session = Depends(get_db),
):
    logger.info(f"GET /orders/{order_number}")

    return get_order(db, order_number)


@router.get("/{order_number}/orderdetails")
def read_order_orderdetails(
    order_number: int,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /orders/{order_number}/orderdetails"
    )

    return get_order_with_orderdetails(
        db,
        order_number
    )


@router.get("/customer/{customer_number}")
def read_customer_orders(
    customer_number: int,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /orders/customer/{customer_number}"
    )

    return get_customer_orders(
        db,
        customer_number
    )


@router.post("/", response_model=OrderOut)
def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
):
    logger.info("POST /orders")

    return create_order(db, order)


@router.put("/{order_number}",
response_model=OrderOut)
def update_existing_order(
    order_number: int,
    order: OrderUpdate,
    db: Session = Depends(get_db),
):
    logger.info(f"PUT /orders/{order_number}")

    return update_order(
        db,
        order_number,
        order
    )


@router.delete("/{order_number}")
def remove_order(
    order_number: int,
    db: Session = Depends(get_db),
):
    logger.info(f"DELETE /orders/{order_number}")

    return delete_order(
        db,
        order_number
    )
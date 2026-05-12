# crud/order_crud.py

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models.model import (
    Order,
    Customer,
)

from config.logger import logger


def get_orders(
    db: Session,
    skip=0,
    limit=100
):
    logger.info("Fetching orders")

    return (
        db.query(Order)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_order(
    db: Session,
    order_number: int
):
    order = (
        db.query(Order)
        .filter(
            Order.orderNumber
            == order_number
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


def create_order(
    db: Session,
    order_data
):

    customer = (
        db.query(Customer)
        .filter(
            Customer.customerNumber
            == order_data.customerNumber
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=422,
            detail="Invalid customerNumber"
        )

    db_order = Order(
        **order_data.model_dump()
    )

    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        logger.info(
            f"Created order "
            f"{order_data.orderNumber}"
        )

        return db_order

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail="Order creation failed"
        )


def update_order(
    db: Session,
    order_number: int,
    order_data
):

    order = get_order(
        db,
        order_number
    )

    update_data = order_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)

    logger.info(
        f"Updated order "
        f"{order_number}"
    )

    return order


def delete_order(
    db: Session,
    order_number: int
):

    order = get_order(
        db,
        order_number
    )

    try:
        db.delete(order)
        db.commit()

        logger.info(
            f"Deleted order "
            f"{order_number}"
        )

        return {
            "message": "Order deleted successfully"
        }

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Cannot delete order with orderdetails"
        )


def get_order_with_orderdetails(
    db: Session,
    order_number: int
):

    order = (
        db.query(Order)
        .options(joinedload(Order.order_details))
        .filter(
            Order.orderNumber
            == order_number
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


def get_customer_orders(
    db: Session,
    customer_number: int
):

    return (
        db.query(Order)
        .filter(
            Order.customerNumber
            == customer_number
        )
        .all()
    )
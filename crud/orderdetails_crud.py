# crud/orderdetail_crud.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models.model import (
    OrderDetail,
    Order,
    Product,
)

from config.logger import logger


def get_orderdetails(
    db: Session,
    skip=0,
    limit=100
):
    logger.info("Fetching orderdetails")

    return (
        db.query(OrderDetail)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_orderdetail(
    db: Session,
    order_number: int,
    product_code: str
):
    orderdetail = (
        db.query(OrderDetail)
        .filter(
            OrderDetail.orderNumber == order_number,
            OrderDetail.productCode == product_code
        )
        .first()
    )

    if not orderdetail:
        raise HTTPException(
            status_code=404,
            detail="OrderDetail not found"
        )

    return orderdetail


def create_orderdetail(
    db: Session,
    orderdetail_data
):

    order = (
        db.query(Order)
        .filter(
            Order.orderNumber
            == orderdetail_data.orderNumber
        )
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=422,
            detail="Invalid orderNumber"
        )

    product = (
        db.query(Product)
        .filter(
            Product.productCode
            == orderdetail_data.productCode
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=422,
            detail="Invalid productCode"
        )

    db_orderdetail = OrderDetail(
        **orderdetail_data.model_dump()
    )

    try:
        db.add(db_orderdetail)
        db.commit()
        db.refresh(db_orderdetail)

        logger.info(
            f"Created orderdetail "
            f"{orderdetail_data.orderNumber} "
            f"{orderdetail_data.productCode}"
        )

        return db_orderdetail

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=422,
            detail="OrderDetail creation failed"
        )


def update_orderdetail(
    db: Session,
    order_number: int,
    product_code: str,
    orderdetail_data
):

    orderdetail = get_orderdetail(
        db,
        order_number,
        product_code
    )

    update_data = orderdetail_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(orderdetail, key, value)

    db.commit()
    db.refresh(orderdetail)

    logger.info(
        f"Updated orderdetail "
        f"{order_number} {product_code}"
    )

    return orderdetail


def delete_orderdetail(
    db: Session,
    order_number: int,
    product_code: str
):

    orderdetail = get_orderdetail(
        db,
        order_number,
        product_code
    )

    db.delete(orderdetail)
    db.commit()

    logger.info(
        f"Deleted orderdetail "
        f"{order_number} {product_code}"
    )

    return {
        "message": "OrderDetail deleted successfully"
    }


def get_order_orderdetails(
    db: Session,
    order_number: int
):

    return (
        db.query(OrderDetail)
        .filter(
            OrderDetail.orderNumber == order_number
        )
        .all()
    )


def get_product_orderdetails(
    db: Session,
    product_code: str
):

    return (
        db.query(OrderDetail)
        .filter(
            OrderDetail.productCode == product_code
        )
        .all()
    )
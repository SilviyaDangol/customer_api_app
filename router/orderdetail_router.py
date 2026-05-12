from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db

from crud.orderdetails_crud import (
    get_orderdetails,
    get_orderdetail,
    create_orderdetail,
    update_orderdetail,
    delete_orderdetail,
    get_order_orderdetails,
    get_product_orderdetails,
)

from schemas.orderdetail_schemas import (
    OrderDetailCreate,
    OrderDetailOut,
    OrderDetailUpdate,
)

from config.logger import logger

router = APIRouter()


@router.get("/", response_model=list[OrderDetailOut])
def read_orderdetails(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logger.info("GET /orderdetails")

    return get_orderdetails(db, skip, limit)


@router.get(
    "/{order_number}/{product_code}",
    response_model=OrderDetailOut
)
def read_orderdetail(
    order_number: int,
    product_code: str,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /orderdetails/"
        f"{order_number}/{product_code}"
    )

    return get_orderdetail(
        db,
        order_number,
        product_code
    )


@router.get("/order/{order_number}")
def read_order_orderdetails(
    order_number: int,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /orderdetails/order/{order_number}"
    )

    return get_order_orderdetails(
        db,
        order_number
    )


@router.get("/product/{product_code}")
def read_product_orderdetails(
    product_code: str,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /orderdetails/product/{product_code}"
    )

    return get_product_orderdetails(
        db,
        product_code
    )


@router.post("/", response_model=OrderDetailOut)
def create_new_orderdetail(
    orderdetail: OrderDetailCreate,
    db: Session = Depends(get_db),
):
    logger.info("POST /orderdetails")

    return create_orderdetail(
        db,
        orderdetail
    )


@router.put(
    "/{order_number}/{product_code}",
    response_model=OrderDetailOut
)
def update_existing_orderdetail(
    order_number: int,
    product_code: str,
    orderdetail: OrderDetailUpdate,
    db: Session = Depends(get_db),
):
    logger.info(
        f"PUT /orderdetails/"
        f"{order_number}/{product_code}"
    )

    return update_orderdetail(
        db,
        order_number,
        product_code,
        orderdetail
    )


@router.delete("/{order_number}/{product_code}")
def remove_orderdetail(
    order_number: int,
    product_code: str,
    db: Session = Depends(get_db),
):
    logger.info(
        f"DELETE /orderdetails/"
        f"{order_number}/{product_code}"
    )

    return delete_orderdetail(
        db,
        order_number,
        product_code
    )
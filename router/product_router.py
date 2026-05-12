# routers/product_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db

from crud.product_crud import (
    get_products,
    get_product,
    create_product,
    update_product,
    delete_product,
    get_product_with_orderdetails,
)

from schemas.product_schemas import (
    ProductCreate,
    ProductOut,
    ProductUpdate,
)

from config.logger import logger

router = APIRouter()


@router.get("/", response_model=list[ProductOut])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logger.info("GET /products")

    return get_products(db, skip, limit)


@router.get("/{product_code}", response_model=ProductOut)
def read_product(
    product_code: str,
    db: Session = Depends(get_db),
):
    logger.info(f"GET /products/{product_code}")

    return get_product(db, product_code)


@router.get("/{product_code}/orderdetails")
def read_product_orderdetails(
    product_code: str,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /products/{product_code}/orderdetails"
    )

    return get_product_with_orderdetails(
        db,
        product_code
    )


@router.post("/", response_model=ProductOut)
def create_new_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    logger.info("POST /products")

    return create_product(db, product)


@router.put("/{product_code}",
response_model=ProductOut)
def update_existing_product(
    product_code: str,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    logger.info(f"PUT /products/{product_code}")

    return update_product(
        db,
        product_code,
        product
    )


@router.delete("/{product_code}")
def remove_product(
    product_code: str,
    db: Session = Depends(get_db),
):
    logger.info(f"DELETE /products/{product_code}")

    return delete_product(db, product_code)
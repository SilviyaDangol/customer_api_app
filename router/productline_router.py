from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from crud.productline_crud import (
    get_productlines,
    get_productline,
    create_productline,
    update_productline,
    delete_productline,
    get_productline_with_products,
)

from schemas.productline_schemas import (
    ProductLineCreate,
    ProductLineOut,
    ProductLineUpdate,
)

from config.logger import logger

router = APIRouter()


@router.get("/", response_model=list[ProductLineOut])
def read_productlines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    logger.info("GET /productlines")
    return get_productlines(db, skip, limit)


@router.get("/{product_line}", response_model=ProductLineOut)
def read_productline(
    product_line: str,
    db: Session = Depends(get_db)
):
    logger.info(f"GET /productlines/{product_line}")
    return get_productline(db, product_line)


@router.get("/{product_line}/products")
def read_productline_products(
    product_line: str,
    db: Session = Depends(get_db)
):
    logger.info(f"GET /productlines/{product_line}/products")
    return get_productline_with_products(db, product_line)


@router.post("/", response_model=ProductLineOut)
def create_new_productline(
    productline: ProductLineCreate,
    db: Session = Depends(get_db)
):
    logger.info("POST /productlines")
    return create_productline(db, productline)


@router.put("/{product_line}", response_model=ProductLineOut)
def update_existing_productline(
    product_line: str,
    productline: ProductLineUpdate,
    db: Session = Depends(get_db)
):
    logger.info(f"PUT /productlines/{product_line}")
    return update_productline(db, product_line, productline)


@router.delete("/{product_line}")
def remove_productline(
    product_line: str,
    db: Session = Depends(get_db)
):
    logger.info(f"DELETE /productlines/{product_line}")
    return delete_productline(db, product_line)
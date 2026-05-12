from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from config import logger
from models.model import Product, ProductLine


def get_products(db: Session, skip: int = 0, limit: int = 10):
    logger.info("Fetching products")

    return db.query(Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_code: str):
    product = db.query(Product).filter(
        Product.productCode == product_code
    ).first()

    if not product:
        logger.warning(f"Product not found: {product_code}")

        raise HTTPException(404, "Product not found")

    return product


def create_product(db: Session, data):
    fk = db.query(ProductLine).filter(
        ProductLine.productLine == data.productLine
    ).first()

    if not fk:
        raise HTTPException(422, "Invalid productLine")

    product = Product(**data.model_dump())

    try:
        db.add(product)
        db.commit()
        db.refresh(product)

        logger.info(f"Created product {product.productCode}")

        return product

    except IntegrityError:
        db.rollback()

        raise HTTPException(422, "Integrity error")


def update_product(db: Session, product_code: str, data):
    product = get_product(db, product_code)

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, product_code: str):
    product = get_product(db, product_code)

    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}


def get_product_with_orderdetails(db: Session, product_code: str):
    product = db.query(Product).options(
        joinedload(Product.order_details)
    ).filter(
        Product.productCode == product_code
    ).first()

    if not product:
        raise HTTPException(404, "Product not found")

    return product
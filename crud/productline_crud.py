from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from config.logger import logger
from models.model import ProductLine


def get_productlines(db: Session, skip: int = 0, limit: int = 100):
    logger.info("Fetching productlines")
    return db.query(ProductLine).offset(skip).limit(limit).all()


def get_productline(db: Session, product_line: str):
    productline = (
        db.query(ProductLine)
        .filter(ProductLine.productLine == product_line)
        .first()
    )

    if not productline:
        raise HTTPException(status_code=404, detail="ProductLine not found")

    return productline


def create_productline(db: Session, productline_data):
    db_productline = ProductLine(**productline_data.model_dump())

    try:
        db.add(db_productline)
        db.commit()
        db.refresh(db_productline)

        logger.info(f"Created productline {db_productline.productLine}")

        return db_productline

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=422, detail="Creation failed")


def update_productline(db: Session, product_line: str, data):
    db_productline = get_productline(db, product_line)

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_productline, key, value)

    db.commit()
    db.refresh(db_productline)

    logger.info(f"Updated productline {product_line}")

    return db_productline


def delete_productline(db: Session, product_line: str):
    db_productline = get_productline(db, product_line)

    try:
        db.delete(db_productline)
        db.commit()

        logger.info(f"Deleted productline {product_line}")

        return {"message": "Deleted successfully"}

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Cannot delete productline with existing products"
        )


def get_productline_with_products(db: Session, product_line: str):
    productline = (
        db.query(ProductLine)
        .options(joinedload(ProductLine.products))
        .filter(ProductLine.productLine == product_line)
        .first()
    )

    if not productline:
        raise HTTPException(status_code=404, detail="ProductLine not found")

    return productline
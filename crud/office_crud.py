from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from config.logger import logger
from models.model import Office


def get_offices(db: Session, skip=0, limit=100):
    logger.info("Fetching offices")
    return db.query(Office).offset(skip).limit(limit).all()


def get_office(db: Session, office_code: str):
    office = (
        db.query(Office)
        .filter(Office.officeCode == office_code)
        .first()
    )

    if not office:
        raise HTTPException(status_code=404, detail="Office not found")

    return office


def create_office(db: Session, office_data):
    db_office = Office(**office_data.model_dump())

    db.add(db_office)
    db.commit()
    db.refresh(db_office)

    logger.info(f"Created office {db_office.officeCode}")

    return db_office


def update_office(db: Session, office_code: str, data):
    office = get_office(db, office_code)

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(office, key, value)

    db.commit()
    db.refresh(office)

    logger.info(f"Updated office {office_code}")

    return office


def delete_office(db: Session, office_code: str):
    office = get_office(db, office_code)

    try:
        db.delete(office)
        db.commit()

        logger.info(f"Deleted office {office_code}")

        return {"message": "Office deleted"}

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Cannot delete office with employees"
        )


def get_office_with_employees(db: Session, office_code: str):
    office = (
        db.query(Office)
        .options(joinedload(Office.employees))
        .filter(Office.officeCode == office_code)
        .first()
    )

    if not office:
        raise HTTPException(status_code=404, detail="Office not found")

    return office
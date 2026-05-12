# routers/office_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db

from crud.office_crud import (
    get_offices,
    get_office,
    create_office,
    update_office,
    delete_office,
    get_office_with_employees,
)

from schemas.office_schemas import (
    OfficeCreate,
    OfficeOut,
    OfficeUpdate,
)

from config.logger import logger

router = APIRouter()


@router.get("/", response_model=list[OfficeOut])
def read_offices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    logger.info("GET /offices")

    return get_offices(db, skip, limit)


@router.get("/{office_code}", response_model=OfficeOut)
def read_office(
    office_code: str,
    db: Session = Depends(get_db),
):
    logger.info(f"GET /offices/{office_code}")

    return get_office(db, office_code)


@router.get("/{office_code}/employees")
def read_office_employees(
    office_code: str,
    db: Session = Depends(get_db),
):
    logger.info(
        f"GET /offices/{office_code}/employees"
    )

    return get_office_with_employees(
        db,
        office_code
    )


@router.post("/", response_model=OfficeOut)
def create_new_office(
    office: OfficeCreate,
    db: Session = Depends(get_db),
):
    logger.info("POST /offices")

    return create_office(db, office)


@router.put(
    "/{office_code}",
    response_model=OfficeOut
)
def update_existing_office(
    office_code: str,
    office: OfficeUpdate,
    db: Session = Depends(get_db),
):
    logger.info(f"PUT /offices/{office_code}")

    return update_office(
        db,
        office_code,
        office
    )


@router.delete("/{office_code}")
def remove_office(
    office_code: str,
    db: Session = Depends(get_db),
):
    logger.info(f"DELETE /offices/{office_code}")

    return delete_office(db, office_code)
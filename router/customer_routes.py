from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas.customer_schemas import CustomerCreate, CustomerUpdate, CustomerOut
from crud import customer_crud
from config.logger import logger

router = APIRouter()

@router.post("/", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    logger.info("Received request to create a new customer.")
    if customer.customerNumber:
        db_customer = customer_crud.get_customer(db, customer_id=customer.customerNumber)
        if db_customer:
            logger.warning(f"Failed to create: Customer ID {customer.customerNumber} already exists.")
            raise HTTPException(status_code=400, detail="Customer already exists")
    created = customer_crud.create_customer(db=db, customer=customer)
    return created

@router.get("/", response_model=List[CustomerOut])
def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info(f"Received request to get customers (skip={skip}, limit={limit}).")
    customers = customer_crud.get_customers(db, skip=skip, limit=limit)
    return customers

@router.get("/{customer_id}", response_model=CustomerOut)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to get customer ID {customer_id}.")
    db_customer = customer_crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        logger.warning(f"Customer not found: ID {customer_id}")
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    logger.info(f"Received request to update customer ID {customer_id}.")
    db_customer = customer_crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        logger.warning(f"Cannot update: Customer not found (ID: {customer_id})")
        raise HTTPException(status_code=404, detail="Customer not found")
    updated = customer_crud.update_customer(db=db, customer_id=customer_id, customer=customer)
    return updated

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Received request to delete customer ID {customer_id}.")
    db_customer = customer_crud.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        logger.warning(f"Cannot delete: Customer not found (ID: {customer_id})")
        raise HTTPException(status_code=404, detail="Customer not found")
    customer_crud.delete_customer(db=db, customer_id=customer_id)
    return

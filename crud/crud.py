from sqlalchemy.orm import Session, joinedload
from models.model import Customer
from schemas.schema import CustomerCreate, CustomerUpdate
from config.logger import logger

def get_customer(db: Session, customer_id: int):
    logger.info(f"Database query: fetch customer ID {customer_id}")
    return db.query(Customer).options(joinedload(Customer.orders), joinedload(Customer.payments)).filter(Customer.customerNumber == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 10):
    logger.info(f"Database query: fetch customers with skip={skip}, limit={limit}")
    return db.query(Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: CustomerCreate):
    logger.info("Database operation: Create customer")
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer: CustomerUpdate):
    logger.info(f"Database operation: Update customer ID {customer_id}")
    db_customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if db_customer:
        update_data = customer.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    logger.info(f"Database operation: Delete customer ID {customer_id}")
    db_customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer

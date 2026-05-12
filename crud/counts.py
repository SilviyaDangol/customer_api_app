from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from models.model import (
    Customer,
    Order,
    Product,
    Employee,
    Office,
    Payment,
    OrderDetail,
    ProductLine,
)

from config.logger import logger


async def get_customers_count(db: AsyncSession) -> int:
    try:
        logger.info("Starting customers count query")

        result = await db.execute(
            select(func.count(Customer.customerNumber))
        )

        count = result.scalar() or 0

        logger.info(f"Customers count completed: {count}")

        return count

    except Exception as e:
        logger.error(f"Customers count failed: {e}")
        return 0


async def get_orders_count(db: AsyncSession) -> int:
    try:
        logger.info("Starting orders count query")

        result = await db.execute(
            select(func.count(Order.orderNumber))
        )

        count = result.scalar() or 0

        logger.info(f"Orders count completed: {count}")

        return count

    except Exception as e:
        logger.error(f"Orders count failed: {e}")
        return 0


async def get_products_count(db: AsyncSession) -> int:
    try:
        logger.info("Starting products count query")

        result = await db.execute(
            select(func.count(Product.productCode))
        )

        count = result.scalar() or 0

        logger.info(f"Products count completed: {count}")

        return count

    except Exception as e:
        logger.error(f"Products count failed: {e}")
        return 0


async def get_employees_count(db: AsyncSession) -> int:
    try:
        logger.info("Starting employees count query")

        result = await db.execute(
            select(func.count(Employee.employeeNumber))
        )

        count = result.scalar() or 0

        logger.info(f"Employees count completed: {count}")

        return count

    except Exception as e:
        logger.error(f"Employees count failed: {e}")
        return 0


async def get_offices_count(db: AsyncSession) -> int:
    try:
        logger.info("Starting offices count query")

        result = await db.execute(
            select(func.count(Office.officeCode))
        )

        count = result.scalar() or 0

        logger.info(f"Offices count completed: {count}")

        return count

    except Exception as e:
        logger.error(f"Offices count failed: {e}")
        return 0


async def get_payments_count(db: AsyncSession) -> int:
    try:
        logger.info("Starting payments count query")

        result = await db.execute(
            select(func.count(Payment.customerNumber))
        )

        count = result.scalar() or 0

        logger.info(f"Payments count completed: {count}")

        return count

    except Exception as e:
        logger.error(f"Payments count failed: {e}")
        return 0


async def get_orderdetails_count(db: AsyncSession) -> int:
    try:
        logger.info("Starting orderdetails count query")

        result = await db.execute(
            select(func.count(OrderDetail.orderNumber))
        )

        count = result.scalar() or 0

        logger.info(f"Orderdetails count completed: {count}")

        return count

    except Exception as e:
        logger.error(f"Orderdetails count failed: {e}")
        return 0


async def get_productlines_count(db: AsyncSession) -> int:
    try:
        logger.info("Starting productlines count query")

        result = await db.execute(
            select(func.count(ProductLine.productLine))
        )

        count = result.scalar() or 0

        logger.info(f"Productlines count completed: {count}")

        return count

    except Exception as e:
        logger.error(f"Productlines count failed: {e}")
        return 0
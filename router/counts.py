import asyncio
import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from schemas.count_schema import (
    CountResponse,
    OverallCountsResponse,
)

from crud.counts import (
    get_customers_count,
    get_orders_count,
    get_products_count,
    get_employees_count,
    get_offices_count,
    get_payments_count,
    get_orderdetails_count,
    get_productlines_count,
)

from config.logger import logger

router = APIRouter(prefix="/count", tags=["Counts"])


# -------------------------
# Individual Endpoints
# -------------------------

@router.get("/customers/count", response_model=CountResponse)
async def customers_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /customers/count called")

    count = await get_customers_count(db)

    logger.info("GET /customers/count success")

    return {"count": count}


@router.get("/orders/count", response_model=CountResponse)
async def orders_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /orders/count called")

    count = await get_orders_count(db)

    logger.info("GET /orders/count success")

    return {"count": count}


@router.get("/products/count", response_model=CountResponse)
async def products_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /products/count called")

    count = await get_products_count(db)

    logger.info("GET /products/count success")

    return {"count": count}


@router.get("/employees/count", response_model=CountResponse)
async def employees_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /employees/count called")

    count = await get_employees_count(db)

    logger.info("GET /employees/count success")

    return {"count": count}


@router.get("/offices/count", response_model=CountResponse)
async def offices_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /offices/count called")

    count = await get_offices_count(db)

    logger.info("GET /offices/count success")

    return {"count": count}


@router.get("/payments/count", response_model=CountResponse)
async def payments_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /payments/count called")

    count = await get_payments_count(db)

    logger.info("GET /payments/count success")

    return {"count": count}


@router.get("/orderdetails/count", response_model=CountResponse)
async def orderdetails_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /orderdetails/count called")

    count = await get_orderdetails_count(db)

    logger.info("GET /orderdetails/count success")

    return {"count": count}


@router.get("/productlines/count", response_model=CountResponse)
async def productlines_count(db: AsyncSession = Depends(get_db)):
    logger.info("GET /productlines/count called")

    count = await get_productlines_count(db)

    logger.info("GET /productlines/count success")

    return {"count": count}


# -------------------------
# Aggregated Concurrent Endpoint
# -------------------------

@router.get(
    "/overall_counts",
    response_model=OverallCountsResponse,
)
async def overall_counts(db: AsyncSession = Depends(get_db)):

    logger.info("GET /overall_counts called")

    start_time = time.perf_counter()

    logger.info("Starting concurrent count tasks")

    tasks = [
        get_customers_count(db),
        get_orders_count(db),
        get_products_count(db),
        get_employees_count(db),
        get_offices_count(db),
        get_payments_count(db),
        get_orderdetails_count(db),
        get_productlines_count(db),
    ]

    results = await asyncio.gather(*tasks)

    logger.info("All concurrent tasks completed")

    elapsed = time.perf_counter() - start_time

    logger.info(f"/overall_counts completed in {elapsed:.4f} seconds")

    return {
        "customers": results[0],
        "orders": results[1],
        "products": results[2],
        "employees": results[3],
        "offices": results[4],
        "payments": results[5],
        "orderdetails": results[6],
        "productlines": results[7],
    }
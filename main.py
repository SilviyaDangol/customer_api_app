from fastapi import FastAPI

from config.logger import logger
from db.database import engine, Base

# Import routers
from router.customer_routes import router as customer_router
from router.product_router import router as product_router
from router.productline_router import router as productline_router
from router.office_router import router as office_router
from router.employee_router import router as employee_router
from router.order_router import router as order_router
from router.orderdetail_router import router as orderdetail_router
from router.payment_router import router as payment_router
from router.counts import router as counts_router


# Initialize FastAPI app
logger.info("Initializing FastAPI application.")

app = FastAPI(
    title="ClassicModels API",
    description="Full REST API for ClassicModels database",
    version="2.0.0"
)


# Create database tables
Base.metadata.create_all(bind=engine)


# Register routers
app.include_router(
    customer_router,
    prefix="/customers",
    tags=["Customers"]
)

app.include_router(
    counts_router,
    prefix="/counts",
    tags=["Counts"]
)

app.include_router(
    product_router,
    prefix="/products",
    tags=["Products"]
)

app.include_router(
    productline_router,
    prefix="/productlines",
    tags=["ProductLines"]
)

app.include_router(
    office_router,
    prefix="/offices",
    tags=["Offices"]
)

app.include_router(
    employee_router,
    prefix="/employees",
    tags=["Employees"]
)

app.include_router(
    order_router,
    prefix="/orders",
    tags=["Orders"]
)

app.include_router(
    orderdetail_router,
    prefix="/orderdetails",
    tags=["OrderDetails"]
)

app.include_router(
    payment_router,
    prefix="/payments",
    tags=["Payments"]
)


@app.get("/")
def root():

    logger.info("Root endpoint accessed.")

    return {
        "message": "ClassicModels API "
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
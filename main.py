from fastapi import FastAPI
from router.routes import router
from config.logger import logger
from db.database import engine, Base

# Create tables if not exist based on models
logger.info("Initializing FastAPI application.")
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer API", description="API for managing customers, orders, and payments.", version="1.0.0")

app.include_router(router)

@app.get("/")
def root():
    logger.info("Received request on root endpoint.")
    return {"message": "Welcome to the Customer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

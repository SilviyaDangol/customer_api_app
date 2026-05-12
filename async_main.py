from fastapi import FastAPI

from router.counts import router

from config.logger import logger

app = FastAPI(
    title="Concurrent Dashboard API",
    description="Async dashboard with concurrent database queries.",
    version="2.0.0",
)

logger.info("Initializing Async FastAPI application.")

app.include_router(router)


@app.get("/")
async def root():
    logger.info("Received request on async root endpoint.")

    return {
        "message": "Welcome to the Async Dashboard API"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main_async:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
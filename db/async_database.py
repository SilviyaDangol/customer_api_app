from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from sqlalchemy.orm import declarative_base

from config.settings import settings
from config.logger import logger


# IMPORTANT:
# Use async driver
# mysql+aiomysql://
DATABASE_URL = settings.async_database_url


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


Base = declarative_base()


async def get_async_db():
    logger.info("Initializing async database connection.")

    async with AsyncSessionLocal() as db:
        try:
            yield db

        except Exception as e:
            logger.error(f"Async database error: {e}")
            raise

        finally:
            logger.info("Closing async database connection.")
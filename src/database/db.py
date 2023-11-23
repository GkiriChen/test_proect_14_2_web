import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.conf.config import settings

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for SQLAlchemy models with asynchronous support."""
    pass


class DatabaseSessionManager:
    def __init__(self, url: str):
        """Initialize the DatabaseSessionManager with a given database URL.

        :param url: The database URL.
        :type url: str
        """
        # Create an asynchronous engine and session maker
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker | None = async_sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Context manager for providing an asynchronous database session.

        Yields an asynchronous session within the context.

        Usage:
        async with sessionmanager.session() as session:
            # Perform database operations using the 'session'

        Exceptions are caught, and the session is rolled back in case of an error.

        :yields: Asynchronous database session.
        :rtype: AsyncSession
        """
        if self._session_maker is None:
            raise Exception("DatabaseSessionManager is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()


# Create an instance of DatabaseSessionManager with the PostgreSQL URL from settings
sessionmanager = DatabaseSessionManager(settings.postgres_url)

# Dependency function for FastAPI to provide an asynchronous database session
async def get_db():
    async with sessionmanager.session() as session:
        yield session

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from main import app
from src.database.models import Base
from src.database.db import get_db


POSTGRES_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    POSTGRES_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def session():
    # Create the database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()


@pytest.fixture(scope="module")
async def client(session):
    # Dependency override
    async def override_get_db():
        try:
            yield session
        finally:
            await session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def user():
    return {"username": "deadpool", 
            "first_name": "Jone", 
            "last_name": "Doe", 
            "email": "deadpool@example.com", 
            "password": "123456789",
            "confirmed": False}

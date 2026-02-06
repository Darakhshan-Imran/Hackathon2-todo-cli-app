"""Pytest configuration and fixtures."""

import asyncio
from collections.abc import AsyncGenerator
from typing import Any
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from app.config import Settings, get_settings
from app.db.engine import _engine, _session_factory
from app.dependencies import get_db_session
from app.main import create_app
from app.models.user import User
from app.security.password import hash_password


# Test database URL (use SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


def get_test_settings() -> Settings:
    """Override settings for testing."""
    return Settings(
        database_url=TEST_DATABASE_URL,
        jwt_secret_key="test-secret-key-minimum-32-characters-here",
        environment="development",
    )


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )

    # Import models to register them with SQLModel
    from app.models.todo import Todo  # noqa: F401
    from app.models.user import User  # noqa: F401

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    session_factory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(test_engine, test_session) -> AsyncGenerator[AsyncClient, None]:
    """Create test HTTP client."""
    app = create_app()

    # Override dependencies
    async def override_get_db():
        yield test_session

    app.dependency_overrides[get_db_session] = override_get_db
    app.dependency_overrides[get_settings] = get_test_settings

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def test_user(test_session: AsyncSession) -> User:
    """Create a test user."""
    user = User(
        id=uuid4(),
        email="test@example.com",
        username="testuser",
        password_hash=hash_password("TestPassword123"),
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_user_2(test_session: AsyncSession) -> User:
    """Create a second test user for isolation tests."""
    user = User(
        id=uuid4(),
        email="test2@example.com",
        username="testuser2",
        password_hash=hash_password("TestPassword123"),
    )
    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User) -> dict[str, str]:
    """Create authorization headers for test user."""
    from app.security.jwt import create_access_token

    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers_user2(test_user_2: User) -> dict[str, str]:
    """Create authorization headers for second test user."""
    from app.security.jwt import create_access_token

    token = create_access_token(test_user_2.id)
    return {"Authorization": f"Bearer {token}"}

"""Async SQLAlchemy engine for Neon PostgreSQL."""

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

# Global engine and session factory
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker | None = None


async def init_engine(database_url: str) -> None:
    """
    Initialize the async database engine.

    Args:
        database_url: PostgreSQL connection string (asyncpg format)
    """
    global _engine, _session_factory

    _engine = create_async_engine(
        database_url,
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
    )

    _session_factory = async_sessionmaker(
        bind=_engine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )


async def dispose_engine() -> None:
    """Dispose the database engine and close all connections."""
    global _engine, _session_factory

    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None


def get_engine() -> AsyncEngine:
    """Get the database engine instance."""
    if _engine is None:
        raise RuntimeError("Database engine not initialized. Call init_engine first.")
    return _engine


def get_session_factory() -> async_sessionmaker:
    """Get the session factory instance."""
    if _session_factory is None:
        raise RuntimeError(
            "Session factory not initialized. Call init_engine first."
        )
    return _session_factory

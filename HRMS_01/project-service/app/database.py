"""Database setup for Project Service."""

from horilla_common.base import Base
from horilla_common.database import create_db_engine, create_session_factory

from app.config import get_settings
import app.models  # noqa: F401

settings = get_settings()
engine = create_db_engine(settings.database_url, echo=settings.debug)
async_session = create_session_factory(engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

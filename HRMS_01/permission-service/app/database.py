"""Database setup."""

import sqlalchemy as sa

from horilla_common.base import Base
from horilla_common.database import create_db_engine, create_session_factory

from app.config import get_settings
import app.models  # noqa: F401 - register models with metadata

settings = get_settings()
engine = create_db_engine(settings.database_url, echo=settings.debug)
async_session = create_session_factory(engine)


async def init_db():
    from seed import seed_permissions
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            sa.text("ALTER TABLE permission_permission ALTER COLUMN action TYPE VARCHAR(50)")
        )
    async with async_session() as session:
        await seed_permissions(session)



async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

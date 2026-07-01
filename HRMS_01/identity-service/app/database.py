"""Database setup."""

from horilla_common.base import Base
from horilla_common.database import create_db_engine, create_session_factory
from sqlalchemy import text

from app.config import get_settings
import app.models  # noqa: F401 - register models with metadata

settings = get_settings()
engine = create_db_engine(settings.database_url, echo=settings.debug)
async_session = create_session_factory(engine)


async def run_migration():
    """One-time migration: M2M junction table for DisciplinaryAction.

    Checks for old FK constraint on employee_id — when it is gone the
    migration is considered complete.
    """
    async with engine.begin() as conn:
        result = await conn.execute(text(
            "SELECT EXISTS (SELECT FROM information_schema.table_constraints "
            "WHERE table_name = 'employee_disciplinaryaction' "
            "AND constraint_name = 'employee_disciplinaryaction_employee_id_fkey')"
        ))
        if not result.scalar():
            return

        await conn.execute(text(
            "ALTER TABLE employee_disciplinaryaction "
            "DROP CONSTRAINT employee_disciplinaryaction_employee_id_fkey"
        ))
        await conn.execute(text(
            "ALTER TABLE employee_disciplinaryaction "
            "ALTER COLUMN employee_id DROP NOT NULL"
        ))
        await conn.execute(text(
            "INSERT INTO employee_disciplinaryaction_employee "
            "(disciplinary_action_id, employee_id) "
            "SELECT id, employee_id FROM employee_disciplinaryaction "
            "WHERE employee_id IS NOT NULL"
        ))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await run_migration()


async def get_db():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

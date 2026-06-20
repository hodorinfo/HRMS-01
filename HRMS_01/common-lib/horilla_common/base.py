"""SQLAlchemy base models and mixins."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class HorillaBaseMixin:
    """Mirrors Django HorillaModel abstract base."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    modified_by_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")

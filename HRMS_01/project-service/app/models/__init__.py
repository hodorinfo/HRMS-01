"""
Project Service Models.

Exact mirror of Horilla's project/models.py:
 - Project
 - ProjectStage
 - Task
 - TimeSheet
"""

import re
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from horilla_common.base import Base, HorillaBaseMixin


# ---------------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------------

class Project(Base, HorillaBaseMixin):
    """
    Mirrors Horilla project.models.Project
    """
    __tablename__ = "project_project"

    # Choices: new | in_progress | completed | on_hold | cancelled | expired
    title: Mapped[str] = mapped_column(String(200), unique=True)
    managers: Mapped[Optional[List]] = mapped_column(
        JSON, nullable=True, default=list,
        comment="Array of employee_id integers"
    )
    members: Mapped[Optional[List]] = mapped_column(
        JSON, nullable=True, default=list,
        comment="Array of employee_id integers"
    )
    status: Mapped[str] = mapped_column(String(50), default="new")
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    document: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True,
        comment="Stored file path / URL"
    )
    description: Mapped[str] = mapped_column(Text)
    company_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


# ---------------------------------------------------------------------------
# Project Stage  (Kanban column)
# ---------------------------------------------------------------------------

class ProjectStage(Base, HorillaBaseMixin):
    """
    Mirrors Horilla project.models.ProjectStage
    """
    __tablename__ = "project_projectstage"
    __table_args__ = (
        UniqueConstraint("project_id", "title", name="uq_stage_project_title"),
    )

    title: Mapped[str] = mapped_column(String(200))
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("project_project.id", ondelete="CASCADE"), nullable=True
    )
    sequence: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_end_stage: Mapped[bool] = mapped_column(Boolean, default=False)


# ---------------------------------------------------------------------------
# Task
# ---------------------------------------------------------------------------

class Task(Base, HorillaBaseMixin):
    """
    Mirrors Horilla project.models.Task
    """
    __tablename__ = "project_task"
    __table_args__ = (
        UniqueConstraint("project_id", "title", name="uq_task_project_title"),
    )

    # Choices: to_do | in_progress | completed | expired
    title: Mapped[str] = mapped_column(String(200))
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("project_project.id", ondelete="CASCADE"), nullable=True
    )
    stage_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("project_projectstage.id", ondelete="CASCADE"), nullable=True
    )
    task_managers: Mapped[Optional[List]] = mapped_column(
        JSON, nullable=True, default=list,
        comment="Array of employee_id integers"
    )
    task_members: Mapped[Optional[List]] = mapped_column(
        JSON, nullable=True, default=list,
        comment="Array of employee_id integers"
    )
    status: Mapped[str] = mapped_column(String(50), default="to_do")
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    document: Mapped[Optional[str]] = mapped_column(
        String(500), nullable=True,
        comment="Stored file path / URL"
    )
    description: Mapped[str] = mapped_column(Text)
    sequence: Mapped[int] = mapped_column(Integer, default=0)


# ---------------------------------------------------------------------------
# TimeSheet
# ---------------------------------------------------------------------------

class TimeSheet(Base, HorillaBaseMixin):
    """
    Mirrors Horilla project.models.TimeSheet
    """
    __tablename__ = "project_timesheet"

    # Choices: in_Progress | completed
    project_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("project_project.id", ondelete="CASCADE"), nullable=True
    )
    task_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("project_task.id", ondelete="SET NULL"), nullable=True
    )
    employee_id: Mapped[int] = mapped_column(Integer)
    date: Mapped[date] = mapped_column(Date)
    time_spent: Mapped[Optional[str]] = mapped_column(
        String(10), default="00:00",
        comment="HH:MM format"
    )
    status: Mapped[str] = mapped_column(String(50), default="in_Progress")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

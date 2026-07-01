"""
Project Service Pydantic Schemas.

Exact mirror of Horilla project/models.py field definitions.
"""

import re
from datetime import date
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class HorillaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Project Schemas
# ---------------------------------------------------------------------------

PROJECT_STATUS = Literal["new", "in_progress", "completed", "on_hold", "cancelled", "expired"]


class ProjectCreate(BaseModel):
    title: str
    description: str
    status: PROJECT_STATUS = "new"
    start_date: date
    end_date: Optional[date] = None
    managers: Optional[List[int]] = []
    members: Optional[List[int]] = []
    company_id: Optional[int] = None

    @field_validator("end_date")
    @classmethod
    def end_date_must_be_after_start(cls, v, info):
        start = info.data.get("start_date")
        if v is not None and start is not None and v < start:
            raise ValueError("end_date must be greater than or equal to start_date")
        return v


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[PROJECT_STATUS] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    managers: Optional[List[int]] = None
    members: Optional[List[int]] = None
    company_id: Optional[int] = None
    document: Optional[str] = None


class ProjectRead(HorillaSchema):
    id: int
    title: str
    description: str
    status: str
    start_date: date
    end_date: Optional[date] = None
    managers: Optional[List[int]] = []
    members: Optional[List[int]] = []
    company_id: Optional[int] = None
    document: Optional[str] = None
    is_active: bool = True


# ---------------------------------------------------------------------------
# Project Stage Schemas
# ---------------------------------------------------------------------------

class ProjectStageCreate(BaseModel):
    title: str
    project_id: Optional[int] = None
    sequence: Optional[int] = None
    is_end_stage: bool = False


class ProjectStageUpdate(BaseModel):
    title: Optional[str] = None
    is_end_stage: Optional[bool] = None
    sequence: Optional[int] = None


class ProjectStageRead(HorillaSchema):
    id: int
    title: str
    project_id: Optional[int] = None
    sequence: Optional[int] = None
    is_end_stage: bool = False
    is_active: bool = True


# ---------------------------------------------------------------------------
# Task Schemas
# ---------------------------------------------------------------------------

TASK_STATUS = Literal["to_do", "in_progress", "completed", "expired"]


class TaskCreate(BaseModel):
    title: str
    project_id: Optional[int] = None
    stage_id: Optional[int] = None
    description: str
    status: TASK_STATUS = "to_do"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    task_managers: Optional[List[int]] = []
    task_members: Optional[List[int]] = []
    document: Optional[str] = None
    sequence: int = 0


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    stage_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[TASK_STATUS] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    task_managers: Optional[List[int]] = None
    task_members: Optional[List[int]] = None
    document: Optional[str] = None
    sequence: Optional[int] = None


class TaskRead(HorillaSchema):
    id: int
    title: str
    project_id: Optional[int] = None
    stage_id: Optional[int] = None
    description: str
    status: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    task_managers: Optional[List[int]] = []
    task_members: Optional[List[int]] = []
    document: Optional[str] = None
    sequence: int = 0
    is_active: bool = True


# ---------------------------------------------------------------------------
# TimeSheet Schemas
# ---------------------------------------------------------------------------

TIMESHEET_STATUS = Literal["in_Progress", "completed"]

_TIME_PATTERN = re.compile(r"^\d{2}:\d{2}$")


class TimeSheetCreate(BaseModel):
    project_id: int
    task_id: Optional[int] = None
    employee_id: int
    date: date
    time_spent: str = "00:00"
    status: TIMESHEET_STATUS = "in_Progress"
    description: Optional[str] = None

    @field_validator("time_spent")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        if not _TIME_PATTERN.match(v):
            raise ValueError("time_spent must be in HH:MM format (e.g. 04:30)")
        hour, minute = v.split(":")
        if int(minute) not in range(60):
            raise ValueError("Minutes must be between 00 and 59")
        return v

    @field_validator("date")
    @classmethod
    def no_future_date(cls, v: date) -> date:
        from datetime import date as _date
        if v > _date.today():
            raise ValueError("You cannot choose a future date for a timesheet")
        return v


class TimeSheetUpdate(BaseModel):
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    employee_id: Optional[int] = None
    date: Optional[date] = None
    time_spent: Optional[str] = None
    status: Optional[TIMESHEET_STATUS] = None
    description: Optional[str] = None


class TimeSheetRead(HorillaSchema):
    id: int
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    employee_id: int
    date: date
    time_spent: Optional[str] = "00:00"
    status: str
    description: Optional[str] = None
    is_active: bool = True


# ---------------------------------------------------------------------------
# Special Action Schemas
# ---------------------------------------------------------------------------

class ChangeProjectStatusPayload(BaseModel):
    status: PROJECT_STATUS


class TaskStageChangePayload(BaseModel):
    task_id: int
    new_stage_id: int
    sequence: Optional[int] = None


class DragDropStagePayload(BaseModel):
    stage_id: int
    new_sequence: int


class BulkIdsPayload(BaseModel):
    ids: List[int]

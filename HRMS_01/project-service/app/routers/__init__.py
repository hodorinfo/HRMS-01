"""
Project Service Router Registry.

Registers all CRUD routers (via common-lib create_crud_router)
and custom action routers.
"""

from fastapi import APIRouter
from horilla_common.crud import create_crud_router

from app.database import get_db
from app.dependencies import get_current_user

from app.models import Project, ProjectStage, Task, TimeSheet
from app.schemas import (
    # Project
    ProjectCreate, ProjectUpdate, ProjectRead,
    # Stage
    ProjectStageCreate, ProjectStageUpdate, ProjectStageRead,
    # Task
    TaskCreate, TaskUpdate, TaskRead,
    # TimeSheet
    TimeSheetCreate, TimeSheetUpdate, TimeSheetRead,
)
from app.routers import health, project_actions

api_router = APIRouter()

# Health check
api_router.include_router(health.router)

# -------------------------------------------------------------------
# CRUD Routers — auto-generates:
#   GET    /{prefix}                     → list
#   POST   /{prefix}                     → create
#   GET    /{prefix}/{id}                → retrieve
#   PUT    /{prefix}/{id}                → update
#   DELETE /{prefix}/{id}                → delete
# -------------------------------------------------------------------
for prefix, model, create_schema, update_schema, read_schema, module_tag in [
    # Projects
    ("/projects",           Project,       ProjectCreate,       ProjectUpdate,       ProjectRead,       "Projects"),
    # Project Stages (Kanban columns)
    ("/project-stages",     ProjectStage,  ProjectStageCreate,  ProjectStageUpdate,  ProjectStageRead,  "Project Stages"),
    # Tasks
    ("/tasks",              Task,          TaskCreate,          TaskUpdate,          TaskRead,          "Tasks"),
    # Timesheets
    ("/timesheets",         TimeSheet,     TimeSheetCreate,     TimeSheetUpdate,     TimeSheetRead,     "Timesheets"),
]:
    api_router.include_router(
        create_crud_router(
            prefix, model, create_schema, update_schema, read_schema,
            get_db, get_current_user, module_tag
        )
    )

# -------------------------------------------------------------------
# Custom Action Routers (mirrors Horilla project/urls.py)
# -------------------------------------------------------------------
api_router.include_router(project_actions.router)

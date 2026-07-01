"""
Project Service Custom Action Routers.

Mirrors Horilla project/urls.py — all non-generic CRUD endpoints:
  - change-project-status
  - project-archive / task-all-archive
  - project-bulk-archive / project-bulk-delete
  - task-stage-change (drag & drop)
  - drag-and-drop-stage
  - quick-create-task
  - create-task-in-project  (creates task directly in first stage)
  - create-stage-taskall
  - get-stages
  - get-members-of-project
  - get-tasks-of-project  (for timesheet dropdowns)
  - personal-time-sheet-view
  - time-sheet-bulk-delete
  - task-all-bulk-archive / task-all-bulk-delete
  - update-project-task-status
  - project-dashboard summary
"""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Project, ProjectStage, Task, TimeSheet
from app.schemas import (
    ChangeProjectStatusPayload,
    DragDropStagePayload,
    ProjectRead,
    ProjectStageCreate,
    ProjectStageRead,
    TaskCreate,
    TaskRead,
    TaskStageChangePayload,
    TimeSheetRead,
    BulkIdsPayload,
)

router = APIRouter(tags=["Project Actions"])


# ---------------------------------------------------------------------------
# PROJECTS — Status / Archive / Bulk
# ---------------------------------------------------------------------------

@router.patch("/change-project-status/{project_id}", response_model=ProjectRead)
async def change_project_status(
    project_id: int,
    payload: ChangeProjectStatusPayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """PATCH /change-project-status/{project_id} — Change status of a project."""
    project = await db.get(Project, project_id)
    if not project or not project.is_active:
        raise HTTPException(status_code=404, detail="Project not found")
    project.status = payload.status
    await db.commit()
    await db.refresh(project)
    return project


@router.post("/project-archive/{project_id}")
async def project_archive(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /project-archive/{project_id} — Toggle archive status of a project."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.is_active = not project.is_active
    await db.commit()
    return {"id": project_id, "is_active": project.is_active}


@router.post("/project-bulk-archive")
async def project_bulk_archive(
    payload: BulkIdsPayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /project-bulk-archive — Archive multiple projects."""
    stmt = select(Project).where(Project.id.in_(payload.ids))
    results = await db.scalars(stmt)
    for p in results.all():
        p.is_active = False
    await db.commit()
    return {"status": "archived", "ids": payload.ids}


@router.post("/project-bulk-delete")
async def project_bulk_delete(
    payload: BulkIdsPayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /project-bulk-delete — Soft-delete multiple projects."""
    stmt = select(Project).where(Project.id.in_(payload.ids))
    results = await db.scalars(stmt)
    for p in results.all():
        p.is_active = False
    await db.commit()
    return {"status": "deleted", "ids": payload.ids}


# ---------------------------------------------------------------------------
# PROJECT STAGES — Get / Drag-Drop
# ---------------------------------------------------------------------------

@router.get("/get-stages", response_model=List[ProjectStageRead])
async def get_stages(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """GET /get-stages?project_id=1 — Return stages ordered by sequence."""
    stmt = (
        select(ProjectStage)
        .where(ProjectStage.project_id == project_id, ProjectStage.is_active == True)
        .order_by(ProjectStage.sequence)
    )
    results = await db.scalars(stmt)
    return results.all()


@router.patch("/drag-and-drop-stage")
async def drag_and_drop_stage(
    payload: DragDropStagePayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """PATCH /drag-and-drop-stage — Reorder a stage within a project."""
    stage = await db.get(ProjectStage, payload.stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    stage.sequence = payload.new_sequence
    await db.commit()
    return {"status": "updated", "stage_id": payload.stage_id, "new_sequence": payload.new_sequence}


@router.post("/create-stage-taskall")
async def create_stage_taskall(
    payload: ProjectStageCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /create-stage-taskall — Create a stage from the global task-all view."""
    # Compute next sequence for this project
    stmt = (
        select(ProjectStage)
        .where(ProjectStage.project_id == payload.project_id)
        .order_by(ProjectStage.sequence.desc())
    )
    results = await db.scalars(stmt)
    last_stage = results.first()
    next_seq = (last_stage.sequence or 0) + 1 if last_stage else 1

    new_stage = ProjectStage(
        title=payload.title,
        project_id=payload.project_id,
        is_end_stage=payload.is_end_stage,
        sequence=next_seq,
    )
    db.add(new_stage)
    await db.commit()
    await db.refresh(new_stage)
    return new_stage


# ---------------------------------------------------------------------------
# TASKS — Stage Change / Quick Create / Bulk / Status
# ---------------------------------------------------------------------------

@router.patch("/task-stage-change")
async def task_stage_change(
    payload: TaskStageChangePayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """PATCH /task-stage-change — Drag & drop a task to a new stage."""
    task = await db.get(Task, payload.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.stage_id = payload.new_stage_id
    if payload.sequence is not None:
        task.sequence = payload.sequence
    await db.commit()
    return {
        "status": "updated",
        "task_id": payload.task_id,
        "new_stage_id": payload.new_stage_id,
    }


@router.post("/quick-create-task/{stage_id}", response_model=TaskRead, status_code=201)
async def quick_create_task(
    stage_id: int,
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /quick-create-task/{stage_id} — Quickly create a task in a specific stage."""
    stage = await db.get(ProjectStage, stage_id)
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    new_task = Task(
        **payload.model_dump(),
        stage_id=stage_id,
        project_id=stage.project_id,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.post("/create-task-in-project/{project_id}", response_model=TaskRead, status_code=201)
async def create_task_in_project(
    project_id: int,
    payload: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /create-task-in-project/{project_id} — Create a task in the first stage of a project."""
    # Get first stage of project
    stmt = (
        select(ProjectStage)
        .where(ProjectStage.project_id == project_id, ProjectStage.is_active == True)
        .order_by(ProjectStage.sequence)
    )
    results = await db.scalars(stmt)
    first_stage = results.first()

    new_task = Task(
        **payload.model_dump(exclude={"project_id", "stage_id"}),
        project_id=project_id,
        stage_id=first_stage.id if first_stage else None,
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@router.patch("/update-project-task-status/{task_id}")
async def update_project_task_status(
    task_id: int,
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """PATCH /update-project-task-status/{task_id} — Update task status inline."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    new_status = payload.get("status")
    if new_status:
        task.status = new_status
    await db.commit()
    return {"task_id": task_id, "status": task.status}


@router.post("/task-all-archive/{task_id}")
async def task_all_archive(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /task-all-archive/{task_id} — Toggle archive of a task from global view."""
    task = await db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.is_active = not task.is_active
    await db.commit()
    return {"id": task_id, "is_active": task.is_active}


@router.post("/task-all-bulk-archive")
async def task_all_bulk_archive(
    payload: BulkIdsPayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /task-all-bulk-archive — Archive multiple tasks."""
    stmt = select(Task).where(Task.id.in_(payload.ids))
    results = await db.scalars(stmt)
    for t in results.all():
        t.is_active = False
    await db.commit()
    return {"status": "archived", "ids": payload.ids}


@router.post("/task-all-bulk-delete")
async def task_all_bulk_delete(
    payload: BulkIdsPayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /task-all-bulk-delete — Soft-delete multiple tasks."""
    stmt = select(Task).where(Task.id.in_(payload.ids))
    results = await db.scalars(stmt)
    for t in results.all():
        t.is_active = False
    await db.commit()
    return {"status": "deleted", "ids": payload.ids}


# ---------------------------------------------------------------------------
# TIMESHEET — Helper lookups / Personal view / Bulk delete
# ---------------------------------------------------------------------------

@router.get("/get-members-of-project")
async def get_members_of_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """GET /get-members-of-project?project_id=1 — Returns managers+members employee_ids."""
    project = await db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    all_ids = list(set((project.managers or []) + (project.members or [])))
    return {"project_id": project_id, "employee_ids": all_ids}


@router.get("/get-tasks-of-project")
async def get_tasks_of_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """GET /get-tasks-of-project?project_id=1 — Tasks for timesheet dropdown."""
    stmt = select(Task).where(Task.project_id == project_id, Task.is_active == True)
    results = await db.scalars(stmt)
    tasks = results.all()
    return [{"id": t.id, "title": t.title} for t in tasks]


@router.get("/personal-time-sheet-view/{emp_id}", response_model=List[TimeSheetRead])
async def personal_time_sheet_view(
    emp_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """GET /personal-time-sheet-view/{emp_id} — All timesheets for an employee."""
    stmt = select(TimeSheet).where(
        TimeSheet.employee_id == emp_id, TimeSheet.is_active == True
    )
    results = await db.scalars(stmt)
    return results.all()


@router.post("/time-sheet-bulk-delete")
async def time_sheet_bulk_delete(
    payload: BulkIdsPayload,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """POST /time-sheet-bulk-delete — Soft-delete multiple timesheets."""
    stmt = select(TimeSheet).where(TimeSheet.id.in_(payload.ids))
    results = await db.scalars(stmt)
    for ts in results.all():
        ts.is_active = False
    await db.commit()
    return {"status": "deleted", "ids": payload.ids}


# ---------------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------------

@router.get("/project-dashboard-view")
async def project_dashboard_view(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """GET /project-dashboard-view — Summary counts by status."""
    all_projects_stmt = select(Project).where(Project.is_active == True)
    projects = (await db.scalars(all_projects_stmt)).all()

    status_counts: dict = {}
    for p in projects:
        status_counts[p.status] = status_counts.get(p.status, 0) + 1

    all_tasks_stmt = select(Task).where(Task.is_active == True)
    tasks = (await db.scalars(all_tasks_stmt)).all()
    task_status_counts: dict = {}
    for t in tasks:
        task_status_counts[t.status] = task_status_counts.get(t.status, 0) + 1

    return {
        "project_status_chart": status_counts,
        "task_status_chart": task_status_counts,
        "total_projects": len(projects),
        "total_tasks": len(tasks),
    }


@router.get("/projects-due-in-this-month", response_model=List[ProjectRead])
async def projects_due_in_month(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """GET /projects-due-in-this-month — Projects whose end_date is in the current month."""
    today = date.today()
    stmt = select(Project).where(
        Project.is_active == True,
        Project.end_date != None,
        Project.end_date >= today.replace(day=1),
    )
    results = await db.scalars(stmt)
    return results.all()


@router.get("/project-detailed-view/{pk}", response_model=ProjectRead)
async def project_detailed_view(
    pk: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """GET /project-detailed-view/{pk} — Full project detail with stages+tasks."""
    project = await db.get(Project, pk)
    if not project or not project.is_active:
        raise HTTPException(status_code=404, detail="Project not found")

    # Fetch stages
    stages_stmt = (
        select(ProjectStage)
        .where(ProjectStage.project_id == pk, ProjectStage.is_active == True)
        .order_by(ProjectStage.sequence)
    )
    stages = (await db.scalars(stages_stmt)).all()

    # Fetch tasks per stage
    stage_data = []
    for stage in stages:
        tasks_stmt = select(Task).where(
            Task.stage_id == stage.id, Task.is_active == True
        ).order_by(Task.sequence)
        tasks = (await db.scalars(tasks_stmt)).all()
        stage_data.append({
            "id": stage.id,
            "title": stage.title,
            "sequence": stage.sequence,
            "is_end_stage": stage.is_end_stage,
            "tasks": [
                {
                    "id": t.id,
                    "title": t.title,
                    "status": t.status,
                    "task_managers": t.task_managers,
                    "task_members": t.task_members,
                    "start_date": str(t.start_date) if t.start_date else None,
                    "end_date": str(t.end_date) if t.end_date else None,
                }
                for t in tasks
            ],
        })

    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "status": project.status,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "managers": project.managers,
        "members": project.members,
        "company_id": project.company_id,
        "document": project.document,
        "is_active": project.is_active,
        "stages": stage_data,
    }

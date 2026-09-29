"""Workflow router — /api/v1/workflow"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.domain import TaskCreate, TaskUpdate, TaskStatusUpdate
from app.services.domain_service import (
    create_task, get_tasks, get_task, update_task,
    update_task_status, delete_task, get_task_timeline
)
from app.dependencies.auth import get_current_active_user
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/workflow", tags=["Workflow"])


@router.get("/timeline", summary="Get full task timeline sorted by due date")
async def task_timeline(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    timeline = await get_task_timeline(db, current_user["id"])
    return success_response(timeline, "Timeline fetched")


@router.get("", summary="List all tasks (no slash)")
@router.get("/", summary="List all tasks")
async def list_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    task_type: str = Query(None),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    result = await get_tasks(db, current_user["id"], page, limit, status, task_type)
    return success_response(result["tasks"], "Tasks fetched", result["pagination"])


@router.post("", summary="Create a new task (no slash)", status_code=201)
@router.post("/", summary="Create a new task", status_code=201)
async def add_task(
    data: TaskCreate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    task = await create_task(db, current_user["id"], data)
    return success_response(task, "Task created successfully")


@router.get("/{task_id}", summary="Get a single task")
async def get_single_task(
    task_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    task = await get_task(db, task_id, current_user["id"])
    return success_response(task, "Task fetched")


@router.put("/{task_id}", summary="Update a task")
async def edit_task(
    task_id: str,
    data: TaskUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    task = await update_task(db, task_id, current_user["id"], data)
    return success_response(task, "Task updated successfully")


@router.patch("/{task_id}/status", summary="Update task status only")
async def set_task_status(
    task_id: str,
    data: TaskStatusUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    task = await update_task_status(db, task_id, current_user["id"], data)
    return success_response(task, f"Task marked as {data.status}")


@router.delete("/{task_id}", summary="Delete a task")
async def remove_task(
    task_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    await delete_task(db, task_id, current_user["id"])
    return success_response(None, "Task deleted successfully")

"""Plots router — /api/v1/plots"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.domain import PlotCreate, PlotUpdate
from app.services.domain_service import (
    create_plot, get_plots, get_plot, update_plot, delete_plot
)
from app.dependencies.auth import get_current_active_user
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/plots", tags=["Plot Management"])


@router.get("/", summary="Get all plots for current user")
async def list_plots(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    crop: str = Query(None),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    result = await get_plots(db, current_user["id"], page, limit, status, crop)
    return success_response(result["plots"], "Plots fetched", result["pagination"])


@router.post("/", summary="Create a new plot", status_code=201)
async def add_plot(
    data: PlotCreate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    plot = await create_plot(db, current_user["id"], data)
    return success_response(plot, "Plot created successfully")


@router.get("/{plot_id}", summary="Get a single plot by ID")
async def get_single_plot(
    plot_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    plot = await get_plot(db, plot_id, current_user["id"])
    return success_response(plot, "Plot fetched")


@router.put("/{plot_id}", summary="Update a plot")
async def edit_plot(
    plot_id: str,
    data: PlotUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    plot = await update_plot(db, plot_id, current_user["id"], data)
    return success_response(plot, "Plot updated successfully")


@router.delete("/{plot_id}", summary="Delete a plot")
async def remove_plot(
    plot_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    await delete_plot(db, plot_id, current_user["id"])
    return success_response(None, "Plot deleted successfully")

"""Ledger router — /api/v1/ledger"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.schemas.domain import LedgerCreate, LedgerUpdate
from app.services.domain_service import (
    create_ledger_entry, get_ledger_entries, get_ledger_entry,
    update_ledger_entry, delete_ledger_entry, get_ledger_summary
)
from app.dependencies.auth import get_current_active_user
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/ledger", tags=["Ledger"])


@router.get("/summary", summary="Get income, expenses, and profit summary")
async def ledger_summary(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    summary = await get_ledger_summary(db, current_user["id"])
    return success_response(summary, "Ledger summary fetched")


@router.get("", summary="List all ledger entries (no slash)")
@router.get("/", summary="List all ledger entries")
async def list_entries(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    type: str = Query(None, description="Income or Expense"),
    category: str = Query(None),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    result = await get_ledger_entries(db, current_user["id"], page, limit, type, category)
    return success_response(result["entries"], "Entries fetched", result["pagination"])


@router.post("", summary="Add a new ledger entry (no slash)", status_code=201)
@router.post("/", summary="Add a new ledger entry", status_code=201)
async def add_entry(
    data: LedgerCreate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    entry = await create_ledger_entry(db, current_user["id"], data)
    return success_response(entry, "Entry added successfully")


@router.get("/{entry_id}", summary="Get a single ledger entry")
async def get_entry(
    entry_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    entry = await get_ledger_entry(db, entry_id, current_user["id"])
    return success_response(entry, "Entry fetched")


@router.put("/{entry_id}", summary="Update a ledger entry")
async def edit_entry(
    entry_id: str,
    data: LedgerUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    entry = await update_ledger_entry(db, entry_id, current_user["id"], data)
    return success_response(entry, "Entry updated successfully")


@router.delete("/{entry_id}", summary="Delete a ledger entry")
async def remove_entry(
    entry_id: str,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    await delete_ledger_entry(db, entry_id, current_user["id"])
    return success_response(None, "Entry deleted successfully")

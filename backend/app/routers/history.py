"""History router — /api/v1/history"""
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date

from app.database.connection import get_db
from app.dependencies.auth import get_current_active_user
from app.services import history_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/history", tags=["Historical Data & Dataset Import"])


@router.post("/import", summary="Import CSV, Excel, or JSON historical market dataset")
async def import_dataset(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Import historical mandi dataset (CSV, Excel .xlsx, or JSON).
    - Automatically cleans missing values & removes duplicate records
    - Normalizes crop & district names
    - Validates date formats
    - Inserts records into database
    - Auto-rebuilds FAISS RAG vector index for AI Assistant
    """
    contents = await file.read()
    result = await history_service.import_historical_dataset(
        db=db,
        file_bytes=contents,
        filename=file.filename,
        source_name=f"Upload by {current_user.get('full_name', 'User')}",
    )
    return success_response(result, "Dataset processed successfully")


@router.get("/search", summary="Search historical price records")
async def search_history(
    commodity: str = Query(..., description="Crop/Commodity name (e.g. Wheat, Onion)"),
    district: Optional[str] = Query(None, description="District filter"),
    start_date: Optional[date] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[date] = Query(None, description="YYYY-MM-DD"),
    limit: int = Query(100, ge=1, le=500),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    records = await history_service.search_historical_prices(
        db=db,
        commodity=commodity,
        district=district,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )
    return success_response(records, f"{len(records)} historical records found for {commodity}")

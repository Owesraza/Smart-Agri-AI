"""Analytics router — /api/v1/analytics"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime

from app.database.connection import get_db
from app.services.analytics_service import get_monthly_profit, get_crop_summary
from app.services.domain_service import get_ledger_summary
from app.services.market_service import compute_market_analytics
from app.dependencies.auth import get_current_active_user
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


@router.get("/market", summary="Get market analytics (Today Avg, Weekly Avg, Monthly Avg, EMA-7/14/30, Volatility)")
async def market_analytics_endpoint(
    crop: str = Query("Wheat", description="Crop/Commodity name"),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Computes real-time market analytics:
    - Today's Average Price
    - Weekly Average & Monthly Average
    - Highest & Lowest Prices
    - Price Volatility Score (%)
    - EMA-7, EMA-14, EMA-30 Trend Analysis
    """
    analytics = await compute_market_analytics(db, crop=crop)
    return success_response(analytics, f"Market analytics computed for {crop}")


@router.get("/monthly-profit", summary="Monthly income vs expenses for a given year")
async def monthly_profit(
    year: int = Query(default=None, description="Year (defaults to current year)"),
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    year = year or datetime.now().year
    data = await get_monthly_profit(db, current_user["id"], year)
    return success_response(data, f"Monthly profit for {year}")


@router.get("/yearly-profit", summary="Yearly profit summary across all years")
async def yearly_profit(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    current_year = datetime.now().year
    years_data = []
    for year in range(current_year - 2, current_year + 1):
        monthly = await get_monthly_profit(db, current_user["id"], year)
        total_income = sum(m["income"] for m in monthly)
        total_expenses = sum(m["expenses"] for m in monthly)
        years_data.append({
            "year": year,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_profit": total_income - total_expenses,
        })
    return success_response(years_data, "Yearly profit fetched")


@router.get("/crop-summary", summary="Crop-wise income breakdown")
async def crop_summary(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    data = await get_crop_summary(db, current_user["id"])
    return success_response(data, "Crop summary fetched")


@router.get("/ledger-summary", summary="Total income, expenses, profit summary")
async def ledger_summary_analytics(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    summary = await get_ledger_summary(db, current_user["id"])
    return success_response(summary, "Ledger summary fetched")


@router.get("/sales-summary", summary="Sales transaction count and revenue by crop")
async def sales_summary(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    crop_data = await get_crop_summary(db, current_user["id"])
    total_revenue = sum(c["total_income"] for c in crop_data)
    return success_response(
        {"total_revenue": total_revenue, "crops": crop_data, "total_crops": len(crop_data)},
        "Sales summary fetched"
    )

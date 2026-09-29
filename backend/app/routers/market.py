"""Market router — /api/v1/market"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date

from app.database.connection import get_db
from app.services import market_service
from app.utils.helpers import success_response

router = APIRouter(prefix="/api/v1/market", tags=["Market Intelligence"])


@router.get("/live", summary="Get live Agmarknet market prices")
async def get_live_prices(
    crop: Optional[str] = Query(None, description="Crop filter e.g. Wheat, Onion"),
    district: Optional[str] = Query(None, description="District filter"),
    state: Optional[str] = Query("Maharashtra", description="State filter"),
    db: AsyncSession = Depends(get_db),
):
    """Fetch live Agmarknet mandi market prices with filters."""
    prices = await market_service.get_live_market_prices(
        db=db,
        crop=crop,
        district=district or "Nashik",
        state=state,
    )
    return success_response(prices, f"{len(prices)} live market prices fetched")


@router.get("/prices", summary="Get current crop prices across mandis")
async def get_current_prices(
    crop: Optional[str] = Query(None, description="Filter by crop name"),
    district: Optional[str] = Query(None, description="Filter by district"),
    mandi: Optional[str] = Query(None, description="Filter by mandi name"),
    db: AsyncSession = Depends(get_db),
):
    prices = await market_service.get_live_market_prices(db=db, crop=crop, district=district or mandi)
    return success_response(prices, f"{len(prices)} prices fetched")


@router.get("/prices/history", summary="Get historical prices for a crop")
async def get_price_history(
    crop: str = Query("Wheat", description="Crop name"),
    db: AsyncSession = Depends(get_db),
):
    analytics = await market_service.compute_market_analytics(db=db, crop=crop)
    prices = await market_service.get_live_market_prices(db=db, crop=crop)
    return success_response({"crop": crop, "analytics": analytics, "prices": prices}, "Price history fetched")


@router.get("/prices/trend", summary="Get 4-week trailing historical price trends for graph")
async def get_price_trend_endpoint(
    district: Optional[str] = Query(None, description="City/district filter"),
    db: AsyncSession = Depends(get_db),
):
    trend_data = await market_service.get_market_trend_data(db=db, district=district)
    return success_response(trend_data, "Historical price trends fetched")


@router.get("/prices/advance-booking", summary="Calculate time-based advance booking price & discounts")
@router.get("/advance-discount", summary="Calculate time-based advance booking price alias")
async def get_advance_booking_pricing(
    base_price: float = Query(2400.0, ge=0, description="Base APMC price per quintal"),
    quantity: float = Query(100.0, ge=0, description="Quantity in quintals"),
    days_in_advance: int = Query(10, ge=0, alias="days", description="Lead time days in advance"),
):
    result = market_service.calculate_advance_booking_discount(
        base_price=base_price,
        quantity_quintals=quantity,
        days_in_advance=days_in_advance
    )
    return success_response(result, f"Advance booking pricing calculated for {days_in_advance} days lead time")


@router.get("/demand-clusters", summary="Get high-density order clusters to minimize farmer transport costs")
@router.get("/regional-demand", summary="Get regional demand clusters alias")
async def get_demand_clusters_endpoint(
    district: Optional[str] = Query("Nashik", description="Farmer district"),
    crop: Optional[str] = Query(None, description="Optional crop filter"),
    db: AsyncSession = Depends(get_db),
):
    res = await market_service.get_demand_clusters_and_transport_savings(db=db, district=district, crop=crop)
    return success_response(res, "Demand clusters and transport freight savings calculated")


@router.get("/mandis", summary="Get list of nearby APMC mandis")
async def get_mandis(
    district: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    prices = await market_service.get_live_market_prices(db=db, district=district or "Nashik")
    mandis = list({p["mandi"]: {"name": p["mandi"], "district": p["district"], "state": p["state"]} for p in prices}.values())
    return success_response(mandis, f"{len(mandis)} mandis found")


@router.get("/search", summary="Search crop prices by name")
async def search_crop(
    q: Optional[str] = Query(None, description="Crop name to search"),
    query: Optional[str] = Query(None, description="Alternative query param"),
    db: AsyncSession = Depends(get_db),
):
    search_term = q or query or ""
    results = await market_service.get_live_market_prices(db=db, crop=search_term if search_term else None)
    return success_response(results, f"{len(results)} results for '{search_term}'")


@router.get("/status", summary="Get AGMARKNET sync status and cache metadata")
async def get_market_status(
    db: AsyncSession = Depends(get_db),
):
    """Retrieve AGMARKNET synchronization status, cache metadata, and freshness."""
    status_meta = await market_service.get_market_intelligence_metadata(db=db)
    return success_response(status_meta, "AGMARKNET status retrieved")


@router.post("/sync", summary="Trigger manual AGMARKNET synchronization")
async def trigger_agmarknet_sync(
    db: AsyncSession = Depends(get_db),
):
    """Trigger manual on-demand fetch and caching of official AGMARKNET daily report."""
    from app.services.agmarknet_service import agmarknet_service
    result = await agmarknet_service.sync_agmarknet_market_prices(db=db)
    return success_response(result, result.get("message", "AGMARKNET synchronization completed"))

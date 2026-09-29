"""
Background Scheduler — APScheduler Integration.
Runs recurring background tasks:
- Market Prices update every 1 hour
- Weather Cache update every 30 minutes
- Analytics Refresh every 2 hours
"""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timezone, timedelta
from app.database.connection import AsyncSessionLocal

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def scheduled_market_update():
    """Background task: Synchronize official AGMARKNET mandi rates and refresh analytics."""
    logger.info("⏰ Scheduler: Running AGMARKNET market price sync...")
    try:
        from app.services.agmarknet_service import agmarknet_service
        from app.services.market_service import compute_market_analytics
        async with AsyncSessionLocal() as db:
            sync_res = await agmarknet_service.sync_agmarknet_market_prices(db)
            if sync_res.get("success"):
                logger.info(f"✅ Scheduler: AGMARKNET sync succeeded. {sync_res.get('records_received')} records received.")
            else:
                logger.warning(f"⚠️ Scheduler: AGMARKNET live fetch unavailable ({sync_res.get('message')}). Retaining existing AGMARKNET cache.")

            for crop in ["Wheat", "Onion", "Tomato", "Cotton", "Soybean", "Rice", "Maize", "Potato"]:
                await compute_market_analytics(db, crop=crop)
        logger.info("✅ Scheduler: Market price & analytics update complete")
    except Exception as e:
        logger.error(f"❌ Scheduler market update error: {e}")


async def scheduled_weather_update():
    """Background task: Refresh weather cache every 30 mins."""
    logger.info("⏰ Scheduler: Running 30-min weather cache update...")
    try:
        from app.services.weather_service import get_current_weather
        async with AsyncSessionLocal() as db:
            for loc in ["Nashik", "Pune", "Mumbai", "Aurangabad", "Latur", "Kolar", "Agra"]:
                await get_current_weather(db, location=loc)
        logger.info("✅ Scheduler: Weather cache update complete")
    except Exception as e:
        logger.error(f"❌ Scheduler weather update error: {e}")


async def scheduled_analytics_refresh():
    """Background task: Refresh analytics tables every 2 hours."""
    logger.info("⏰ Scheduler: Running 2-hour analytics refresh...")
    try:
        from app.services.market_service import compute_market_analytics
        async with AsyncSessionLocal() as db:
            for crop in ["Wheat", "Onion", "Tomato", "Cotton", "Soybean"]:
                await compute_market_analytics(db, crop=crop)
        logger.info("✅ Scheduler: Analytics refresh complete")
    except Exception as e:
        logger.error(f"❌ Scheduler analytics refresh error: {e}")


def start_scheduler():
    """Start APScheduler background jobs."""
    try:
        scheduler.add_job(scheduled_market_update, 'interval', hours=1, id="market_update_job", replace_existing=True)
        scheduler.add_job(scheduled_weather_update, 'interval', minutes=30, id="weather_update_job", replace_existing=True)
        scheduler.add_job(scheduled_analytics_refresh, 'interval', hours=2, id="analytics_refresh_job", replace_existing=True)

        # Trigger initial AGMARKNET synchronization shortly after startup
        init_run_time = datetime.now(timezone.utc) + timedelta(seconds=2)
        scheduler.add_job(scheduled_market_update, 'date', run_date=init_run_time, id="market_initial_sync", replace_existing=True)

        scheduler.start()
        logger.info("🚀 APScheduler background scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to start APScheduler: {e}")


def stop_scheduler():
    """Shutdown background scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("🛑 APScheduler background scheduler stopped")

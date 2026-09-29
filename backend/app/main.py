"""
SmartAgri AI – FastAPI Application Entry Point
Closed-Loop Agricultural Marketplace & Plot Manager API (SQL Engine)
"""
import logging
import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.config.settings import settings
from app.database.connection import init_db, close_db_connection
from app.middleware.logging_middleware import LoggingMiddleware
from app.services.scheduler import start_scheduler, stop_scheduler
from app.utils.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

# ── Routers ────────────────────────────────────────────────
from app.routers import (
    auth, users, plots, ledger, workflow, market, weather,
    analytics, dashboard, history, recommendations,
    buyer, marketplace, listings, requirements, offers,
    deals, payments, purchase_requests, chat, notifications, ratings, reports, ai_v2, contact
)
from app.routers import ai as ai_router


# ── Logging Configuration ──────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("smartagri")


# ── App Lifespan ───────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    # Initialize SQL Database (SQLite / PostgreSQL)
    try:
        await init_db()
    except Exception as e:
        logger.error(f"❌ SQL Database initialization error: {e}")

    # Initialize AI Engine (builds FAISS index, loads embedding model)
    try:
        from app.ai import ai_service
        await ai_service.initialize_ai()
    except Exception as e:
        logger.warning(f"⚠️  AI Engine initialization failed: {e}. AI routes will be limited.")

    # Start APScheduler Background Scheduler
    try:
        start_scheduler()
    except Exception as e:
        logger.warning(f"⚠️  APScheduler startup error: {e}")

    yield

    logger.info("🛑 Shutting down SmartAgri AI backend...")
    stop_scheduler()
    await close_db_connection()


# ── FastAPI App ────────────────────────────────────────────
app = FastAPI(
    title="SmartAgri AI Marketplace API",
    description="""
## SmartAgri AI – Closed-Loop Agricultural Marketplace & Plot Manager

AI-Powered Agricultural Marketplace & Decision Support API.

### Core Modules
- **Buyer & Farmer Accounts** – Roles: Farmer, Buyer, Admin with verified profiles & dashboards
- **Agricultural Marketplace** – Crop Listings for Sale & Buyer Requirements with AI Matching Engine
- **WhatsApp Click-to-Chat & Purchase Requests** – Direct WhatsApp buyer-farmer communication & deal pipeline
- **AI Negotiation Assistant** – Gemini 2.0 Flash fair price range guidance & confidence scoring
- **Real-Time Chat & WebSockets** – Direct buyer-farmer messaging & instant status updates
- **Deal Workflow & Auto Ledger** – Workflow timeline & automatic farmer ledger synchronization upon deal completion

### Database Engine
Powered by **SQLAlchemy Async** supporting **SQLite (local zero-config)**, **PostgreSQL**, and **MySQL**.
""",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ── Middleware ─────────────────────────────────────────────
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Exception Handlers ─────────────────────────────────────
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# ── Routers ────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(plots.router)
app.include_router(ledger.router)
app.include_router(workflow.router)
app.include_router(market.router)
app.include_router(weather.router)
app.include_router(analytics.router)
app.include_router(dashboard.router)
app.include_router(history.router)
app.include_router(recommendations.router)
app.include_router(buyer.router)
app.include_router(marketplace.router)
app.include_router(listings.router)
app.include_router(requirements.router)
app.include_router(offers.router)
app.include_router(deals.router)
app.include_router(payments.router)
app.include_router(purchase_requests.router)
app.include_router(chat.router)
app.include_router(notifications.router)
app.include_router(ratings.router)
app.include_router(reports.router)
app.include_router(contact.router)
app.include_router(ai_v2.router)
app.include_router(ai_router.router)


# ── Health Check ───────────────────────────────────────────
@app.get("/health", tags=["Health"], summary="Health check")
async def health():
    return {
        "status": "healthy",
        "database": "SQL (Active)",
        "scheduler": "APScheduler (Active)",
        "marketplace": "Active",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/", tags=["Root"], include_in_schema=False)
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME} Marketplace API",
        "version": settings.APP_VERSION,
        "database": "SQL Engine",
        "docs": "/docs",
    }

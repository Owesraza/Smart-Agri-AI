"""Register all routers — import convenience."""
from app.routers import (
    auth, users, plots, ledger, workflow, market, weather,
    analytics, dashboard, ai, history, recommendations,
    buyer, marketplace, listings, requirements, offers,
    deals, chat, notifications, ratings
)

__all__ = [
    "auth", "users", "plots", "ledger", "workflow", "market", "weather",
    "analytics", "dashboard", "ai", "history", "recommendations",
    "buyer", "marketplace", "listings", "requirements", "offers",
    "deals", "chat", "notifications", "ratings"
]

"""
AI Service — Public interface for all AI capabilities.
Initializes the vector store on startup and exposes clean methods.
"""
import logging
from typing import Optional, List, Dict

logger = logging.getLogger(__name__)

# Startup state
_ai_ready = False


async def initialize_ai():
    """Called on app startup to build FAISS index and load models."""
    global _ai_ready
    try:
        logger.info("🤖 Initializing SmartAgri AI Engine...")
        from app.ai.vector_store.faiss_store import build_index
        build_index()
        _ai_ready = True
        logger.info("✅ AI Engine ready")
    except Exception as e:
        logger.error(f"❌ AI initialization failed: {e}")
        _ai_ready = False


def is_ai_ready() -> bool:
    return _ai_ready


async def chat(
    question: str,
    crop: str = "General",
    location: str = "India",
    current_price: Optional[float] = None,
    historical_prices: Optional[List[float]] = None,
    language: str = "English",
    user_id: Optional[str] = None,
) -> Dict:
    """Main AI chat entry point — runs full pipeline."""
    if not _ai_ready:
        return {
            "recommendation": "CONSULT_EXPERT",
            "confidence": 0,
            "answer": "AI engine is initializing. Please try again in a moment.",
            "error": "AI_NOT_READY",
        }

    from app.ai.agents.farm_agent import run_ai_pipeline
    result = await run_ai_pipeline(
        question=question,
        crop=crop,
        location=location,
        current_price=current_price,
        historical_prices=historical_prices,
        language=language,
    )

    logger.info(
        f"[AI Chat] user={user_id} crop={crop} intent={result.get('intent')} "
        f"rec={result.get('recommendation')} conf={result.get('confidence')}% "
        f"time={result.get('execution_time_ms')}ms"
    )
    return result


async def analyze_profit_data(
    ledger_entries: List[Dict],
    crop: Optional[str] = None,
) -> Dict:
    """Analyze ledger data and return profit intelligence."""
    from app.ai.utils.profit_analyzer import analyze_profit
    return analyze_profit(ledger_entries, crop)


async def get_workflow(
    crop: str,
    harvest_date: Optional[str] = None,
    quantity: Optional[float] = None,
    mandi: Optional[str] = None,
    recommendation: str = "SELL",
) -> List[Dict]:
    """Generate harvest-to-sale workflow."""
    from app.ai.utils.workflow_generator import generate_workflow
    return generate_workflow(crop, harvest_date, quantity, mandi, recommendation)


async def get_market_trend(prices: List[float]) -> Dict:
    """Run EMA trend analysis on price series."""
    from app.ai.forecasting.ema import analyze_trend
    return analyze_trend(prices)

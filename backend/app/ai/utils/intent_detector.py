"""
Deterministic Intent Detector
Classifies farmer questions into predefined intents using keyword matching.
Falls back to Gemini for ambiguous cases.
"""
import re
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Intent keyword map — ordered by priority
INTENT_PATTERNS = {
    "PRICE_QUERY": [
        r"\bprice\b", r"\brate\b", r"\bbhav\b", r"\bdam\b",
        r"\bhow much\b", r"\bcurrent price\b", r"\btoday.*price\b",
        r"\bprice.*today\b", r"\bmarket rate\b",
    ],
    "SELL_ADVICE": [
        r"\bsell\b", r"\bwhen.*sell\b", r"\bsell.*now\b", r"\bshould i sell\b",
        r"\bbechna\b", r"\bbechu\b", r"\bselling\b", r"\bsale\b",
        r"\bgood time to sell\b", r"\bright time\b",
    ],
    "BEST_MARKET": [
        r"\bbest mandi\b", r"\bwhich market\b", r"\bwhich mandi\b",
        r"\bnearby market\b", r"\bapmc\b", r"\bwhere.*sell\b",
        r"\bmarket.*best\b", r"\bbetter price.*mandi\b",
    ],
    "WEATHER_IMPACT": [
        r"\bweather\b", r"\brain\b", r"\bmonsoon\b", r"\bdrought\b",
        r"\bflood\b", r"\btemperature\b", r"\bbarish\b", r"\bsookha\b",
        r"\bel nino\b", r"\bclimate\b",
    ],
    "PROFIT_ANALYSIS": [
        r"\bprofit\b", r"\bloss\b", r"\bincome\b", r"\bexpense\b",
        r"\bearning\b", r"\blaabh\b", r"\bkharcha\b", r"\bnet.*profit\b",
        r"\bhow much.*earn\b", r"\bfinancial\b",
    ],
    "WORKFLOW_PLANNING": [
        r"\bworkflow\b", r"\bplan\b", r"\bsteps\b", r"\bschedule\b",
        r"\bharvest.*plan\b", r"\bwhat.*do\b", r"\btask\b",
        r"\bday.*day\b", r"\btimeline\b", r"\bprocess\b",
    ],
    "MARKET_TREND": [
        r"\btrend\b", r"\bgoing up\b", r"\bgoing down\b", r"\buptrend\b",
        r"\bdowntrend\b", r"\bprice.*rising\b", r"\bprice.*falling\b",
        r"\bema\b", r"\bmoving average\b", r"\bforecast\b",
    ],
    "STORAGE_ADVICE": [
        r"\bstore\b", r"\bstorage\b", r"\bwait\b", r"\bhold\b",
        r"\bgodown\b", r"\bwhere.*store\b", r"\bhow long.*store\b",
        r"\bsafely.*store\b",
    ],
    "GENERAL_AGRICULTURE": [],  # Default/fallback
}


def detect_intent(question: str) -> Dict:
    """
    Classify a farmer's question into a predefined intent.
    Returns: {'intent': str, 'confidence': int, 'method': str}
    """
    question_lower = question.lower().strip()
    scores = {}

    for intent, patterns in INTENT_PATTERNS.items():
        if not patterns:
            continue
        matches = sum(1 for p in patterns if re.search(p, question_lower))
        if matches > 0:
            scores[intent] = matches

    if scores:
        best_intent = max(scores, key=scores.get)
        confidence = min(95, 60 + scores[best_intent] * 15)
        logger.info(f"🎯 Intent detected: {best_intent} (confidence={confidence}%) for: '{question[:50]}'")
        return {
            "intent": best_intent,
            "confidence": confidence,
            "method": "keyword_matching",
            "all_scores": scores,
        }

    # Default fallback
    logger.info(f"🎯 Intent fallback: GENERAL_AGRICULTURE for: '{question[:50]}'")
    return {
        "intent": "GENERAL_AGRICULTURE",
        "confidence": 40,
        "method": "fallback",
        "all_scores": {},
    }

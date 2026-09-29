"""
Recommendation Engine
Generates SELL / WAIT / STORE recommendations with confidence, reasoning, advantages, and risks.
Uses EMA trend + price level + crop-specific rules.
"""
import logging
from typing import Dict, List, Optional
from datetime import date, timedelta

logger = logging.getLogger(__name__)

# Crops that MUST be sold quickly (perishable)
PERISHABLE_CROPS = {"tomato", "onion", "leafy greens", "spinach", "coriander",
                    "okra", "brinjal", "cauliflower", "cabbage", "potato"}

# Crops that store well
STORABLE_CROPS = {"wheat", "rice", "cotton", "soybean", "maize", "chickpea",
                  "lentil", "mustard", "groundnut"}

# MSP reference prices (2024-25)
MSP_PRICES = {
    "wheat": 2275, "rice": 2300, "cotton": 6620, "soybean": 4892,
    "maize": 2225, "bajra": 2625, "jowar": 3371, "groundnut": 6783,
    "mustard": 5950, "chickpea": 5440,
}


def generate_recommendation(
    crop: str,
    current_price: float,
    trend_data: Dict,
    historical_prices: Optional[List[float]] = None,
    harvest_date: Optional[str] = None,
    quantity: Optional[float] = None,
) -> Dict:
    """
    Core recommendation engine.
    Returns full structured recommendation with confidence, reasoning, risks.
    """
    crop_lower = crop.lower()
    trend = trend_data.get("trend", "UNKNOWN")
    trend_confidence = trend_data.get("confidence", 50)
    price_change_7d = trend_data.get("price_change_7d_pct", 0) or 0
    ema7 = trend_data.get("ema7")
    ema14 = trend_data.get("ema14")

    msp = MSP_PRICES.get(crop_lower)
    is_perishable = crop_lower in PERISHABLE_CROPS
    is_storable = crop_lower in STORABLE_CROPS

    # ── Core decision logic ────────────────────────────────
    recommendation = "WAIT"
    confidence = 50
    reasons = []
    advantages = []
    risks = []
    action = ""

    # Rule 1: Perishable crops — always sell
    if is_perishable:
        recommendation = "SELL"
        confidence = 92
        reasons.append(f"{crop} is a perishable crop. Delays cause quality loss and price drop.")
        advantages.append("Preserve quality and avoid total loss")
        advantages.append("Get current market price before deterioration")
        risks.append("Waiting even 2-3 days risks 30-50% quality loss")
        action = f"Transport {crop} to nearest mandi within 24-48 hours. Do not delay."

    # Rule 2: Price well above MSP — good time to sell
    elif msp and current_price > msp * 1.15:
        premium = round(((current_price - msp) / msp) * 100, 1)
        if trend == "UPTREND":
            recommendation = "SELL"
            confidence = min(95, 75 + trend_confidence // 5)
            reasons.append(f"Price is {premium}% above MSP (₹{msp}/quintal) and market is in UPTREND.")
            advantages.append(f"Excellent price — {premium}% premium over MSP")
            advantages.append("Uptrend may reverse soon — secure profit now")
            risks.append("Prices could rise further if trend continues")
            action = f"Sell 60-70% of your stock now. Hold remaining 30-40% to benefit from continued uptrend."
        elif trend == "STABLE":
            recommendation = "SELL"
            confidence = 78
            reasons.append(f"Price is {premium}% above MSP. Market is stable — good time to exit.")
            advantages.append("Secure good profit above MSP")
            risks.append("Stable market may not offer significantly better prices")
            action = f"Sell your full stock now. Price is attractive."

    # Rule 3: Strong uptrend — consider waiting
    elif trend == "UPTREND" and trend_confidence >= 70 and is_storable:
        recommendation = "WAIT"
        confidence = min(85, trend_confidence)
        reasons.append(f"Strong uptrend detected. EMA-7 ({ema7}) > EMA-14 ({ema14}). Prices rising {price_change_7d:+.1f}% in 7 days.")
        advantages.append("Waiting 7-14 more days could yield 5-10% higher price")
        advantages.append("Trend supported by multiple EMA signals")
        risks.append("Trend could reverse unexpectedly")
        risks.append("Storage costs accumulate over time")
        action = f"Wait 7-10 days. Monitor price daily. Set a target price — if reached, sell immediately."

    # Rule 4: Downtrend — sell now before further fall
    elif trend == "DOWNTREND":
        recommendation = "SELL"
        confidence = min(88, trend_confidence + 5)
        reasons.append(f"Downtrend detected. Prices falling {price_change_7d:+.1f}% in 7 days. EMA-7 < EMA-14.")
        advantages.append("Avoid further price erosion")
        advantages.append("Free up storage space and recover capital")
        risks.append("Selling in downtrend may not recover full cost")
        action = f"Sell your stock as soon as possible. Each day of delay may cost ₹{round(current_price * 0.02, 0)}/quintal in losses."

    # Rule 5: Price below MSP + storable crop — store for MSP procurement
    elif msp and current_price < msp and is_storable:
        recommendation = "STORE"
        confidence = 80
        reasons.append(f"Current price ₹{current_price} is below MSP of ₹{msp}. Register for government procurement.")
        advantages.append(f"Government MSP guarantees ₹{msp}/quintal — {round(msp - current_price)} more than current price")
        advantages.append("Store safely for 2-4 months and sell to FCI/NAFED")
        risks.append("Procurement availability varies by state")
        risks.append("Storage requires proper moisture control")
        action = f"Visit your nearest APMC/procurement center, register for MSP procurement. Store {crop} in dry conditions below 12% moisture."

    # Default: Stable market, insufficient data
    else:
        recommendation = "WAIT"
        confidence = 45
        reasons.append("Market conditions are stable. No strong signal to sell or store yet.")
        advantages.append("Waiting for clearer signal reduces decision risk")
        risks.append("Opportunity cost if prices start falling")
        action = "Monitor mandi prices daily for 3-5 days before making a decision."

    logger.info(f"💡 Recommendation: {recommendation} ({confidence}%) for {crop} @ ₹{current_price}")

    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "market_trend": trend,
        "reason": " ".join(reasons),
        "advantages": advantages,
        "risks": risks,
        "suggested_action": action,
        "price_vs_msp": {
            "msp": msp,
            "current": current_price,
            "premium_pct": round(((current_price - msp) / msp) * 100, 1) if msp else None,
        },
        "trend_data": {
            "ema7": ema7,
            "ema14": ema14,
            "price_change_7d_pct": price_change_7d,
        },
        "is_perishable": is_perishable,
        "is_storable": is_storable,
    }

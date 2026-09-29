"""
EMA (Exponential Moving Average) Calculator
Computes EMA-7, EMA-14, EMA-30 and detects market trends.
"""
import pandas as pd
import numpy as np
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def calculate_ema(prices: List[float], period: int) -> List[float]:
    """Calculate EMA for a given period using pandas exponential moving average."""
    if not prices:
        return []
    s = pd.Series(prices, dtype=float)
    effective_period = max(2, min(period, len(prices)))
    ema = s.ewm(span=effective_period, adjust=False).mean()
    return ema.tolist()


def analyze_trend(prices: List[float]) -> Dict:
    """
    Full trend analysis using EMA-7, EMA-14, EMA-30.
    Input: list of prices (oldest → newest)
    """
    if not prices or len(prices) < 3:
        return {
            "trend": "UNKNOWN",
            "confidence": 0,
            "ema7": None, "ema14": None, "ema30": None,
            "price_change_7d": None,
            "price_change_30d": None,
            "signal": "INSUFFICIENT_DATA",
        }

    ema7_series = calculate_ema(prices, 7)
    ema14_series = calculate_ema(prices, 14)
    ema30_series = calculate_ema(prices, 30)

    current_price = prices[-1]
    ema7 = ema7_series[-1]
    ema14 = ema14_series[-1]
    ema30 = ema30_series[-1] if ema30_series[-1] else None

    # Price changes
    price_change_7d = None
    price_change_30d = None
    if len(prices) >= 7:
        price_change_7d = round(((current_price - prices[-7]) / prices[-7]) * 100, 2)
    if len(prices) >= 30:
        price_change_30d = round(((current_price - prices[-30]) / prices[-30]) * 100, 2)
    elif len(prices) > 1:
        price_change_30d = round(((current_price - prices[0]) / prices[0]) * 100, 2)

    # Trend detection logic
    trend = "STABLE"
    confidence = 50
    signal = "HOLD"

    if ema7 and ema14:
        if ema7 > ema14:
            # EMA7 above EMA14 = short-term bullish
            if ema30 and ema14 > ema30:
                # All EMAs aligned upward = strong uptrend
                trend = "UPTREND"
                confidence = 85
                signal = "SELL_SOON"
            else:
                trend = "UPTREND"
                confidence = 65
                signal = "MONITOR"
        elif ema7 < ema14:
            # EMA7 below EMA14 = short-term bearish
            if ema30 and ema14 < ema30:
                trend = "DOWNTREND"
                confidence = 80
                signal = "SELL_NOW"
            else:
                trend = "DOWNTREND"
                confidence = 60
                signal = "WAIT"
        else:
            trend = "STABLE"
            confidence = 55
            signal = "HOLD"

    # Boost confidence if price_change supports EMA signal
    if price_change_7d is not None:
        if trend == "UPTREND" and price_change_7d > 3:
            confidence = min(95, confidence + 10)
        elif trend == "DOWNTREND" and price_change_7d < -3:
            confidence = min(95, confidence + 10)
        elif abs(price_change_7d) < 1:
            trend = "STABLE"
            confidence = min(confidence, 60)

    logger.info(f"📈 Trend analysis: {trend} (conf={confidence}%) | EMA7={ema7 or 'N/A'} EMA14={ema14 or 'N/A'}")

    return {
        "trend": trend,
        "confidence": confidence,
        "signal": signal,
        "current_price": current_price,
        "ema7": round(ema7, 2) if ema7 else None,
        "ema14": round(ema14, 2) if ema14 else None,
        "ema30": round(ema30, 2) if ema30 else None,
        "price_change_7d_pct": price_change_7d,
        "price_change_30d_pct": price_change_30d,
        "data_points": len(prices),
    }


def get_trend_description(trend_data: Dict) -> str:
    """Human-readable trend description for the prompt context."""
    trend = trend_data.get("trend", "UNKNOWN")
    conf = trend_data.get("confidence", 0)
    change = trend_data.get("price_change_7d_pct")
    ema7 = trend_data.get("ema7")
    ema14 = trend_data.get("ema14")

    if trend == "UNKNOWN":
        return "Insufficient price history to determine trend."

    direction = "rising" if trend == "UPTREND" else ("falling" if trend == "DOWNTREND" else "stable")
    change_str = f" ({change:+.1f}% in last 7 days)" if change is not None else ""

    return (
        f"Market is in {trend} — prices are {direction}{change_str}. "
        f"EMA-7 = {ema7}, EMA-14 = {ema14}. "
        f"Trend confidence: {conf}%."
    )


def analyze_trend_with_historical_yoy(
    prices: List[float],
    previous_year_prices: Optional[List[float]] = None
) -> Dict:
    """
    Dual-Horizon Multi-Timeframe Trend & Seasonality Analysis:
    Combines Short-Term EMA 7 / 14 / 30 with Previous Year Historical YoY Seasonality (EMA 365 Days Baseline).
    """
    base_res = analyze_trend(prices)
    
    yoy_change_pct = None
    yoy_trend = "UNKNOWN"
    prev_year_avg = None
    
    if previous_year_prices and len(previous_year_prices) > 0:
        prev_year_avg = round(float(np.mean(previous_year_prices)), 2)
        current_p = prices[-1] if prices else 0.0
        if prev_year_avg > 0:
            yoy_change_pct = round(((current_p - prev_year_avg) / prev_year_avg) * 100, 2)
            if yoy_change_pct > 5:
                yoy_trend = "HIGHER_THAN_LAST_YEAR"
            elif yoy_change_pct < -5:
                yoy_trend = "LOWER_THAN_LAST_YEAR"
            else:
                yoy_trend = "SEASONALLY_ALIGNED"
    else:
        prev_year_avg = None
        yoy_change_pct = None
        yoy_trend = "UNAVAILABLE"

    base_res["previous_year_avg_price"] = prev_year_avg
    base_res["yoy_change_pct"] = yoy_change_pct
    base_res["yoy_trend"] = yoy_trend
    if yoy_trend == "UNAVAILABLE":
        base_res["seasonality_summary"] = "Previous-year comparison unavailable"
    else:
        base_res["seasonality_summary"] = (
            f"Year-over-Year (YoY) Analysis: Current Price (₹{prices[-1] if prices else 0}) is "
            f"{'+' if (yoy_change_pct or 0) >= 0 else ''}{yoy_change_pct}% compared to previous year APMC baseline (₹{prev_year_avg}/Qtl)."
        )
    return base_res

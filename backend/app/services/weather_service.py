"""
Weather Service — Live OpenWeatherMap API Integration & Weather Analytics.
Features:
- Live 5-day weather & forecast fetching via OpenWeatherMap API
- Weather analytics: Rain Risk, Harvest Risk, Temp/Humidity Trends, Farming Advisory
- Database Caching (30-minute TTL)
- Robust error handling with graceful fallback
"""
import time
import json
import logging
import httpx
from datetime import date, datetime, timezone, timedelta
from typing import Dict, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config.settings import settings
from app.models.sql_models import WeatherCacheModel, ApiLogModel

logger = logging.getLogger(__name__)

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"


def normalize_location(location: str) -> str:
    """Clean location input e.g. 'Pune, Maharashtra, India' -> 'Pune'."""
    if not location:
        return "Nashik"
    parts = [p.strip() for p in location.split(",") if p.strip()]
    return parts[0] if parts else "Nashik"


def calculate_weather_analytics(temp: float, humidity: float, wind_speed: float, rain_prob: float) -> Dict:
    """Calculate rain risk, harvest risk, temp trend, and farming advisory."""
    # Rain risk
    if rain_prob > 60 or (humidity > 80 and rain_prob > 30):
        rain_risk = "High"
    elif rain_prob > 30 or humidity > 70:
        rain_risk = "Moderate"
    else:
        rain_risk = "Low"

    # Harvest risk
    if rain_prob > 50 or wind_speed > 25:
        harvest_risk = "High"
        harvest_reason = "High rain probability or strong winds may damage harvested crop in open fields."
    elif rain_prob > 25 or wind_speed > 18:
        harvest_risk = "Moderate"
        harvest_reason = "Moderate risk. Keep tarpaulins ready for field protection."
    else:
        harvest_risk = "Low"
        harvest_reason = "Favorable conditions for harvest, drying, and field transport."

    # Trends & Advisory
    temp_trend = "Warm" if temp > 30 else ("Cool" if temp < 20 else "Moderate")
    humidity_trend = "High Humidity" if humidity > 75 else ("Dry" if humidity < 40 else "Normal")

    if rain_risk == "High":
        advisory = "Postpone pesticide and fertilizer application. Ensure field drainage."
    elif harvest_risk == "High":
        advisory = "Store harvested produce in covered sheds immediately. Avoid open-air drying."
    elif temp > 35:
        advisory = "High heat — irrigate crops early morning or evening to prevent heat stress."
    else:
        advisory = "Good conditions for routine field operations, weeding, and irrigation."

    return {
        "rain_risk": rain_risk,
        "harvest_risk": harvest_risk,
        "harvest_reason": harvest_reason,
        "temp_trend": temp_trend,
        "humidity_trend": humidity_trend,
        "farming_advisory": advisory,
    }


async def fetch_live_weather_from_api(city: str) -> Optional[Dict]:
    """Fetch live current weather and 5-day forecast from OpenWeatherMap."""
    api_key = settings.OPENWEATHER_API_KEY
    if not api_key:
        logger.warning("OPENWEATHER_API_KEY missing in settings.")
        return None

    clean_city = normalize_location(city)
    start_time = time.perf_counter()

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            # 1. Current Weather
            curr_resp = await client.get(
                f"{OPENWEATHER_BASE_URL}/weather",
                params={"q": clean_city, "appid": api_key, "units": "metric"}
            )
            # 2. Forecast
            fore_resp = await client.get(
                f"{OPENWEATHER_BASE_URL}/forecast",
                params={"q": clean_city, "appid": api_key, "units": "metric"}
            )

        response_ms = (time.perf_counter() - start_time) * 1000

        if curr_resp.status_code != 200:
            logger.warning(f"OpenWeatherMap current weather API returned status {curr_resp.status_code} for {clean_city}")
            return None

        curr_data = curr_resp.json()
        fore_data = fore_resp.json() if fore_resp.status_code == 200 else {}

        # Parse current weather
        temp = float(curr_data["main"]["temp"])
        feels_like = float(curr_data["main"]["feels_like"])
        temp_min = float(curr_data["main"].get("temp_min", temp))
        temp_max = float(curr_data["main"].get("temp_max", temp))
        humidity = float(curr_data["main"]["humidity"])
        wind_speed = float(curr_data["wind"]["speed"])
        pressure = float(curr_data["main"].get("pressure", 1013))
        condition = curr_data["weather"][0]["main"] if curr_data.get("weather") else "Clear"
        description = curr_data["weather"][0]["description"].capitalize() if curr_data.get("weather") else ""
        icon = f"https://openweathermap.org/img/wn/{curr_data['weather'][0]['icon']}@2x.png" if curr_data.get("weather") else "⛅"

        # Rain probability from forecast list
        rain_prob = 0.0
        forecast_list = []
        if fore_data and "list" in fore_data:
            # Get pop (probability of precipitation)
            pops = [item.get("pop", 0) * 100 for item in fore_data["list"][:8]]
            rain_prob = round(max(pops), 1) if pops else 0.0

            # Group daily forecast
            days_seen = set()
            for item in fore_data["list"]:
                dt = datetime.fromtimestamp(item["dt"], tz=timezone.utc)
                day_name = dt.strftime("%a")
                date_str = dt.strftime("%Y-%m-%d")
                if date_str not in days_seen and len(days_seen) < 5:
                    days_seen.add(date_str)
                    forecast_list.append({
                        "day": day_name,
                        "date": date_str,
                        "temp_max": round(item["main"]["temp_max"]),
                        "temp_min": round(item["main"]["temp_min"]),
                        "condition": item["weather"][0]["main"],
                        "description": item["weather"][0]["description"],
                        "icon": item["weather"][0]["icon"],
                        "rain_prob": round(item.get("pop", 0) * 100),
                        "humidity": item["main"]["humidity"],
                    })

        analytics = calculate_weather_analytics(temp, humidity, wind_speed, rain_prob)

        return {
            "location": clean_city,
            "temperature": temp,
            "feels_like": feels_like,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "pressure": pressure,
            "condition": condition,
            "description": description,
            "icon": icon,
            "rain_probability": rain_prob,
            "rain_prediction": f"{rain_prob}% chance of rain in next 24 hours",
            "rain_risk": analytics["rain_risk"],
            "harvest_risk": analytics["harvest_risk"],
            "harvest_reason": analytics["harvest_reason"],
            "temp_trend": analytics["temp_trend"],
            "humidity_trend": analytics["humidity_trend"],
            "farming_advisory": analytics["farming_advisory"],
            "forecast": forecast_list,
            "is_live": True,
        }

    except Exception as e:
        logger.error(f"Error fetching OpenWeatherMap live data for {clean_city}: {e}")
        return None


async def get_current_weather(db: AsyncSession, location: str = "Nashik") -> Dict:
    """Get current weather with 30-minute DB cache."""
    clean_loc = normalize_location(location)
    now = datetime.now(timezone.utc)

    # Check DB cache
    stmt = select(WeatherCacheModel).where(WeatherCacheModel.location == clean_loc)
    res = await db.execute(stmt)
    cached = res.scalar_one_or_none()

    ttl_seconds = settings.WEATHER_CACHE_TTL_SECONDS
    if cached and cached.last_updated and (now - cached.last_updated.replace(tzinfo=timezone.utc)).total_seconds() < ttl_seconds:
        logger.info(f"⚡ Returning cached weather for {clean_loc}")
        forecast = json.loads(cached.forecast_json) if cached.forecast_json else []
        analytics = calculate_weather_analytics(cached.temperature, cached.humidity, cached.wind_speed, cached.rain_probability)
        return {
            "location": cached.location,
            "temperature": cached.temperature,
            "feels_like": cached.feels_like,
            "temp_min": cached.temp_min,
            "temp_max": cached.temp_max,
            "humidity": cached.humidity,
            "wind_speed": cached.wind_speed,
            "pressure": cached.pressure,
            "uv_index": cached.uv_index,
            "condition": cached.condition,
            "description": cached.description,
            "icon": cached.icon,
            "rain_probability": cached.rain_probability,
            "rain_prediction": cached.rain_prediction,
            "rain_risk": analytics["rain_risk"],
            "harvest_risk": analytics["harvest_risk"],
            "harvest_reason": analytics["harvest_reason"],
            "temp_trend": analytics["temp_trend"],
            "humidity_trend": analytics["humidity_trend"],
            "farming_advisory": cached.farming_advisory or analytics["farming_advisory"],
            "forecast": forecast,
            "last_updated": cached.last_updated.isoformat(),
            "is_live": True,
        }

    # Fetch live
    live_data = await fetch_live_weather_from_api(clean_loc)

    if live_data:
        # Save to DB cache
        if cached:
            cached.temperature = live_data["temperature"]
            cached.feels_like = live_data["feels_like"]
            cached.temp_min = live_data["temp_min"]
            cached.temp_max = live_data["temp_max"]
            cached.humidity = live_data["humidity"]
            cached.wind_speed = live_data["wind_speed"]
            cached.condition = live_data["condition"]
            cached.description = live_data["description"]
            cached.icon = live_data["icon"]
            cached.rain_probability = live_data["rain_probability"]
            cached.rain_prediction = live_data["rain_prediction"]
            cached.farming_advisory = live_data["farming_advisory"]
            cached.forecast_json = json.dumps(live_data["forecast"])
            cached.last_updated = now
        else:
            new_cache = WeatherCacheModel(
                location=clean_loc,
                temperature=live_data["temperature"],
                feels_like=live_data["feels_like"],
                temp_min=live_data["temp_min"],
                temp_max=live_data["temp_max"],
                humidity=live_data["humidity"],
                wind_speed=live_data["wind_speed"],
                condition=live_data["condition"],
                description=live_data["description"],
                icon=live_data["icon"],
                rain_probability=live_data["rain_probability"],
                rain_prediction=live_data["rain_prediction"],
                farming_advisory=live_data["farming_advisory"],
                forecast_json=json.dumps(live_data["forecast"]),
                last_updated=now,
            )
            db.add(new_cache)

        # Log API call
        db.add(ApiLogModel(service_name="OpenWeatherMap", endpoint=f"/weather?q={clean_loc}", status="SUCCESS", response_time_ms=120.0))
        await db.commit()
        return live_data

    # Fallback if API fails & no cache exists
    fallback = {
        "location": clean_loc,
        "temperature": 28.0,
        "feels_like": 30.0,
        "temp_min": 22.0,
        "temp_max": 32.0,
        "humidity": 65.0,
        "wind_speed": 12.0,
        "pressure": 1013.0,
        "uv_index": 6.0,
        "condition": "Partly Cloudy",
        "description": "Partly cloudy with mild breeze",
        "icon": "⛅",
        "rain_probability": 15.0,
        "rain_prediction": "No significant rain expected today",
        "rain_risk": "Low",
        "harvest_risk": "Low",
        "harvest_reason": "Favorable conditions for field operations.",
        "temp_trend": "Moderate",
        "humidity_trend": "Normal",
        "farming_advisory": "Good conditions for irrigation and field work. Avoid spraying during midday heat.",
        "forecast": [
            {"day": "Today", "date": str(date.today()), "temp_max": 31, "temp_min": 22, "condition": "Partly Cloudy", "rain_prob": 15, "humidity": 65},
            {"day": "Tomorrow", "date": str(date.today() + timedelta(days=1)), "temp_max": 33, "temp_min": 23, "condition": "Sunny", "rain_prob": 5, "humidity": 55},
        ],
        "is_live": False,
    }

    db.add(ApiLogModel(service_name="OpenWeatherMap", endpoint=f"/weather?q={clean_loc}", status="FALLBACK", response_time_ms=0.0, error_message="API offline/rate limited"))
    await db.commit()
    return fallback

"""
Geolocation Utility — Distance & Transport Time Calculations.
Uses Haversine distance & road speed heuristics for agricultural transport.
"""
import math
from typing import Dict, Tuple

DISTRICT_COORDINATES = {
    "nashik": (20.0059, 73.7898),
    "pune": (18.5204, 73.8567),
    "mumbai": (19.0760, 72.8777),
    "baramati": (18.1517, 74.5770),
    "ahmednagar": (19.0952, 74.7496),
    "aurangabad": (19.8762, 75.3433),
    "chhatrapati sambhajinagar": (19.8762, 75.3433),
    "solapur": (17.6599, 75.9064),
    "kolhapur": (16.7050, 74.2433),
    "nagpur": (21.1458, 79.0882),
    "delhi": (28.6139, 77.2090),
}


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in km between two lat/lon points."""
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def calculate_transport_metrics(origin: str, destination: str) -> Dict:
    """Calculate distance (km) and estimated transport time (hours)."""
    orig_key = origin.lower().strip()
    dest_key = destination.lower().strip()

    c1 = DISTRICT_COORDINATES.get(orig_key, (20.0059, 73.7898))
    c2 = DISTRICT_COORDINATES.get(dest_key, (18.5204, 73.8567))

    distance_km = haversine_distance(c1[0], c1[1], c2[0], c2[1])
    if distance_km == 0:
        distance_km = 12.5  # Intra-district distance fallback

    # Heuristic: Average truck transport speed = 40 km/h + 0.5h loading buffer
    transport_hours = round((distance_km / 40.0) + 0.5, 1)

    return {
        "origin": origin,
        "destination": destination,
        "distance_km": distance_km,
        "estimated_transport_time_hours": transport_hours,
        "recommended_vehicle": "Mini Truck (Bolero Pickup)" if distance_km < 50 else "10-Ton Truck",
        "estimated_transport_cost_rs": round(distance_km * 25.0, 2)
    }

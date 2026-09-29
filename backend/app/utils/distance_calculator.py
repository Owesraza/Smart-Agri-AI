"""
District Distance & Transport Cost Calculator for Smart Agri AI.
Calculates approximate geographical distance (in km) between Maharashtra districts using centroid coordinates,
and computes estimated freight costs and net realizations.
"""
import math
from datetime import date, timedelta
from typing import Dict, Optional, Tuple

# Centroid coordinates (latitude, longitude) for major agricultural districts in Maharashtra
DISTRICT_COORDINATES: Dict[str, Tuple[float, float]] = {
    "nashik": (19.9975, 73.7898),
    "lasalgaon": (20.1472, 74.2272),
    "pune": (18.5204, 73.8567),
    "mumbai": (19.0760, 72.8777),
    "solapur": (17.6599, 75.9064),
    "ahmednagar": (19.0948, 74.7480),
    "latur": (18.4088, 76.5604),
    "aurangabad": (19.8762, 75.3433),
    "chhatrapati sambhajinagar": (19.8762, 75.3433),
    "kolhapur": (16.7050, 74.2433),
    "nagpur": (21.1458, 79.0882),
    "jalgaon": (21.0077, 75.5626),
    "dhule": (20.9042, 74.7749),
    "satara": (17.6805, 74.0183),
    "sangli": (16.8524, 74.5815),
    "amravati": (20.9374, 77.7796),
    "nanded": (19.1383, 77.3210),
    "thane": (19.2183, 72.9781),
    "raigad": (18.5158, 73.1822),
    "palghar": (19.6936, 72.7655),
    "ratnagiri": (16.9902, 73.3120),
    "sindhudurg": (16.1264, 73.6841),
    "beed": (18.9891, 75.7601),
    "osmanabad": (18.2070, 76.1684),
    "dharashiv": (18.2070, 76.1684),
    "nandurbar": (21.3703, 74.2404),
    "buldhana": (20.5292, 76.1843),
    "washim": (20.1009, 77.1352),
    "akola": (20.7002, 77.0082),
    "yavatmal": (20.3888, 78.1204),
    "wardha": (20.7453, 78.6022),
    "chandrapur": (19.9615, 79.2961),
    "gadchiroli": (20.1849, 80.0035),
    "bhandara": (21.1704, 79.6543),
    "gondia": (21.4604, 80.1961),
    "hingoli": (19.7173, 77.1477),
    "parbhani": (19.2608, 76.7800),
}


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the Great Circle (Haversine) distance between two points in km."""
    R = 6371.0  # Radius of Earth in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    # Multiply by 1.25 to approximate actual road travel distance over direct air distance
    road_distance = R * c * 1.25
    return round(road_distance, 1)


def get_district_distance(origin_district: str, destination_district: str) -> Optional[float]:
    """Get approximate road distance in km between two districts."""
    orig_clean = origin_district.strip().lower() if origin_district else "nashik"
    dest_clean = destination_district.strip().lower() if destination_district else "nashik"

    # Match exact or partial district names
    orig_coords = None
    dest_coords = None

    for name, coords in DISTRICT_COORDINATES.items():
        if name in orig_clean or orig_clean in name:
            orig_coords = coords
            break

    for name, coords in DISTRICT_COORDINATES.items():
        if name in dest_clean or dest_clean in name:
            dest_coords = coords
            break

    if not orig_coords or not dest_coords:
        return None

    if orig_clean == dest_clean:
        return 5.0  # Intra-district local transport ~ 5 km average

    return haversine_distance(orig_coords[0], orig_coords[1], dest_coords[0], dest_coords[1])


def calculate_transport_realization(
    offered_price_per_qtl: float,
    quantity_qtl: float,
    origin_district: str,
    destination_district: str,
    freight_rate_per_qtl_km: float = 0.50  # ~ ₹50 per quintal per 100 km (~ ₹5/km per Ton)
) -> Dict:
    """
    Compute transport cost and net price realization for a buyer/listing pair.
    """
    distance_km = get_district_distance(origin_district, destination_district)

    if distance_km is None:
        # Distance unavailable
        return {
            "distance_km": None,
            "estimated_transport_cost_total": 0.0,
            "estimated_transport_cost_per_qtl": 0.0,
            "net_price_per_qtl": round(offered_price_per_qtl, 2),
            "net_total_realization": round(offered_price_per_qtl * quantity_qtl, 2),
            "proximity_tag": "Location Distance Unknown",
            "transport_disclaimer": "Exact transport cost requires logistics provider quote.",
        }

    is_local = (distance_km <= 20.0)
    transport_cost_per_qtl = round(distance_km * freight_rate_per_qtl_km, 2) if not is_local else 0.0
    total_transport_cost = round(transport_cost_per_qtl * quantity_qtl, 2)
    net_price_per_qtl = round(offered_price_per_qtl - transport_cost_per_qtl, 2)
    net_total_realization = round(net_price_per_qtl * quantity_qtl, 2)

    if is_local:
        proximity_tag = "🟢 Local Cluster (Geographically Closer)"
    elif distance_km <= 100.0:
        proximity_tag = "🟡 Nearby District"
    else:
        proximity_tag = "🔵 Regional District"

    return {
        "origin_district": origin_district,
        "destination_district": destination_district,
        "distance_km": distance_km,
        "is_local": is_local,
        "estimated_transport_cost_total": total_transport_cost,
        "estimated_transport_cost_per_qtl": transport_cost_per_qtl,
        "net_price_per_qtl": net_price_per_qtl,
        "net_total_realization": net_total_realization,
        "proximity_tag": proximity_tag,
        "transport_disclaimer": f"Estimated based on approx {distance_km} km district distance. Exact transport cost requires actual logistics rates.",
    }


# Configurable delivery duration slabs based on road distance
DELIVERY_DISTANCE_SLABS = [
    (100.0, 1),        # 0–100 km   → 1 day
    (300.0, 2),        # 101–300 km → 2 days
    (500.0, 3),        # 301–500 km → 3 days
    (800.0, 4),        # 501–800 km → 4 days
    (float('inf'), 5)  # 801+ km    → 5 days
]


def calculate_delivery_estimate(
    origin_district: str,
    destination_district: str,
    start_date: Optional[date] = None
) -> Dict:
    """
    Calculate estimated delivery days and expected delivery date dynamically
    based on the Haversine / road distance between farmer and buyer locations.
    """
    dist = get_district_distance(origin_district, destination_district)
    # Default to 120.0 km (2 days) if locations are unmapped or external
    distance_km = round(dist, 1) if dist is not None else 120.0

    delivery_days = 2
    for max_km, days in DELIVERY_DISTANCE_SLABS:
        if distance_km <= max_km:
            delivery_days = days
            break

    base_date = start_date or date.today()
    expected_date = base_date + timedelta(days=delivery_days)

    return {
        "distance_km": distance_km,
        "delivery_days": delivery_days,
        "expected_delivery_date": expected_date,
        "formatted_expected_date": expected_date.strftime("%d %b %Y"),
        "origin_district": origin_district,
        "destination_district": destination_district
    }


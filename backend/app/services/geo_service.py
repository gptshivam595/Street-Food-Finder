from __future__ import annotations

import math

from app.schemas.vendor import VendorResponse


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    earth_radius_km = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    rad_lat1 = math.radians(lat1)
    rad_lat2 = math.radians(lat2)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(d_lng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius_km * c


def sort_vendors_by_distance(
    vendors: list[VendorResponse],
    user_lat: float,
    user_lng: float,
) -> list[VendorResponse]:
    for vendor in vendors:
        vendor.distance_km = round(
            haversine_km(user_lat, user_lng, vendor.latitude, vendor.longitude),
            2,
        )
    return sorted(vendors, key=lambda vendor: vendor.distance_km if vendor.distance_km is not None else float("inf"))


def filter_by_radius(
    vendors: list[VendorResponse],
    user_lat: float,
    user_lng: float,
    radius_km: float,
) -> list[VendorResponse]:
    filtered: list[VendorResponse] = []
    for vendor in vendors:
        distance = haversine_km(user_lat, user_lng, vendor.latitude, vendor.longitude)
        vendor.distance_km = round(distance, 2)
        if distance <= radius_km:
            filtered.append(vendor)
    return filtered

import hashlib
import json
import time
from typing import Optional, Dict, Any

# Simple in-memory cache with Time-To-Live (TTL)
_CACHE: Dict[str, Dict[str, Any]] = {}
CACHE_TTL_SECONDS = 3600  # Cache results for 1 hour

def generate_cache_key(
    destination: str,
    num_days: int,
    budget_total: float,
    currency: str,
    travel_style: str,
    interests: list,
    group_type: str,
    pace: str
) -> str:
    """Generates a unique SHA-256 hash key based on input preferences."""
    payload = {
        "dest": destination.strip().lower(),
        "days": num_days,
        "budget": budget_total,
        "curr": currency.upper(),
        "style": travel_style.lower(),
        "interests": sorted([i.lower() for i in interests]),
        "group": group_type.lower(),
        "pace": pace.lower()
    }
    raw_str = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()

def get_cached_itinerary(cache_key: str) -> Optional[Dict[str, Any]]:
    """Retrieves cached itinerary if it exists and hasn't expired."""
    entry = _CACHE.get(cache_key)
    if not entry:
        return None
    
    # Check if expired
    if time.time() - entry["timestamp"] > CACHE_TTL_SECONDS:
        del _CACHE[cache_key]
        return None
        
    return entry["data"]

def set_cached_itinerary(cache_key: str, data: Dict[str, Any]) -> None:
    """Stores itinerary in cache with current timestamp."""
    _CACHE[cache_key] = {
        "data": data,
        "timestamp": time.time()
    }

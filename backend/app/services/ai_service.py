from datetime import date
from typing import List, Dict, Any, Tuple
from app.ai.prompt_builder import build_itinerary_prompt
from app.ai.groq_client import call_groq_api
from app.ai.response_parser import clean_and_parse_json
from app.ai.cache_manager import (
    generate_cache_key,
    get_cached_itinerary,
    set_cached_itinerary
)

async def generate_itinerary_service(
    destination: str,
    start_date: date,
    end_date: date,
    budget_total: float,
    currency: str = "INR",
    travel_style: str = "balanced",
    interests: List[str] = None,
    group_type: str = "solo",
    group_size: int = 1,
    accommodation_preference: str = "hotel",
    pace: str = "moderate"
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Complete pipeline orchestrator:
    1. Check Cache
    2. Build Prompt
    3. Call Groq
    4. Parse & Validate JSON
    5. Save to Cache
    Returns: (parsed_itinerary_json, metadata_dict)
    """
    if interests is None:
        interests = ["sightseeing", "food"]

    num_days = (end_date - start_date).days + 1
    if num_days <= 0:
        raise ValueError("End date must be greater than or equal to start date.")

    # 1. Check Cache
    cache_key = generate_cache_key(
        destination, num_days, budget_total, currency,
        travel_style, interests, group_type, pace
    )
    cached_plan = get_cached_itinerary(cache_key)
    if cached_plan:
        metadata = {
            "cached": True,
            "model_used": "cache-hit",
            "generation_time_ms": 0,
            "tokens_input": 0,
            "tokens_output": 0
        }
        return cached_plan, metadata

    # 2. Build Prompt
    prompt = build_itinerary_prompt(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        num_days=num_days,
        budget_total=budget_total,
        currency=currency,
        travel_style=travel_style,
        interests=interests,
        group_type=group_type,
        group_size=group_size,
        accommodation_preference=accommodation_preference,
        pace=pace
    )

    # 3. Call Groq API
    raw_response, metadata = await call_groq_api(prompt)

    # 4. Parse & Clean JSON
    parsed_itinerary = clean_and_parse_json(raw_response)

    # 5. Save to Cache
    set_cached_itinerary(cache_key, parsed_itinerary)
    metadata["cached"] = False

    return parsed_itinerary, metadata

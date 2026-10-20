import json
import re
from typing import Dict, Any, Optional

def extract_json_object(raw_text: str) -> Dict[str, Any]:
    """Helper to extract and parse JSON from raw LLM text."""
    if not raw_text or not raw_text.strip():
        raise ValueError("AI response was empty.")

    cleaned = raw_text.strip()

    # Strip markdown code blocks
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    # Locate outer braces
    start_idx = cleaned.find("{")
    end_idx = cleaned.rfind("}")

    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise ValueError("No valid JSON object found in AI response.")

    json_str = cleaned[start_idx : end_idx + 1]

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON string: {e}")

def clean_and_parse_json(raw_text: str) -> Dict[str, Any]:
    """Parses full multi-day itinerary response."""
    parsed_data = extract_json_object(raw_text)

    # Full itinerary verification
    required_keys = ["trip_title", "destination", "days"]
    for key in required_keys:
        if key not in parsed_data:
            raise ValueError(f"Missing required key '{key}' in AI generated itinerary.")

    if not isinstance(parsed_data.get("days"), list) or len(parsed_data["days"]) == 0:
        raise ValueError("Itinerary contains no days or days is not a list.")

    return parsed_data

def clean_and_parse_day_json(raw_text: str) -> Dict[str, Any]:
    """Parses single-day itinerary regeneration response."""
    parsed_data = extract_json_object(raw_text)

    if "activities" not in parsed_data or not isinstance(parsed_data["activities"], list):
        raise ValueError("Single day JSON must contain an 'activities' list.")

    return parsed_data

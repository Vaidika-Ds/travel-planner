from typing import List, Optional
from datetime import date


def build_itinerary_prompt(
    destination: str,
    start_date: date,
    end_date: date,
    num_days: int,
    budget_total: float,
    currency: str,
    travel_style: str,
    interests: List[str],
    group_type: str,
    group_size: int,
    accommodation_preference: str,
    pace: str,
) -> str:
    """
    Builds a structured prompt for the Groq AI model.
    Returns a string that tells the AI exactly what to do and what format to return.
    """

    interests_str = ", ".join(interests) if interests else "general sightseeing"
    budget_per_day = round(budget_total / num_days, 2) if num_days > 0 else budget_total

    prompt = f"""You are an expert travel planner with 20 years of experience creating personalized, realistic, and budget-conscious travel itineraries.

TASK:
Create a detailed {num_days}-day travel itinerary for {destination}.

TRAVELER DETAILS:
- Destination    : {destination}
- Travel Dates   : {start_date} to {end_date} ({num_days} days)
- Total Budget   : {budget_total} {currency} (approx. {budget_per_day} {currency}/day)
- Travel Style   : {travel_style}
- Interests      : {interests_str}
- Group Type     : {group_type}
- Group Size     : {group_size} people
- Accommodation  : {accommodation_preference}
- Pace           : {pace} (slow = 2-3 activities/day, moderate = 3-4, fast = 5-6)

RULES:
1. Keep all costs realistic and within the total budget of {budget_total} {currency}.
2. Match the pace: {pace} paced itinerary.
3. Tailor activities to the interests: {interests_str}.
4. Include a mix of: sightseeing, dining, travel, leisure activities.
5. Keep descriptions concise: exactly 1 to 2 clear sentences per activity to avoid truncation.
6. Provide exactly 3 to 4 activities per day.
7. time_slot must be in format "09:00 AM - 11:00 AM".
8. activity_type must be one of: sightseeing, dining, travel, leisure, accommodation.
9. Each day must have a creative theme.
10. All dates must be real calendar dates starting from {start_date}.

CRITICAL INSTRUCTION:
Return ONLY a valid JSON object.
Do NOT include any markdown, code blocks, backticks, explanations, or extra text.
Start your response directly with {{ and end with }}.

The JSON must follow this EXACT structure:

{{
  "trip_title": "A creative title for this trip",
  "destination": "{destination}",
  "total_days": {num_days},
  "estimated_total_cost": 0.0,
  "currency": "{currency}",
  "days": [
    {{
      "day_number": 1,
      "date": "YYYY-MM-DD",
      "theme": "Theme for this day",
      "estimated_day_cost": 0.0,
      "activities": [
        {{
          "time_slot": "09:00 AM - 11:00 AM",
          "activity_type": "sightseeing",
          "name": "Activity Name",
          "description": "Brief description of the activity",
          "location": "Specific location or address",
          "estimated_cost": 0.0,
          "duration_minutes": 120,
          "tips": "A helpful practical tip"
        }}
      ]
    }}
  ],
  "accommodation_suggestions": ["Hotel/hostel name 1", "Hotel/hostel name 2"],
  "transport_tips": "Key transport advice for getting around {destination}",
  "general_tips": ["Tip 1", "Tip 2", "Tip 3"]
}}"""

    return prompt


def build_single_day_prompt(
    destination: str,
    day_number: int,
    day_date: Optional[date],
    day_budget: float,
    currency: str,
    travel_style: str,
    interests: List[str],
    pace: str,
    existing_themes: List[str] = None
) -> str:
    """
    Builds a prompt to regenerate only ONE specific day of an itinerary.
    """
    interests_str = ", ".join(interests) if interests else "general sightseeing"
    themes_avoid = f"Avoid repeating these existing day themes: {', '.join(existing_themes)}" if existing_themes else ""

    date_str = str(day_date) if day_date else f"Day {day_number}"

    return f"""You are an expert travel planner.
TASK:
Generate a fresh, brand-new single-day travel plan for Day {day_number} in {destination}.

DETAILS:
- Destination   : {destination}
- Day Number    : {day_number} ({date_str})
- Day Budget    : {day_budget} {currency}
- Style & Pace  : {travel_style}, {pace} pace
- Interests     : {interests_str}
{themes_avoid}

RULES:
1. Provide a creative theme for the day.
2. Provide 3-4 diverse activities (sightseeing, dining, leisure).
3. Total estimated_day_cost should be realistic and around {day_budget} {currency}.
4. Return ONLY a valid JSON object matching the exact format below:

{{
  "day_number": {day_number},
  "date": "{date_str}",
  "theme": "Fresh Creative Theme",
  "estimated_day_cost": {day_budget},
  "activities": [
    {{
      "time_slot": "09:00 AM - 11:30 AM",
      "activity_type": "sightseeing",
      "name": "Activity Name",
      "description": "Short 1-2 sentence description.",
      "location": "Location Name",
      "estimated_cost": 0.0,
      "duration_minutes": 120,
      "tips": "Practical tip."
    }}
  ]
}}"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Dict, Any
from uuid import UUID
from datetime import datetime

from app.db.database import get_db
from app.models.models import Trip, Itinerary, ItineraryDay, Activity, AIGenerationLog
from app.schemas.trip_schema import TripCreateRequest, ItineraryResponse
from app.core.security import get_current_user_id
from app.services.ai_service import generate_itinerary_service

router = APIRouter(prefix="/itinerary", tags=["Itinerary"])

async def log_ai_usage(
    db: AsyncSession,
    trip_id: UUID,
    user_id: UUID,
    metadata: Dict[str, Any]
):
    """Background task to record AI execution metrics without blocking the response."""
    try:
        log_entry = AIGenerationLog(
            trip_id=trip_id,
            user_id=user_id,
            model_used=metadata.get("model_used"),
            tokens_input=metadata.get("tokens_input", 0),
            tokens_output=metadata.get("tokens_output", 0),
            generation_time_ms=metadata.get("generation_time_ms", 0),
            status="SUCCESS"
        )
        db.add(log_entry)
        await db.commit()
    except Exception as e:
        print(f"Failed to log AI metrics: {e}")

@router.post("/generate", response_model=Dict[str, Any])
async def generate_itinerary_endpoint(
    req: TripCreateRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """
    Core AI generation endpoint:
    1. Runs AI pipeline to generate structured day-by-day plan.
    2. Persists Trip, Itinerary, Days, and Activities in Supabase DB.
    3. Queues background AI usage logging.
    4. Returns complete itinerary payload to the caller.
    """
    num_days = (req.end_date - req.start_date).days + 1
    if num_days <= 0:
        raise HTTPException(status_code=400, detail="End date must be on or after start date.")

    # 1. Run AI Generation Pipeline
    try:
        raw_itinerary, metadata = await generate_itinerary_service(
            destination=req.destination,
            start_date=req.start_date,
            end_date=req.end_date,
            budget_total=req.budget_total,
            currency=req.currency or "INR",
            travel_style=req.travel_style or "moderate",
            interests=req.interests or [],
            group_type=req.group_type or "solo",
            group_size=req.group_size or 1,
            accommodation_preference=req.accommodation_preference or "hotel",
            pace=req.pace or "moderate"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

    # 2. Save Trip Record in Supabase
    new_trip = Trip(
        user_id=user_id,
        title=raw_itinerary.get("trip_title", f"Trip to {req.destination}"),
        destination=req.destination,
        start_date=req.start_date,
        end_date=req.end_date,
        num_days=num_days,
        budget_total=req.budget_total,
        currency=req.currency or "INR",
        group_type=req.group_type,
        group_size=req.group_size,
        travel_style=req.travel_style,
        interests=req.interests,
        accommodation_preference=req.accommodation_preference,
        pace=req.pace,
        status="COMPLETED"
    )
    db.add(new_trip)
    await db.flush()

    # 3. Save Itinerary Container
    new_itinerary = Itinerary(
        trip_id=new_trip.id,
        estimated_total_cost=raw_itinerary.get("estimated_total_cost", req.budget_total),
        transport_tips=raw_itinerary.get("transport_tips"),
        general_tips=raw_itinerary.get("general_tips", []),
        accommodation_suggestions=raw_itinerary.get("accommodation_suggestions", [])
    )
    db.add(new_itinerary)
    await db.flush()

    # 4. Save Days and Activities
    for day_data in raw_itinerary.get("days", []):
        day_record = ItineraryDay(
            itinerary_id=new_itinerary.id,
            day_number=day_data.get("day_number", 1),
            theme=day_data.get("theme", ""),
            estimated_day_cost=day_data.get("estimated_day_cost", 0.0)
        )
        db.add(day_record)
        await db.flush()

        for idx, act in enumerate(day_data.get("activities", [])):
            activity_record = Activity(
                day_id=day_record.id,
                time_slot=act.get("time_slot"),
                activity_type=act.get("activity_type", "sightseeing"),
                name=act.get("name", "Activity"),
                description=act.get("description"),
                location=act.get("location"),
                estimated_cost=act.get("estimated_cost", 0.0),
                duration_minutes=act.get("duration_minutes", 60),
                tips=act.get("tips"),
                sort_order=idx
            )
            db.add(activity_record)

    await db.commit()

    # 5. Attach DB identifiers to response
    raw_itinerary["id"] = str(new_itinerary.id)
    raw_itinerary["trip_id"] = str(new_trip.id)

    return {
        "status": "success",
        "trip_id": str(new_trip.id),
        "itinerary_id": str(new_itinerary.id),
        "itinerary": raw_itinerary,
        "metadata": metadata
    }


from pydantic import BaseModel
from typing import List, Optional
from app.ai.prompt_builder import build_single_day_prompt
from app.ai.groq_client import call_groq_api
from app.ai.response_parser import clean_and_parse_json, clean_and_parse_day_json

class RegenerateDayRequest(BaseModel):
    destination: str
    day_number: int
    day_date: Optional[str] = None
    day_budget: float
    currency: Optional[str] = "INR"
    travel_style: Optional[str] = "moderate"
    interests: Optional[List[str]] = []
    pace: Optional[str] = "moderate"
    existing_themes: Optional[List[str]] = []

@router.post("/regenerate-day")
async def regenerate_single_day(req: RegenerateDayRequest):
    """Generates a fresh single-day plan without modifying other days."""
    try:
        prompt = build_single_day_prompt(
            destination=req.destination,
            day_number=req.day_number,
            day_date=req.day_date,
            day_budget=req.day_budget,
            currency=req.currency,
            travel_style=req.travel_style,
            interests=req.interests,
            pace=req.pace,
            existing_themes=req.existing_themes
        )
        raw_text, metadata = await call_groq_api(prompt)
        day_json = clean_and_parse_day_json(raw_text)
        return {
            "status": "success",
            "day": day_json,
            "metadata": metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to regenerate day: {str(e)}")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.models import Trip, Itinerary, ItineraryDay, Activity
from app.schemas.trip_schema import TripCreateRequest, TripResponse
from app.core.security import get_current_user_id

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.get("/", response_model=List[TripResponse])
async def list_user_trips(
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """Retrieve all trips created by the logged in user"""
    query = (
        select(Trip)
        .options(
            selectinload(Trip.itinerary)
            .selectinload(Itinerary.days)
            .selectinload(ItineraryDay.activities)
        )
        .where(Trip.user_id == user_id)
        .order_by(Trip.created_at.desc())
    )
    result = await db.execute(query)
    trips = result.scalars().all()
    return trips

@router.post("/", response_model=TripResponse)
async def create_trip(
    trip_data: TripCreateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """Initialize a new trip preference record"""
    num_days = (trip_data.end_date - trip_data.start_date).days + 1
    if num_days <= 0:
        raise HTTPException(status_code=400, detail="End date must be on or after start date.")

    new_trip = Trip(
        user_id=user_id,
        title=f"Trip to {trip_data.destination}",
        destination=trip_data.destination,
        start_date=trip_data.start_date,
        end_date=trip_data.end_date,
        num_days=num_days,
        budget_total=trip_data.budget_total,
        currency=trip_data.currency,
        group_type=trip_data.group_type,
        group_size=trip_data.group_size,
        travel_style=trip_data.travel_style,
        interests=trip_data.interests,
        accommodation_preference=trip_data.accommodation_preference,
        pace=trip_data.pace,
        status="PENDING"
    )
    db.add(new_trip)
    await db.flush()
    await db.refresh(new_trip)
    return new_trip

@router.get("/{trip_id}", response_model=TripResponse)
async def get_trip_details(
    trip_id: UUID,
    db: AsyncSession = Depends(get_db),
    user_id: UUID = Depends(get_current_user_id)
):
    """Fetch details of a specific trip by its ID"""
    query = (
        select(Trip)
        .options(
            selectinload(Trip.itinerary)
            .selectinload(Itinerary.days)
            .selectinload(ItineraryDay.activities)
        )
        .where(Trip.id == trip_id)
    )
    result = await db.execute(query)
    trip = result.scalar_one_or_none()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Check ownership or if trip is publicly shared
    if trip.user_id != user_id and not trip.is_shared:
        raise HTTPException(status_code=403, detail="Not authorized to view this trip")

    return trip

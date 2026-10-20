from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID

# Activity Schemas
class ActivityBase(BaseModel):
    time_slot: Optional[str] = None
    activity_type: Optional[str] = "sightseeing"
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    estimated_cost: Optional[float] = 0.0
    duration_minutes: Optional[int] = 60
    tips: Optional[str] = None
    sort_order: Optional[int] = 0
    is_custom: Optional[bool] = False

class ActivityCreate(ActivityBase):
    pass

class ActivityResponse(ActivityBase):
    id: UUID
    day_id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Day Schemas
class DayPlanBase(BaseModel):
    day_number: int
    date: Optional[date] = None
    theme: Optional[str] = None
    estimated_day_cost: Optional[float] = 0.0

class DayPlanCreate(DayPlanBase):
    activities: List[ActivityCreate] = []

class DayPlanResponse(DayPlanBase):
    id: UUID
    itinerary_id: UUID
    activities: List[ActivityResponse] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Itinerary Schemas
class ItineraryResponse(BaseModel):
    id: Optional[UUID] = None
    trip_id: Optional[UUID] = None
    trip_title: Optional[str] = None
    destination: Optional[str] = None
    total_days: Optional[int] = None
    estimated_total_cost: Optional[float] = 0.0
    currency: Optional[str] = "INR"
    days: List[DayPlanResponse] = []
    accommodation_suggestions: Optional[List[str]] = []
    transport_tips: Optional[str] = None
    general_tips: Optional[List[str]] = []

    class Config:
        from_attributes = True

# Trip Schemas
class TripCreateRequest(BaseModel):
    destination: str
    start_date: date
    end_date: date
    budget_total: float
    currency: Optional[str] = "INR"
    travel_style: Optional[str] = "moderate"
    interests: List[str] = []
    group_type: Optional[str] = "solo"
    group_size: Optional[int] = 1
    accommodation_preference: Optional[str] = "hotel"
    pace: Optional[str] = "moderate"

class TripResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: Optional[str] = None
    destination: str
    start_date: date
    end_date: date
    num_days: Optional[int] = None
    budget_total: Optional[float] = None
    currency: str
    group_type: Optional[str] = None
    group_size: Optional[int] = 1
    travel_style: Optional[str] = None
    interests: Optional[List[str]] = []
    accommodation_preference: Optional[str] = None
    pace: Optional[str] = None
    status: str
    is_shared: bool
    created_at: datetime
    itinerary: Optional[ItineraryResponse] = None

    class Config:
        from_attributes = True

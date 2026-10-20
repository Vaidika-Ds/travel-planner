import uuid
from datetime import datetime, date
from sqlalchemy import (
    Column, String, Text, Integer, Numeric, Boolean, Date, DateTime, ForeignKey, ARRAY
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True)
    full_name = Column(String(100), nullable=True)
    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trips = relationship("Trip", back_populates="user", cascade="all, delete-orphan")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False)
    travel_style = Column(String(50), nullable=True)
    interests = Column(ARRAY(String), nullable=True)
    default_budget = Column(Numeric(10, 2), nullable=True)
    default_currency = Column(String(3), default="INR")
    default_pace = Column(String(20), default="moderate")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("UserProfile", back_populates="preferences")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=True)
    destination = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    num_days = Column(Integer, nullable=True)
    budget_total = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(3), default="INR")
    group_type = Column(String(50), nullable=True)
    group_size = Column(Integer, default=1)
    travel_style = Column(String(50), nullable=True)
    interests = Column(ARRAY(String), nullable=True)
    accommodation_preference = Column(String(50), nullable=True)
    pace = Column(String(20), default="moderate")
    status = Column(String(20), default="PENDING")
    is_shared = Column(Boolean, default=False)
    share_token = Column(UUID(as_uuid=True), default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("UserProfile", back_populates="trips")
    itinerary = relationship("Itinerary", back_populates="trip", uselist=False, cascade="all, delete-orphan")


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"), unique=True, nullable=False)
    estimated_total_cost = Column(Numeric(10, 2), nullable=True)
    transport_tips = Column(Text, nullable=True)
    general_tips = Column(ARRAY(String), nullable=True)
    accommodation_suggestions = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    trip = relationship("Trip", back_populates="itinerary")
    days = relationship("ItineraryDay", back_populates="itinerary", cascade="all, delete-orphan", order_by="ItineraryDay.day_number")


class ItineraryDay(Base):
    __tablename__ = "itinerary_days"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_id = Column(UUID(as_uuid=True), ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=True)
    theme = Column(String(200), nullable=True)
    estimated_day_cost = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    itinerary = relationship("Itinerary", back_populates="days")
    activities = relationship("Activity", back_populates="day", cascade="all, delete-orphan", order_by="Activity.sort_order")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    day_id = Column(UUID(as_uuid=True), ForeignKey("itinerary_days.id", ondelete="CASCADE"), nullable=False)
    time_slot = Column(String(50), nullable=True)
    activity_type = Column(String(50), nullable=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    estimated_cost = Column(Numeric(8, 2), default=0.0)
    duration_minutes = Column(Integer, nullable=True)
    tips = Column(Text, nullable=True)
    sort_order = Column(Integer, default=0)
    is_custom = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    day = relationship("ItineraryDay", back_populates="activities")


class AIGenerationLog(Base):
    __tablename__ = "ai_generation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id", ondelete="SET NULL"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user_profiles.id", ondelete="SET NULL"), nullable=True)
    model_used = Column(String(100), nullable=True)
    prompt_hash = Column(String(64), nullable=True)
    tokens_input = Column(Integer, nullable=True)
    tokens_output = Column(Integer, nullable=True)
    generation_time_ms = Column(Integer, nullable=True)
    status = Column(String(20), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

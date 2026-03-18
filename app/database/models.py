import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255))
    google_id = Column(String(255), unique=True)

    google_access_token = Column(Text)
    google_refresh_token = Column(Text)
    google_token_expiry = Column(DateTime)

    calendar_id = Column(String(36), ForeignKey("calendars.id"), index=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime)

    calendar = relationship("Calendar", back_populates="users", foreign_keys=[calendar_id])


class Calendar(Base):
    __tablename__ = "calendars"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255))
    timezone = Column(String(50), default="UTC")

    owner_user_id = Column(String(36), ForeignKey("users.id"))

    google_calendar_id = Column(String(255))
    last_sync_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    users = relationship("User", back_populates="calendar", foreign_keys="User.calendar_id")
    invitations = relationship("CalendarInvitation", back_populates="calendar", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="calendar", cascade="all, delete-orphan")


class CalendarInvitation(Base):
    __tablename__ = "calendar_invitations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    calendar_id = Column(String(36), ForeignKey("calendars.id"), nullable=False)
    invited_email = Column(String(255), nullable=False, index=True)
    inviter_user_id = Column(String(36), ForeignKey("users.id"))
    status = Column(String(20), default="pending", nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime)

    calendar = relationship("Calendar", back_populates="invitations")


class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    calendar_id = Column(String(36), ForeignKey("calendars.id"), nullable=False, index=True)
    created_by_user_id = Column(String(36), ForeignKey("users.id"))

    title = Column(String(255), nullable=False)
    description = Column(Text)

    start_at = Column(DateTime, nullable=False, index=True)
    end_at = Column(DateTime, nullable=False)
    timezone = Column(String(50), default="UTC")

    rrule = Column(String(500))

    google_event_id = Column(String(255))
    google_sync_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_edited_by_user_id = Column(String(36), ForeignKey("users.id"))
    is_deleted = Column(Boolean, default=False, nullable=False)

    calendar = relationship("Calendar", back_populates="events")


Index("ix_events_start_end", Event.start_at, Event.end_at)

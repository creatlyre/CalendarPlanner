from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: str
    google_id: Optional[str] = None
    calendar_id: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CalendarBase(BaseModel):
    name: str
    timezone: str = "UTC"


class CalendarCreate(CalendarBase):
    pass


class CalendarResponse(CalendarBase):
    id: str
    owner_user_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_at: datetime
    end_at: datetime
    timezone: str = "UTC"
    rrule: Optional[str] = None


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: str
    calendar_id: str
    created_by_user_id: Optional[str] = None
    google_event_id: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}

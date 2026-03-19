from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    start_at: datetime
    end_at: datetime
    timezone: str = "UTC"
    rrule: Optional[str] = None
    visibility: Literal["shared", "private"] = "shared"


class EventUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    timezone: Optional[str] = None
    rrule: Optional[str] = None
    visibility: Optional[Literal["shared", "private"]] = None


class EventResponse(BaseModel):
    id: str
    calendar_id: str
    created_by_user_id: Optional[str]
    title: str
    description: Optional[str]
    start_at: datetime
    end_at: datetime
    timezone: str
    is_deleted: bool
    rrule: Optional[str] = None
    visibility: str = "shared"

    model_config = {"from_attributes": True}

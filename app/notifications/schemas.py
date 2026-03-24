from pydantic import BaseModel
from datetime import datetime


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    actor_user_id: str
    actor_name: str = ""
    type: str
    entity_type: str
    entity_id: str | None
    entity_title: str
    is_read: bool
    created_at: datetime | None


class UnreadCountResponse(BaseModel):
    count: int


class PreferenceResponse(BaseModel):
    email_enabled: bool


class PreferenceUpdate(BaseModel):
    email_enabled: bool

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.database.models import Notification, NotificationPreference
from app.database.supabase_store import SupabaseStore


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is not None:
            return parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    except ValueError:
        return None


def _to_notification(row: dict[str, Any]) -> Notification:
    return Notification(
        id=row.get("id", ""),
        user_id=row.get("user_id", ""),
        calendar_id=row.get("calendar_id", ""),
        actor_user_id=row.get("actor_user_id", ""),
        type=row.get("type", ""),
        entity_type=row.get("entity_type", ""),
        entity_id=row.get("entity_id"),
        entity_title=row.get("entity_title", ""),
        is_read=bool(row.get("is_read", False)),
        is_dismissed=bool(row.get("is_dismissed", False)),
        created_at=_parse_dt(row.get("created_at")),
    )


def _to_preference(row: dict[str, Any]) -> NotificationPreference:
    return NotificationPreference(
        id=row.get("id", ""),
        user_id=row.get("user_id", ""),
        email_enabled=bool(row.get("email_enabled", False)),
        created_at=_parse_dt(row.get("created_at")),
        updated_at=_parse_dt(row.get("updated_at")),
    )


class NotificationRepository:
    def __init__(self, db: SupabaseStore):
        self.db = db

    def create(
        self,
        user_id: str,
        calendar_id: str,
        actor_user_id: str,
        type: str,
        entity_type: str,
        entity_id: str | None,
        entity_title: str,
    ) -> Notification:
        row = self.db.insert(
            "notifications",
            {
                "user_id": user_id,
                "calendar_id": calendar_id,
                "actor_user_id": actor_user_id,
                "type": type,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "entity_title": entity_title,
            },
        )
        return _to_notification(row)

    def list_for_user(self, user_id: str, limit: int = 20) -> list[Notification]:
        rows = self.db.select(
            "notifications",
            {
                "user_id": f"eq.{user_id}",
                "is_dismissed": "eq.false",
                "order": "created_at.desc",
                "limit": str(limit),
            },
        )
        return [_to_notification(r) for r in rows]

    def unread_count(self, user_id: str) -> int:
        return self.db.count(
            "notifications",
            {
                "user_id": f"eq.{user_id}",
                "is_read": "eq.false",
                "is_dismissed": "eq.false",
            },
        )

    def mark_read(self, notification_id: str, user_id: str) -> Notification | None:
        result = self.db.update(
            "notifications",
            {"id": f"eq.{notification_id}", "user_id": f"eq.{user_id}"},
            {"is_read": True},
        )
        return _to_notification(result) if result else None

    def mark_all_read(self, user_id: str) -> int:
        result = self.db.update(
            "notifications",
            {
                "user_id": f"eq.{user_id}",
                "is_read": "eq.false",
                "is_dismissed": "eq.false",
            },
            {"is_read": True},
        )
        return 1 if result else 0

    def dismiss(self, notification_id: str, user_id: str) -> Notification | None:
        result = self.db.update(
            "notifications",
            {"id": f"eq.{notification_id}", "user_id": f"eq.{user_id}"},
            {"is_dismissed": True},
        )
        return _to_notification(result) if result else None

    def get_preference(self, user_id: str) -> NotificationPreference:
        rows = self.db.select(
            "notification_preferences",
            {"user_id": f"eq.{user_id}", "limit": "1"},
        )
        if rows:
            return _to_preference(rows[0])
        return NotificationPreference(user_id=user_id, email_enabled=False)

    def upsert_preference(self, user_id: str, email_enabled: bool) -> NotificationPreference:
        existing = self.db.select(
            "notification_preferences",
            {"user_id": f"eq.{user_id}", "limit": "1"},
        )
        if existing:
            result = self.db.update(
                "notification_preferences",
                {"user_id": f"eq.{user_id}"},
                {"email_enabled": email_enabled, "updated_at": "now()"},
            )
            return _to_preference(result) if result else self.get_preference(user_id)
        else:
            row = self.db.insert(
                "notification_preferences",
                {"user_id": user_id, "email_enabled": email_enabled},
            )
            return _to_preference(row)

    def exists_reminder(self, user_id: str, entity_id: str, type: str) -> bool:
        return (
            self.db.count(
                "notifications",
                {
                    "user_id": f"eq.{user_id}",
                    "entity_id": f"eq.{entity_id}",
                    "type": f"eq.{type}",
                },
            )
            > 0
        )

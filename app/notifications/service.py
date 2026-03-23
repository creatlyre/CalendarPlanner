from __future__ import annotations

from app.database.models import Notification, NotificationPreference
from app.notifications.repository import NotificationRepository
from app.users.repository import UserRepository


class NotificationService:
    def __init__(self, repo: NotificationRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def list_for_user(self, user_id: str, limit: int = 20) -> list[dict]:
        notifications = self.repo.list_for_user(user_id, limit)
        # Cache actor names to avoid repeated lookups (only 2 users in household)
        actor_cache: dict[str, str] = {}
        results = []
        for n in notifications:
            if n.actor_user_id not in actor_cache:
                actor = self.user_repo.get_user_by_id(n.actor_user_id)
                actor_cache[n.actor_user_id] = actor.name if actor else ""
            results.append(
                {
                    "id": n.id,
                    "user_id": n.user_id,
                    "actor_user_id": n.actor_user_id,
                    "actor_name": actor_cache[n.actor_user_id],
                    "type": n.type,
                    "entity_type": n.entity_type,
                    "entity_id": n.entity_id,
                    "entity_title": n.entity_title,
                    "is_read": n.is_read,
                    "created_at": n.created_at,
                }
            )
        return results

    def unread_count(self, user_id: str) -> int:
        return self.repo.unread_count(user_id)

    def mark_read(self, notification_id: str, user_id: str) -> Notification | None:
        return self.repo.mark_read(notification_id, user_id)

    def mark_all_read(self, user_id: str) -> int:
        return self.repo.mark_all_read(user_id)

    def dismiss(self, notification_id: str, user_id: str) -> Notification | None:
        return self.repo.dismiss(notification_id, user_id)

    def get_preference(self, user_id: str) -> NotificationPreference:
        return self.repo.get_preference(user_id)

    def update_preference(self, user_id: str, email_enabled: bool) -> NotificationPreference:
        return self.repo.upsert_preference(user_id, email_enabled)

    def create_for_partner(
        self,
        actor_user_id: str,
        calendar_id: str,
        type: str,
        entity_type: str,
        entity_id: str | None,
        entity_title: str,
    ) -> Notification | None:
        members = self.user_repo.get_household_members(actor_user_id)
        partner = next((m for m in members if m.id != actor_user_id), None)
        if not partner:
            return None
        return self.repo.create(
            user_id=partner.id,
            calendar_id=calendar_id,
            actor_user_id=actor_user_id,
            type=type,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_title=entity_title,
        )

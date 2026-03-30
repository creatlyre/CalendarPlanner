from __future__ import annotations

import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from app.database.models import Notification, NotificationPreference
from app.notifications.repository import NotificationRepository
from app.users.repository import UserRepository


class NotificationService:
    def __init__(self, repo: NotificationRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def list_for_user(self, user_id: str, limit: int = 20) -> list[dict]:
        # Check reminders first (on-demand)
        user = self.user_repo.get_user_by_id(user_id)
        if user and user.calendar_id:
            try:
                self.check_reminders(user_id, user.calendar_id)
            except Exception:
                pass  # Reminder check failure must not break feed

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

    def update_preference(
        self, user_id: str, email_enabled: bool
    ) -> NotificationPreference:
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
        notification = self.repo.create(
            user_id=partner.id,
            calendar_id=calendar_id,
            actor_user_id=actor_user_id,
            type=type,
            entity_type=entity_type,
            entity_id=entity_id,
            entity_title=entity_title,
        )
        # Send email if partner has email alerts enabled
        try:
            pref = self.repo.get_preference(partner.id)
            if pref.email_enabled and partner.email:
                actor = self.user_repo.get_user_by_id(actor_user_id)
                actor_name = actor.name if actor else "Partner"
                self.send_email_alert(partner.email, actor_name, type, entity_title)
        except Exception:
            pass  # Email failure must not affect notification creation
        return notification

    def send_email_alert(
        self,
        recipient_email: str,
        actor_name: str,
        action_type: str,
        entity_title: str,
    ) -> bool:
        from config import Settings

        settings = Settings()
        if not settings.SMTP_HOST or not settings.SMTP_FROM_ADDRESS:
            return False  # SMTP not configured, skip silently
        try:
            msg = EmailMessage()
            msg["Subject"] = f"Dobry Plan: {actor_name} {action_type.replace('_', ' ')}"
            msg["From"] = settings.SMTP_FROM_ADDRESS
            msg["To"] = recipient_email
            body = f"{actor_name} {action_type.replace('_', ' ')}: {entity_title}\n"
            msg.set_content(body)
            with smtplib.SMTP(
                settings.SMTP_HOST, settings.SMTP_PORT, timeout=10
            ) as server:
                if settings.SMTP_USE_TLS:
                    server.starttls()
                if settings.SMTP_USER and settings.SMTP_PASSWORD:
                    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception:
            return False  # Email failure must not break notifications

    def check_reminders(self, user_id: str, calendar_id: str) -> None:
        from app.events.repository import EventRepository

        event_repo = EventRepository(self.repo.db)
        now = datetime.now(timezone.utc)
        range_end = now + timedelta(hours=24)
        events = event_repo.list_recurrence_roots_until(
            calendar_id, range_end, requesting_user_id=user_id
        )

        for event in events:
            if not event.effective_reminders or not event.start_at:
                continue
            for minutes in event.effective_reminders:
                reminder_time = event.start_at - timedelta(minutes=minutes)
                # Reminder is due if within last hour window
                if reminder_time <= now and reminder_time > now - timedelta(hours=1):
                    if not self.repo.exists_reminder(
                        user_id, event.id, "event_reminder"
                    ):
                        self.repo.create(
                            user_id=user_id,
                            calendar_id=calendar_id,
                            actor_user_id=user_id,
                            type="event_reminder",
                            entity_type="event",
                            entity_id=event.id,
                            entity_title=event.title,
                        )

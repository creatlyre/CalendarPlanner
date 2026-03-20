from __future__ import annotations

from datetime import datetime, timezone

from app.database.models import MonthlyHours, AdditionalEarning
from app.database.supabase_store import SupabaseStore
from app.budget.income_schemas import MonthlyHoursUpdate, AdditionalEarningCreate


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


def _to_monthly_hours(row: dict) -> MonthlyHours:
    return MonthlyHours(
        id=row.get("id", ""),
        calendar_id=row.get("calendar_id", ""),
        year=int(row.get("year", 0)),
        month=int(row.get("month", 0)),
        rate_1_hours=row.get("rate_1_hours"),
        rate_2_hours=row.get("rate_2_hours"),
        rate_3_hours=row.get("rate_3_hours"),
        created_at=_parse_dt(row.get("created_at")),
        updated_at=_parse_dt(row.get("updated_at")),
    )


def _to_additional_earning(row: dict) -> AdditionalEarning:
    return AdditionalEarning(
        id=row.get("id", ""),
        calendar_id=row.get("calendar_id", ""),
        year=int(row.get("year", 0)),
        month=int(row.get("month", 0)),
        name=row.get("name", ""),
        amount=float(row.get("amount", 0)),
        created_at=_parse_dt(row.get("created_at")),
        updated_at=_parse_dt(row.get("updated_at")),
    )


class MonthlyHoursRepository:
    def __init__(self, db: SupabaseStore):
        self.db = db

    def get_by_calendar_year(self, calendar_id: str, year: int) -> list[MonthlyHours]:
        rows = self.db.select(
            "monthly_hours",
            {"calendar_id": f"eq.{calendar_id}", "year": f"eq.{year}"},
        )
        return [_to_monthly_hours(r) for r in rows]

    def get_by_calendar_year_month(self, calendar_id: str, year: int, month: int) -> MonthlyHours | None:
        rows = self.db.select(
            "monthly_hours",
            {"calendar_id": f"eq.{calendar_id}", "year": f"eq.{year}", "month": f"eq.{month}", "limit": "1"},
        )
        return _to_monthly_hours(rows[0]) if rows else None

    def upsert(self, calendar_id: str, payload: MonthlyHoursUpdate) -> MonthlyHours:
        existing = self.get_by_calendar_year_month(calendar_id, payload.year, payload.month)
        if existing:
            row = self.db.update(
                "monthly_hours",
                {"id": f"eq.{existing.id}"},
                {
                    "rate_1_hours": payload.rate_1_hours,
                    "rate_2_hours": payload.rate_2_hours,
                    "rate_3_hours": payload.rate_3_hours,
                    "updated_at": datetime.utcnow().isoformat(),
                },
            )
            return _to_monthly_hours(row) if row else existing
        row = self.db.insert(
            "monthly_hours",
            {
                "calendar_id": calendar_id,
                "year": payload.year,
                "month": payload.month,
                "rate_1_hours": payload.rate_1_hours,
                "rate_2_hours": payload.rate_2_hours,
                "rate_3_hours": payload.rate_3_hours,
            },
        )
        return _to_monthly_hours(row)


class AdditionalEarningsRepository:
    def __init__(self, db: SupabaseStore):
        self.db = db

    def get_by_calendar_year(self, calendar_id: str, year: int) -> list[AdditionalEarning]:
        rows = self.db.select(
            "additional_earnings",
            {"calendar_id": f"eq.{calendar_id}", "year": f"eq.{year}"},
        )
        return [_to_additional_earning(r) for r in rows]

    def get_by_calendar_year_month(self, calendar_id: str, year: int, month: int) -> list[AdditionalEarning]:
        rows = self.db.select(
            "additional_earnings",
            {"calendar_id": f"eq.{calendar_id}", "year": f"eq.{year}", "month": f"eq.{month}"},
        )
        return [_to_additional_earning(r) for r in rows]

    def create(self, calendar_id: str, payload: AdditionalEarningCreate) -> AdditionalEarning:
        row = self.db.insert(
            "additional_earnings",
            {
                "calendar_id": calendar_id,
                "year": payload.year,
                "month": payload.month,
                "name": payload.name,
                "amount": payload.amount,
            },
        )
        return _to_additional_earning(row)

    def delete(self, earning_id: str) -> bool:
        count = self.db.delete(
            "additional_earnings",
            {"id": f"eq.{earning_id}"},
        )
        return count > 0

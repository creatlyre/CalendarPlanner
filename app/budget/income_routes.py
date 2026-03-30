from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.budget.income_repository import (
    MonthlyHoursRepository,
    AdditionalEarningsRepository,
)
from app.budget.income_schemas import (
    AdditionalEarningCreate,
    AdditionalEarningResponse,
    BulkMonthlyHoursUpdate,
    MonthlyHoursResponse,
    MonthlyHoursUpdate,
)
from app.budget.income_service import IncomeService
from app.budget.repository import BudgetSettingsRepository
from app.database.database import get_db
from app.notifications.repository import NotificationRepository
from app.notifications.service import NotificationService
from app.users.repository import UserRepository

router = APIRouter(prefix="/api/budget/income", tags=["income"])


def _service(db) -> IncomeService:
    return IncomeService(
        MonthlyHoursRepository(db),
        AdditionalEarningsRepository(db),
        BudgetSettingsRepository(db),
    )


def _notify_svc(db) -> NotificationService:
    return NotificationService(NotificationRepository(db), UserRepository(db))


@router.get("")
async def get_income_data(
    year: int, user=Depends(get_current_user), db=Depends(get_db)
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    data = service.get_year_data(user.calendar_id, year)
    return {"data": data}


@router.put("/hours")
async def save_hours(
    payload: MonthlyHoursUpdate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    hours = service.save_hours(user.calendar_id, payload)
    try:
        _notify_svc(db).create_for_partner(
            user.id,
            user.calendar_id,
            "income_updated",
            "income",
            None,
            f"Monthly hours {payload.month}",
        )
    except Exception:
        pass
    return {
        "data": MonthlyHoursResponse.model_validate(
            hours, from_attributes=True
        ).model_dump()
    }


@router.post("/hours/bulk")
async def bulk_save_hours(
    payload: BulkMonthlyHoursUpdate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    results = service.bulk_save_hours(user.calendar_id, payload.year, payload.entries)
    return {
        "data": [
            MonthlyHoursResponse.model_validate(h, from_attributes=True).model_dump()
            for h in results
        ]
    }


@router.post("/earnings")
async def add_earning(
    payload: AdditionalEarningCreate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    earning = service.add_earning(user.calendar_id, payload)
    try:
        _notify_svc(db).create_for_partner(
            user.id,
            user.calendar_id,
            "income_created",
            "income",
            earning.id,
            earning.name,
        )
    except Exception:
        pass
    return {
        "data": AdditionalEarningResponse.model_validate(
            earning, from_attributes=True
        ).model_dump()
    }


@router.delete("/earnings/{earning_id}")
async def delete_earning(
    earning_id: str,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    service = _service(db)
    deleted = service.delete_earning(earning_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Earning not found")
    try:
        _notify_svc(db).create_for_partner(
            user.id, user.calendar_id, "income_deleted", "income", None, ""
        )
    except Exception:
        pass
    return {"ok": True}

from __future__ import annotations

from fastapi import Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.billing.repository import BillingRepository
from app.database.database import get_db


async def get_current_plan(
    user=Depends(get_current_user),
    db=Depends(get_db),
) -> str:
    repo = BillingRepository(db)
    sub = repo.get_subscription(user.id)
    if sub:
        return sub.plan
    return "free"


def require_plan(*allowed_plans: str):
    async def _dependency(
        user=Depends(get_current_user),
        db=Depends(get_db),
    ) -> str:
        repo = BillingRepository(db)
        sub = repo.get_subscription(user.id)
        plan = sub.plan if sub else "free"
        if plan not in allowed_plans:
            raise HTTPException(
                status_code=403,
                detail="Upgrade required",
                headers={"X-Upgrade-URL": "/billing/settings"},
            )
        return plan

    return _dependency


def get_user_plan_for_template(user, db) -> str:
    repo = BillingRepository(db)
    sub = repo.get_subscription(user.id)
    return sub.plan if sub else "free"

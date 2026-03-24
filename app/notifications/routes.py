from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.notifications.repository import NotificationRepository
from app.notifications.schemas import (
    NotificationResponse,
    PreferenceResponse,
    PreferenceUpdate,
    UnreadCountResponse,
)
from app.notifications.service import NotificationService
from app.users.repository import UserRepository

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


def _service(db) -> NotificationService:
    return NotificationService(NotificationRepository(db), UserRepository(db))


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    return svc.list_for_user(user.id)


@router.get("/unread-count", response_model=UnreadCountResponse)
async def unread_count(user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    return {"count": svc.unread_count(user.id)}


@router.post("/{notification_id}/read")
async def mark_read(notification_id: str, user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    result = svc.mark_read(notification_id, user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"ok": True}


@router.post("/read-all")
async def mark_all_read(user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    svc.mark_all_read(user.id)
    return {"ok": True}


@router.post("/{notification_id}/dismiss")
async def dismiss(notification_id: str, user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    result = svc.dismiss(notification_id, user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"ok": True}


@router.get("/preferences", response_model=PreferenceResponse)
async def get_preferences(user=Depends(get_current_user), db=Depends(get_db)):
    svc = _service(db)
    pref = svc.get_preference(user.id)
    return {"email_enabled": pref.email_enabled}


@router.put("/preferences", response_model=PreferenceResponse)
async def update_preferences(
    payload: PreferenceUpdate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    svc = _service(db)
    pref = svc.update_preference(user.id, payload.email_enabled)
    return {"email_enabled": pref.email_enabled}

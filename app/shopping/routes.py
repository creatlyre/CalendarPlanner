from fastapi import APIRouter, Depends, HTTPException

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.shopping.repository import ShoppingRepository
from app.shopping.schemas import (
    KeywordLearn,
    MultiItemCreate,
    ShoppingItemCreate,
    ShoppingItemUpdate,
    ShoppingSectionCreate,
    ShoppingSectionUpdate,
)
from app.shopping.service import ShoppingService, SECTION_KEYWORDS

router = APIRouter(prefix="/api/shopping", tags=["shopping"])


def _service(db) -> ShoppingService:
    return ShoppingService(ShoppingRepository(db))


# ── Items ────────────────────────────────────────────────────────────────

@router.get("/items")
async def get_items(user=Depends(get_current_user), db=Depends(get_db)):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    return {"data": service.list_items(user.calendar_id)}


@router.post("/items", status_code=201)
async def create_item(
    payload: ShoppingItemCreate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    item = service.add_item(user.calendar_id, payload.name, payload.section_id)
    return {"data": {"id": item.id, "name": item.name, "section_id": item.section_id}}


@router.post("/items/multi", status_code=201)
async def create_multiple_items(
    payload: MultiItemCreate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    result = service.add_multiple(user.calendar_id, payload.text)
    return {"data": result}


@router.put("/items/{item_id}")
async def update_item(
    item_id: str,
    payload: ShoppingItemUpdate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    data = {}
    if payload.name is not None:
        data["name"] = payload.name
    if payload.section_id is not None:
        data["section_id"] = payload.section_id
    item = service.update_item(item_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"data": {"id": item.id, "name": item.name, "section_id": item.section_id}}


@router.delete("/items/{item_id}")
async def delete_item(
    item_id: str,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    deleted = service.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}


@router.post("/items/{item_id}/learn")
async def learn_keyword(
    item_id: str,
    payload: KeywordLearn,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    service.learn_keyword(user.calendar_id, payload.item_name, payload.section_id)
    # Also update the item's section
    service.update_item(item_id, {"section_id": payload.section_id})
    return {"ok": True}


# ── Sections ─────────────────────────────────────────────────────────────

@router.get("/sections")
async def get_sections(user=Depends(get_current_user), db=Depends(get_db)):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    sections = service.list_sections(user.calendar_id)
    return {
        "data": [
            {
                "id": s.id,
                "name": s.name,
                "emoji": s.emoji,
                "sort_order": s.sort_order,
                "is_preset": s.is_preset,
            }
            for s in sections
        ]
    }


@router.post("/sections", status_code=201)
async def create_section(
    payload: ShoppingSectionCreate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    section = service.create_section(
        user.calendar_id, payload.name, payload.emoji, payload.sort_order
    )
    return {"data": {"id": section.id, "name": section.name, "emoji": section.emoji}}


@router.put("/sections/{section_id}")
async def update_section(
    section_id: str,
    payload: ShoppingSectionUpdate,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    data = {}
    if payload.name is not None:
        data["name"] = payload.name
    if payload.emoji is not None:
        data["emoji"] = payload.emoji
    if payload.sort_order is not None:
        data["sort_order"] = payload.sort_order
    section = service.update_section(section_id, data)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"data": {"id": section.id, "name": section.name, "emoji": section.emoji}}


@router.delete("/sections/{section_id}")
async def delete_section(
    section_id: str,
    user=Depends(get_current_user),
    db=Depends(get_db),
):
    if not user.calendar_id:
        raise HTTPException(status_code=400, detail="No calendar linked")
    service = _service(db)
    deleted = service.delete_section(section_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Section not found")
    return {"ok": True}


@router.get("/keywords")
async def get_keywords(user=Depends(get_current_user)):
    return {"data": SECTION_KEYWORDS}

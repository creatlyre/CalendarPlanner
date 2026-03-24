from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, field_validator


class ShoppingItemCreate(BaseModel):
    name: str
    section_id: Optional[str] = None

    @field_validator("name")
    @classmethod
    def valid_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name must not be empty")
        return v


class ShoppingItemUpdate(BaseModel):
    name: Optional[str] = None
    section_id: Optional[str] = None

    @field_validator("name")
    @classmethod
    def valid_name(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Name must not be empty")
        return v


class MultiItemCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def valid_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Text must not be empty")
        return v


class ShoppingSectionCreate(BaseModel):
    name: str
    emoji: str = ""
    sort_order: int = 0


class ShoppingSectionUpdate(BaseModel):
    name: Optional[str] = None
    emoji: Optional[str] = None
    sort_order: Optional[int] = None


class KeywordLearn(BaseModel):
    item_name: str
    section_id: str

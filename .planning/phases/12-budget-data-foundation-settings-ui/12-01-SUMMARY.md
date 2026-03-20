---
phase: 12-budget-data-foundation-settings-ui
plan: 01
status: complete
started: 2026-03-20
completed: 2026-03-20
---

## Summary

Built the complete budget data foundation: BudgetSettings dataclass model, Pydantic validation schemas, Supabase-backed repository, service layer, and FastAPI API routes. Added 24 budget i18n keys to both Polish and English locale files. Registered budget API router in main.py. Added budget_settings table to InMemoryStore test infrastructure.

## Key Files

### Created
- app/budget/__init__.py — Module init
- app/budget/schemas.py — BudgetSettingsUpdate (with positive/non-negative validators) + BudgetSettingsResponse
- app/budget/repository.py — BudgetSettingsRepository with get_by_calendar/create/update CRUD
- app/budget/service.py — BudgetSettingsService with get_settings/save_settings (upsert logic)
- app/budget/routes.py — GET /api/budget/settings + PUT /api/budget/settings endpoints

### Modified
- app/database/models.py — Added BudgetSettings dataclass
- app/locales/pl.json — Added 24 budget.* keys in Polish
- app/locales/en.json — Added 24 budget.* keys in English
- main.py — Registered budget_router
- tests/conftest.py — Added budget_settings table to InMemoryStore

## Decisions
- Used filters dict pattern for SupabaseStore.update (matches EventRepository pattern)
- Validation: rates/costs > 0, balance >= 0, all rounded to 2 decimals
- API returns `{"data": null}` when no settings exist (not 404)

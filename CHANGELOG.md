# Changelog

## 2026-03-19

### feat: complete phase 7 UX flow and sync reminder enhancements (87aae65)

- Added manual event-entry modal for calendar workflow.
- Added invite-page back navigation affordance with keyboard-visible focus styles.
- Updated month-day interaction so day click opens manual entry for selected day (title + time-first flow).
- Preserved quick-add NLP/OCR flow while adding manual-entry bridge from quick-add modal.
- Added Google sync reminder support in event payloads (`reminders` with default popup minutes, plus per-event override support).
- Added `GOOGLE_EVENT_REMINDER_MINUTES` setting in configuration.
- Expanded integration tests for calendar UX and sync reminder payload behavior.

### Verification

- `python -m pytest -q tests/test_calendar_views.py tests/test_sync_api.py` passed.
- `python -m pytest -q tests/test_auth.py tests/test_sync_api.py tests/test_calendar_views.py` passed.

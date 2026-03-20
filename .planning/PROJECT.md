# CalendarPlanner

## What This Is

A shared household calendar web application that lets two people (e.g., partners/spouses) collaboratively manage their schedule from a single source of truth. It supports recurring and one-time events, push sync to Google Calendar, natural-language event requests, image-based event extraction, and full Polish/English localization — keeping both users aligned on the family schedule across all devices.

## Core Value

A shared calendar both partners can edit that stays in sync with Google Calendar, so the family schedule is always current everywhere — on the web and on their phones.

## Current Milestone: v2.0 Budget Tracker

**Goal:** Add household budget tracking with income calculation from hourly rates, expense management, and 12-month financial overview.

**Target features:**
- Income settings with 3 hourly rates, per-month hours, and tax/cost deductions
- Additional household earnings (partner salary, child bonuses)
- Recurring and one-time expense tracking
- 12-month year overview with running account balance
- Settings UI integrated into existing app navigation

## Current State

- v1.1 shipped on 2026-03-20.
- Full Polish/English localization with language switcher, persisted preference, and locale-aware NLP/OCR parsing.
- Day-click quick-entry for rapid event creation with auto-calculated end times.
- Google Calendar reminder payload support (backend ready, UI deferred).
- 145 tests passing across auth, events, calendar views, NLP, sync, and integration.
- 8,164 LOC across Python, HTML templates, and JSON locale files.
- Planning artifacts for v1.0 archived under `.planning/milestones/`.

## Requirements

### Validated

- ✓ Two users can share a single calendar and each add/edit events — v1.0
- ✓ Events can be recurring (daily/weekly/monthly/yearly) — v1.0
- ✓ View upcoming events for the current day and month — v1.0
- ✓ Export/sync events to Google Calendar for both linked users — v1.0
- ✓ Natural-language request processing with review-before-save flow — v1.0
- ✓ Image input extraction with confidence/review and fallback — v1.0
- ✓ Modal-first event entry UX with keyboard and mobile support — v1.0
- ✓ Polish as default locale across all user-facing views and messages — v1.1
- ✓ Language switcher (Polish/English) with persistent preference — v1.1
- ✓ Bilingual copy coverage for auth, calendar, events, sync, NLP, and OCR — v1.1
- ✓ Locale-aware date/time formatting in Polish and English — v1.1
- ✓ NLP and OCR parsing with Polish phrases and diacritics — v1.1
- ✓ Day-click quick-entry for rapid event creation (auto end-time +1h) — v1.1
- ✓ Google Calendar reminder payload support (backend/sync) — v1.1

### Active

See REQUIREMENTS.md v2.0 section for full Budget Tracker requirements.

**Target features:**
- Budget Tracker settings: 3 hourly rates, monthly hours per rate, ZUS + accounting cost deduction
- Net earnings calculation with 0.88 tax multiplier and flat cost deduction
- Additional household earnings (partner salary, ZUS child bonuses) per month
- Recurring monthly expenses and one-time expenses tracking
- 12-month year overview: monthly balance, running account total
- Initial bank account balance setting
- Current year scope (future years deferred)

### Out of Scope

- More than two concurrent users / team calendars — focus on household pair first
- Native mobile app — Google Calendar on phone handles mobile access via sync
- Full two-way Google Calendar sync as v1 — export/push covers the core need
- Event visibility controls (private vs shared) — deferred to next milestone
- Reminder UI in quick-entry form — backend ready, UI deferred
- Multi-year budget tracking — current year only for v2.0
- Excel data import for past months — optional, not required for v2.0
- Two-way sync between budget and calendar events

## Context

- Target users: two people in the same household (e.g., couple)
- Platform: Python web application
- Primary integration: Google Calendar / Google Workspace Calendar (OAuth + API)
- Event creation methods: manual UI, natural language text request, image/OCR extraction
- The user wants to see the calendar from a browser and get event reminders on their phone via Google Calendar's notification system

## Constraints

- **Tech stack**: Python — backend must be Python-based
- **Scope**: Two-user household calendar; no multi-tenancy in v1
- **Integration**: Google Calendar API (OAuth2) required for sync/export
- **User count**: Exactly two users per calendar instance for v1

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Python backend | User's stated tech preference | ✓ Implemented |
| Two-user model (not multi-user) | Simplest model that covers household use case | ✓ Implemented |
| Push sync to Google Calendar (not full two-way v1) | Reduces complexity; users read on phone via Google | ✓ Implemented |
| Image OCR for event extraction | Differentiating quick-add path with review safety | ✓ Implemented |
| Polish as default locale | Target user base is Polish-speaking household | ✓ Implemented |
| Cookie + query param locale cascade | Simple, stateless persistence without DB migration | ✓ Implemented |
| Bilingual keyword fallback in NLP | Users may mix Polish and English; always check both | ✓ Implemented |
| Day-click quick-entry vs full form | Parallel entry modes for speed vs control | ✓ Implemented |
| Backend-only reminder support | Ship reminder sync now, UI later when needed | ✓ Implemented |

| Budget Tracker as new feature module | New user need: household financial planning alongside calendar | Starting v2.0 |
| Current year only for budget | Simplest scope; future years deferred | v2.0 decision |
| Polish required, English optional (i18n) | Follow existing i18n if low effort; Polish-only acceptable | v2.0 decision |
| Flat ZUS + accounting costs | Same every month, configured once in settings | v2.0 decision |

---
*Last updated: 2026-03-20 after starting v2.0 Budget Tracker milestone*

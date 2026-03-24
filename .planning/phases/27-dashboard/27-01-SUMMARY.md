---
phase: 27-dashboard
plan: 01
status: complete
started: 2026-03-23
completed: 2026-03-23
---

# Plan 27-01 Summary: Dashboard Service, Routes, Template, Nav & i18n

## What was built

### Dashboard Service
- `app/dashboard/service.py` — `DashboardService` aggregating data from EventService, OverviewService, and ExpenseService
- `get_today_events()` — today's events sorted by start_at via `list_day_expanded`
- `get_week_preview()` — 7-day lookahead with max 3 events per day + overflow count
- `get_event_categories()` — category_id→EventCategory map for color rendering
- `get_budget_snapshot()` — current month balance, income, expenses from year overview
- `get_top_expense_categories()` — top 3 spending categories by total_amount

### Dashboard Route
- `app/dashboard/routes.py` — GET /dashboard HTML view with all 4 data sections
- Budget errors caught gracefully (has_data=False fallback)

### Calendar Page Route
- Added GET /calendar to `app/views/calendar_routes.py` to serve calendar.html now that "/" redirects

### Dashboard Template
- `app/templates/dashboard.html` — responsive 2-column grid (events left, budget right)
- Today's events with category color dots, time ranges, max 5 with "+N more" link
- 7-day preview with color-coded event pills, day names, overflow badges
- Budget snapshot with hero balance (green/red), income vs expenses boxes, top categories
- Quick-add buttons linking to /calendar and /budget/expenses
- Empty states for no events and no budget data

### Navigation Updates
- `app/templates/base.html` — "Home" link added as first desktop nav item
- Mobile bottom nav: Home icon (house) added as first item before Calendar

### Route Changes
- `main.py` — "/" now redirects 302 to /dashboard, dashboard_router registered
- Auth redirect handler updated to include /dashboard in 401→login redirect paths

### i18n
- 16 dashboard keys added to both `app/locales/en.json` and `app/locales/pl.json`
- Keys: nav_home, today_events, week_preview, budget_snapshot, quick_add, add_event, add_expense, no_events_today, no_events, more_events, view_overview, setup_budget, account_balance, income, expenses, top_categories

## Verification
- `python -c "from app.dashboard.service import DashboardService; from app.dashboard.routes import router; print('OK')"` → OK
- Dashboard template renders all 4 sections without errors
- Navigation shows Home link in both desktop and mobile

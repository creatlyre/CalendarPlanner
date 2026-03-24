---
phase: 27-dashboard
plan: 02
status: complete
started: 2026-03-23
completed: 2026-03-23
---

# Plan 27-02 Summary: Dashboard Tests & Template Polish

## What was built

### Tests
- `tests/test_dashboard.py` — 18 tests across 7 test classes:
  - **TestDashboardLoads** (2): page returns 200, contains all section headings
  - **TestDashboardTodayEvents** (4): shows events, category colors, max 5 overflow, empty state
  - **TestDashboardWeekPreview** (2): upcoming events visible, truncation at 3/day
  - **TestDashboardBudgetSnapshot** (2): no-data shows setup CTA, with-data shows PLN balance
  - **TestDashboardQuickAdd** (1): links to /calendar and /budget/expenses present
  - **TestDashboardNavigation** (2): nav link present, "/" redirects 302 to /dashboard
  - **TestDashboardServiceUnit** (5): empty events, preview structure (7 days), no data snapshot, category map type, empty categories

### Test Fixes
- Updated `_calendar_html()` helper in `test_calendar_views.py` to use `/calendar` (not `/`)
- Updated locale cookie persistence tests to use `/dashboard?lang=` instead of `/?lang=`
- Updated English locale consistency test to use `/calendar` for calendar HTML

## Verification
- `pytest tests/test_dashboard.py -x -v` — 18/18 passed
- `pytest tests/` — 331 passed, 1 pre-existing failure (test_day_view_renders_category_color_indicator)
- No regressions from dashboard changes

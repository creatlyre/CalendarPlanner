---
phase: 22-historical-year-import
plan: 01
subsystem: budget
tags: [bulk-import, tsv, api, ui]

requires:
  - phase: 21-year-over-year-comparison
    provides: YoY comparison endpoint and dashboard

provides:
  - POST /api/budget/income/hours/bulk endpoint for batch hour upserts
  - Import page at /budget/import with TSV paste for hours, one-time, and recurring expenses
  - Sidebar import link in all budget templates
  - i18n keys for EN and PL

affects: [budget, overview]

tech-stack:
  added: []
  patterns: [bulk-upsert-via-loop, client-side-tsv-parsing]

key-files:
  created:
    - app/templates/budget_import.html
    - tests/test_import.py
  modified:
    - app/budget/income_schemas.py
    - app/budget/income_routes.py
    - app/budget/income_service.py
    - app/budget/overview_views.py
    - app/templates/budget_overview.html
    - app/templates/budget_settings.html
    - app/templates/budget_income.html
    - app/templates/budget_expenses.html
    - app/locales/en.json
    - app/locales/pl.json

key-decisions:
  - "Reused existing POST /api/budget/expenses/bulk for expense imports (no new endpoint needed)"
  - "Client-side TSV parsing with preview before save"
  - "Year picker defaults to current year minus 1"

patterns-established:
  - "Bulk upsert pattern: service loops over entries calling existing single-upsert repo method"
  - "TSV import UI pattern: textarea → parse → preview table → save button"

requirements-completed: [IMP-01, IMP-02, IMP-03, IMP-04]

duration: 8min
completed: 2026-03-21
---

# Phase 22: Historical Year Import Summary

**Bulk import page for backfilling historical budget data via spreadsheet copy-paste, with YoY integration verified**

## Performance

- **Duration:** 8 min
- **Completed:** 2026-03-21
- **Tasks:** 3/3
- **Files modified:** 12

## Accomplishments
- Added BulkMonthlyHoursUpdate schema and POST /api/budget/income/hours/bulk endpoint
- Created /budget/import page with 3 TSV paste sections (hours, one-time expenses, recurring expenses), year picker, preview, and save
- Added sidebar import link to all 4 budget templates with EN/PL i18n
- Integration tests prove imported data flows correctly into YoY comparison
- Full regression suite passes (262 tests)

## Task Commits

1. **Task 1: Bulk hours import endpoint + schema** - `9f60cc5` (feat)
2. **Task 2: Import page UI with TSV parsing** - `0457de1` (feat)
3. **Task 3: Integration test — import and verify in YoY** - `46853fc` (test)

## Files Created/Modified
- `app/budget/income_schemas.py` - Added BulkMonthlyHoursUpdate schema
- `app/budget/income_routes.py` - Added POST /hours/bulk endpoint
- `app/budget/income_service.py` - Added bulk_save_hours method
- `app/budget/overview_views.py` - Added /budget/import route
- `app/templates/budget_import.html` - Full import page with TSV parsing JS
- `app/templates/budget_overview.html` - Added import sidebar link
- `app/templates/budget_settings.html` - Added import sidebar link
- `app/templates/budget_income.html` - Added import sidebar link
- `app/templates/budget_expenses.html` - Added import sidebar link
- `app/locales/en.json` - Added 17 import-related i18n keys
- `app/locales/pl.json` - Added 17 import-related i18n keys (Polish)
- `tests/test_import.py` - 5 tests: bulk hours CRUD + YoY integration

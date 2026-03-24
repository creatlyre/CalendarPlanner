# Quick Task 260324-tlt: Summary

**Task:** Refactor "Szybkie dodawanie" navbar button to open a chooser modal with quick-add options for Wydarzenie, Wydatek, and Zakupy

**Date:** 2026-03-24
**Commit:** 97ba386

## What Changed

### New: Quick-Add Chooser Modal (`app/templates/base.html`)
- Added `#qa-chooser-modal` — a glass-styled overlay with 3 vertically-stacked buttons:
  - **Wydarzenie / Event** (primary) → opens existing NLP quick-add event modal
  - **Wydatek / Expense** (info) → navigates to `/calendar?open=expense`
  - **Zakupy / Shopping** (secondary) → navigates to `/shopping`
- Closes on: X button, Escape key, backdrop click
- Wired to navbar `#qa-global-btn` and mobile FAB `#qa-fab`
- Calendar page inline `#qa-open-btn` still opens event modal directly (unchanged)

### i18n Keys Added (`app/locales/pl.json`, `app/locales/en.json`)
- `qa.chooser_title`: "Co chcesz dodać?" / "What do you want to add?"
- `qa.chooser_event`: "Wydarzenie" / "Event"
- `qa.chooser_expense`: "Wydatek" / "Expense"
- `qa.chooser_shopping`: "Zakupy" / "Shopping"

## Files Modified
- `app/templates/base.html` — chooser modal HTML + JS wiring
- `app/locales/pl.json` — 4 new keys
- `app/locales/en.json` — 4 new keys

## Verification
- 56 tests passing (test_pwa + test_dashboard)
- i18n keys in sync (0 mismatches between PL/EN)

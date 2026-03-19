# Phase 8 Research: Localization Foundation and Polish Default

**Phase:** 08
**Date:** 2026-03-19

## Problem Framing

Phase 8 must localize all current user-facing surfaces with Polish as default, while preparing bilingual resources for Phase 9 language switching.

## Existing Codebase Signals

- UI is server-rendered Jinja templates with large inline JavaScript blocks in `app/templates/calendar.html`.
- HTML root language is currently hardcoded as `en` in `app/templates/base.html`.
- Calendar month/day rendering currently uses English month names (`calendar.month_name`) and JavaScript locale defaults / `sv-SE` formatting markers.
- User-facing API error strings are hardcoded in `app/events/routes.py` and `app/auth/routes.py`.

## Recommended Technical Direction

1. Add a lightweight application-local i18n module (no new external dependency required for Phase 8).
2. Store translations in versioned JSON dictionaries (Polish + English) keyed by semantic identifiers.
3. Resolve locale via request helper with hard default `pl`; permit optional cookie read now to avoid refactor in Phase 9.
4. Inject `locale` and translation function into Jinja template context so both templates and inline scripts can use localized strings.
5. Replace hardcoded user-facing API `detail`/`message` strings with translation-key lookups.
6. Replace month/day/date rendering that depends on English names or `sv-SE` with locale-aware formatting that uses selected locale conventions.

## Risks and Mitigations

- Risk: Missing translation keys during template migration.
  - Mitigation: fallback to English key map and add explicit tests for critical marker strings.
- Risk: Breaking quick-add script behavior while replacing inline literals.
  - Mitigation: keep IDs and JS flow intact; only externalize display strings.
- Risk: Locale formatting drift between Python and JS paths.
  - Mitigation: centralize locale code mapping (`pl` -> `pl-PL`, `en` -> `en-US`) in one helper and test both day/month and quick-add outputs.

## Planning Implications

- Plan 08-01 should establish contracts: locale resolver + translation dictionaries + template wiring.
- Plan 08-02 should perform broad copy migration across templates and user-facing API messages.
- Plan 08-03 should focus on locale-aware date/time rendering and regression coverage.

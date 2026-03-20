# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.1 — Localization and Language Switching

**Shipped:** 2026-03-20
**Phases:** 4 | **Plans:** 10

### What Was Built
- Full i18n foundation with Polish default and English option (174 translation keys per locale)
- Language switcher UI with cookie/localStorage persistence across sessions
- Locale-aware NLP and OCR parsing with Polish keyword dictionaries and bilingual fallback
- Day-click quick-entry for rapid event creation with auto-calculated end-time (+1h)
- Google Calendar reminder payload support (multi-reminder, backward-compatible model)
- 145 tests passing across all subsystems

### What Worked
- Cookie + query param locale cascade was simple and required zero DB migrations
- Bilingual keyword fallback (always merge English + locale) meant Polish parsing worked immediately without breaking English
- Phase execution was fast (plans completed in 3-5 minutes each) with minimal rework
- VALIDATION.md per phase caught testing gaps early (Nyquist compliance)

### What Was Inefficient
- Backfilled SUMMARY.md files for Phase 08 after the fact — should have been created during execution
- Missing VERIFICATION.md for 3 of 4 phases — gsd-verifier wasn't run on phases 08-10
- Phase 9 SUMMARY frontmatter `requirements_completed` was empty — metadata discipline needs attention
- REQUIREMENTS.md checkboxes weren't updated until audit caught it

### Patterns Established
- `inject_template_i18n()` — single injection point for locale + translator into all template contexts
- Bilingual merge pattern: `{**DICT['en'], **DICT[locale]}` ensures English always works as fallback
- Quick-entry mode: parallel entry mode alongside full form for speed vs control trade-off
- `effective_reminders` property pattern: computed property with fallback chain on model

### Key Lessons
1. Run gsd-verifier on every phase during execution, not just the last one — process gaps accumulate
2. Keep SUMMARY frontmatter `requirements_completed` updated during plan execution, not as cleanup
3. Cookie-based locale persistence is sufficient for small-scale apps — no need for DB-backed preferences
4. Locale-aware NLP is achievable with keyword dictionaries; no need for separate parser models per language

### Cost Observations
- Model mix: ~80% sonnet, ~20% opus (verifier + integration checker)
- Notable: 4 phases completed in 2 days including all tests and validation

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Phases | Plans | Key Change |
|-----------|--------|-------|------------|
| v1.0 | 7 | 22 | Foundation — established GSD workflow, Nyquist validation |
| v1.1 | 4 | 10 | Faster execution, but verification discipline slipped for 3/4 phases |

### Cumulative Quality

| Milestone | Tests | Key Additions |
|-----------|-------|---------------|
| v1.0 | 117 | Auth, events, NLP, OCR, sync, calendar views |
| v1.1 | 145 | Locale integration, Polish NLP, day-click, reminder sync |

### Top Lessons (Verified Across Milestones)

1. Run verification on every phase — gaps compound and become audit blockers
2. Keep planning metadata current during execution, not as retroactive cleanup

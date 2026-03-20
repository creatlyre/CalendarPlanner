# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v2.0 (Phases 16-17) — Overview Detail & Performance

**Shipped:** 2026-03-20
**Phases:** 2 | **Plans:** 4

### What Was Built
- Accordion month detail in year overview — click any month to expand inline one-time expense CRUD
- Prebuilt Tailwind CSS (34KB) replacing CDN runtime dependency (~300KB)
- httpx connection pooling via singleton client in SupabaseStore
- Cache-Control headers on static assets (7-day cache)
- 8 new performance/validation tests, 230 total passing

### What Worked
- PERF-01 and PERF-02 were clean, self-contained changes that shipped without rework
- Nyquist validation tests caught the PERF-03 gap before milestone completion
- Integration checker correctly identified 7/8 requirements as wired
- Singleton pattern for httpx client was simple and effective

### What Was Inefficient
- Phase 16 missing SUMMARY.md files — no summaries were generated during execution
- Prior audit (v3.0) created fabricated VERIFICATION.md files with non-existent test names — required full re-audit
- PERF-03 (Cache-Control) was claimed as "passed" in stale VERIFICATION.md but never implemented — false positive
- REQUIREMENTS.md traceability table never updated for OMD/PERF requirements — checkboxes still unchecked
- v2.0 requirements (BSET/INC/EXP/YOV) still marked "Pending" in traceability despite being shipped

### Patterns Established
- `StaticCacheMiddleware` — BaseHTTPMiddleware for adding Cache-Control to static paths
- `_shared_client` singleton with `_get_shared_client()` for connection pooling
- Prebuilt CSS workflow: `input.css` → `npx @tailwindcss/cli build` → `public/css/style.css`

### Key Lessons
1. NEVER trust VERIFICATION.md files created retroactively — always verify against actual code and running tests
2. Fabricated test names in verification documents are a serious integrity issue — re-audit immediately
3. Cache-Control requires explicit middleware in FastAPI/Starlette — `StaticFiles` does NOT set it by default
4. Keep REQUIREMENTS.md traceability table updated per-phase, not at milestone close
5. Phase 16 worked perfectly despite missing SUMMARY.md — execution quality and process quality are separate

### Cost Observations
- Model mix: ~70% sonnet, ~30% opus (audit + integration checker + validation)
- Notable: 2 phases completed in 1 day, but audit/validation cycle added significant overhead due to stale artifacts

---

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
| v2.0 (12-15) | 4 | 10 | Budget feature module — clean execution, full test coverage |
| v2.0 (16-17) | 2 | 4 | Small scope, but stale verification artifacts caused significant audit overhead |

### Cumulative Quality

| Milestone | Tests | Key Additions |
|-----------|-------|---------------|
| v1.0 | 117 | Auth, events, NLP, OCR, sync, calendar views |
| v1.1 | 145 | Locale integration, Polish NLP, day-click, reminder sync |
| v2.0 (12-15) | 214 | Budget settings, income, expenses, year overview |
| v2.0 (16-17) | 230 | Month detail CRUD, CDN removal, pooling, cache headers |

### Top Lessons (Verified Across Milestones)

1. Run verification on every phase — gaps compound and become audit blockers
2. Keep planning metadata current during execution, not as retroactive cleanup
3. Never trust retroactively-generated VERIFICATION.md — always cross-reference with actual tests and code
4. Stale/fabricated process artifacts are worse than missing ones — they create false confidence

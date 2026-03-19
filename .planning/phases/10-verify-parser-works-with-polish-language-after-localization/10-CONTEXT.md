# Phase 10 Context: Verify parser works with Polish language after localization

**Phase:** 10  
**Depends on:** Phase 8, Phase 9  
**Requirements:** I18N-07  
**Goal:** Ensure NLP and OCR event parsing supports Polish language input (including diacritics) with parity to existing English parsing flows.

## Phase Boundary

### What This Phase Delivers

1. Locale-aware NLP parsing for Polish and English phrase sets
2. OCR parsing path that preserves and parses Polish diacritics (ą, ć, ę, ł, ń, ó, ś, ź, ż)
3. Automated tests proving Polish parser/OCR parity with existing English behavior

### What This Phase Does NOT Cover

- New UI components or interaction changes
- New translation catalog keys for templates
- Google sync behavior changes
- Parser redesign beyond locale support and OCR handoff hardening

## Implementation Decisions

### Locked Decisions

- Phase 10 MUST include OCR text handling for Polish characters and accents.
- Parser verification MUST cover both NLP text-input and OCR upload paths.
- Existing English parse behavior MUST remain backward compatible.

### Claude's Discretion

- Exact shape of locale dictionaries and helper function names.
- Whether OCR reader always loads both languages or locale-preferred order (must still parse both).
- How normalization handles OCR noise (for example, optional fallback tokens without diacritics).

## Canonical References

- `.planning/ROADMAP.md` - Phase 10 goal, dependencies, and plan tracking
- `.planning/REQUIREMENTS.md` - I18N-07 requirement definition and traceability
- `app/events/nlp.py` - Current parser implementation (English-oriented rules)
- `app/events/ocr.py` - OCR service and NLP handoff
- `app/events/routes.py` - Locale resolution and parse endpoints
- `tests/test_nlp.py` - Parser unit/regression tests
- `tests/test_events_api.py` - API and OCR endpoint tests

## Specific Ideas

- Add locale-aware dictionaries for relative dates, weekdays, months, recurrence keywords.
- Ensure title extraction and normalization retain Unicode letters.
- Pass request locale from route handlers into NLP and OCR parsing methods.
- Add Polish corpora examples with and without diacritics in tests.

## Deferred Ideas

- Full multilingual parser beyond Polish and English
- OCR engine replacement or model retraining
- Advanced spell-correction pipeline for OCR output

---

*Phase: 10-verify-parser-works-with-polish-language-after-localization*  
*Context gathered: 2026-03-19*

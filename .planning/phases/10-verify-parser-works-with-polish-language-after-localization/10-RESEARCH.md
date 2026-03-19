---
phase: 10-verify-parser-works-with-polish-language-after-localization
status: complete
researched: 2026-03-19
---

# Phase 10 Research

## Problem Summary

Current NLP and OCR parse paths are functionally correct for English, but parser rules are mostly English-keyword based.

Observed code reality:
- `app/events/nlp.py` uses English-only tokens for relative dates, months, weekdays, and recurrence keywords.
- `app/events/nlp.py` title cleanup strips non-ASCII letters via `[^A-Za-z\s]`.
- `app/events/ocr.py` initializes EasyOCR reader with `Reader(["en"], gpu=False)` only.
- `app/events/routes.py` resolves request locale but does not pass locale into NLP/OCR services.

## Technical Recommendations

1. Make NLP locale-aware without breaking current signatures for callers.
2. Preserve Unicode letters in title extraction so Polish diacritics survive cleanup.
3. Pass locale through parse endpoints: route -> NLPService/OCRService.
4. Make OCR reader locale-capable (Polish + English) and ensure NLP handoff gets the selected locale.
5. Expand tests in `tests/test_nlp.py` and `tests/test_events_api.py` with Polish phrases and diacritics.

## Risk Review

- Backward compatibility risk for existing English tests if regex/date handling changes too broadly.
- OCR runtime risk if EasyOCR language list changes unexpectedly; tests should monkeypatch OCR parse path to remain deterministic.
- Ambiguity in date phrases across locales; keep deterministic fixtures with `context_date`.

## Recommended Implementation Sequence

1. Locale contract and parser plumbing in `app/events/nlp.py` and `app/events/routes.py`.
2. OCR locale support and handoff plumbing in `app/events/ocr.py` and routes.
3. Add/expand tests for Polish NLP and OCR scenarios.
4. Run focused parser/OCR suites then regression subset.

## Validation Architecture

- Quick run command: `.venv\\Scripts\\python.exe -m pytest tests/test_nlp.py tests/test_events_api.py -q`
- Full suite command: `.venv\\Scripts\\python.exe -m pytest tests/ -q`
- Sampling target: run quick suite after each task, full suite at phase end.

## Expected Deliverables

- Locale-aware NLP parsing for Polish and English text input.
- OCR parse path handling Polish characters and accent-sensitive text.
- Automated tests proving I18N-07 acceptance behavior.

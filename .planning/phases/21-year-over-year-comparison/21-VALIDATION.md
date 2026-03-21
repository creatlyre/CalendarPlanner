---
phase: 21
slug: year-over-year-comparison
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-21
---

# Phase 21 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.4.3 |
| **Config file** | pyproject.toml (`[tool.pytest.ini_options]`) |
| **Quick run command** | `python -m pytest tests/test_overview.py -x -q` |
| **Full suite command** | `python -m pytest tests/ -x -q` |
| **Estimated runtime** | ~0.4 seconds (overview), ~4 seconds (full) |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_overview.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -x -q`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 4 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 21-01-01 | 01 | 1 | BUD-04 | integration | `python -m pytest tests/test_overview.py::TestYearOverYearComparison -x -q` | ✅ | ✅ green |
| 21-01-02 | 01 | 1 | BUD-04 | page-render | `python -m pytest tests/test_overview.py::TestOverviewPage -x -q` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Requirement Coverage Detail

### BUD-04: Year-over-year comparison summary

| Behavior | Test(s) | Status |
|----------|---------|--------|
| API returns selected + previous year data | `test_comparison_returns_both_years` | ✅ |
| Response contains all 6 required metric keys | `test_comparison_has_required_keys` | ✅ |
| Delta = selected − previous (for all metrics) | `test_comparison_delta_is_selected_minus_previous` | ✅ |
| Previous year with no data returns valid values | `test_comparison_previous_year_has_valid_data` | ✅ |
| Endpoint requires authentication | `test_comparison_requires_auth` | ✅ |
| Overview page renders successfully | `test_overview_page_renders` | ✅ |
| Delta color indicators (green/red) | — | 🔧 Manual-only |
| Comparison updates on year navigation | — | 🔧 Manual-only |

**Automated coverage:** 6/8 behaviors (75%)
**Total coverage (incl. manual):** 8/8 behaviors (100%)

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements.

- Test framework: pytest (pre-existing)
- Fixtures: `authenticated_client`, `test_db`, `test_user_a`, `test_client` (pre-existing in conftest.py)
- Helper: `_seed_settings()` (pre-existing in test_overview.py)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Delta indicators show green (▲) for improvement and red (▼) for decline; expense rows use inverted logic | BUD-04 | Client-side JS rendering logic; no browser testing framework (Playwright/Selenium) in project | 1. Navigate to Budget Overview page. 2. Ensure data exists for current and previous year. 3. Verify ▲ green arrows on income rows where current > previous. 4. Verify ▼ red arrows on expense rows where current > previous (inverted = more spending is bad). 5. Verify — gray dashes when values are equal. |
| Comparison card updates when year picker arrows are clicked | BUD-04 | Client-side JS event handler + async fetch; no browser testing infrastructure | 1. Navigate to Budget Overview. 2. Click year-next arrow. 3. Verify comparison card reloads with new year's data. 4. Click year-prev arrow. 5. Verify comparison updates again. 6. Navigate to a year with no prior data — card should still render with zero/empty previous. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 4s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-03-21

---

## Validation Audit 2026-03-21

| Metric | Count |
|--------|-------|
| Behaviors analyzed | 8 |
| Automated (COVERED) | 6 |
| Manual-only | 2 |
| Gaps (fixable) | 0 |
| Escalated | 0 |

**Source:** Reconstructed from 21-01-PLAN.md + 21-01-SUMMARY.md (State B — no prior VALIDATION.md)

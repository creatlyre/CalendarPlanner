---
phase: 31
slug: self-hosted
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-23
---

# Phase 31 — Validation Strategy

> Per-phase validation contract for paid self-hosted distribution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `python -m pytest tests/test_licensing.py -x -q` |
| **Full suite command** | `python -m pytest tests/test_licensing.py -v` |
| **Estimated runtime** | ~0.1 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_licensing.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/test_licensing.py -v`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 1 second

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 31-01-01 | 01 | 1 | SHS-02 | unit | `pytest tests/test_licensing.py::TestGenerateLicenseKey` | ✅ | ✅ green |
| 31-01-01 | 01 | 1 | SHS-02 | unit | `pytest tests/test_licensing.py::TestValidateLicenseKey` | ✅ | ✅ green |
| 31-01-02 | 01 | 1 | SHS-02 | integration | `pytest tests/test_licensing.py::TestLicenseCheckMiddleware` | ✅ | ✅ green |
| 31-01-02 | 01 | 1 | SHS-01 | file check | `Test-Path self-hosted/docker-compose.yml` | ✅ | ✅ green |
| 31-02-01 | 02 | 2 | SHS-02 | unit | `pytest tests/test_licensing.py -v` (18 tests) | ✅ | ✅ green |
| 31-02-02 | 02 | 2 | SHS-04 | file check | `Test-Path self-hosted/README.md` | ✅ | ✅ green |
| 31-02-02 | 02 | 2 | SHS-03 | file check | `Test-Path self-hosted/UPGRADE.md` | ✅ | ✅ green |
| 31-02-02 | 02 | 2 | SHS-03 | file check | `Test-Path self-hosted/CHANGELOG-SELFHOSTED.md` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements. tests/test_licensing.py created during phase execution (Plan 31-02, Task 1).*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Docker Compose starts all 4 services | SHS-01 | Requires Docker daemon | `cd self-hosted && docker compose up -d` — verify app, db, rest, caddy running |
| Setup guide is comprehensible | SHS-04 | Requires human reading | Follow self-hosted/README.md from scratch on a clean machine |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 1s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-03-23

---

## Validation Audit 2026-03-23

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

Phase 31 already had 18 tests in tests/test_licensing.py (created during execution). All pass. Self-hosted documentation files verified present.

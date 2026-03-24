---
phase: 29
slug: billing
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-23
---

# Phase 29 — Validation Strategy

> Per-phase validation contract for billing, plans, and entitlements.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `python -m pytest tests/test_billing.py -x -q` |
| **Full suite command** | `python -m pytest tests/test_billing.py -v` |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_billing.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/test_billing.py -v`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 29-01-01 | 01 | 1 | SAS-02 | unit | `pytest tests/test_billing.py::TestBillingRepository` | ✅ | ✅ green |
| 29-01-01 | 01 | 1 | SAS-02 | schema | `pytest tests/test_billing.py::TestSupabaseSchemaCompliance` | ✅ | ✅ green |
| 29-01-02 | 01 | 1 | SAS-03 | unit | `pytest tests/test_billing.py::TestBillingRoutes::test_webhook_endpoint_exists` | ✅ | ✅ green |
| 29-01-02 | 01 | 1 | SAS-02 | unit | `pytest tests/test_billing.py::TestBillingServiceLogic` | ✅ | ✅ green |
| 29-01-02 | 01 | 1 | SAS-06 | unit | `pytest tests/test_billing.py::TestBillingRepository::test_log_billing_event` | ✅ | ✅ green |
| 29-02-01 | 02 | 2 | SAS-04 | integration | `pytest tests/test_billing.py::TestEntitlementDependencies` | ✅ | ✅ green |
| 29-02-01 | 02 | 2 | SAS-05 | integration | `pytest tests/test_billing.py::TestBillingViews` | ✅ | ✅ green |
| 29-02-02 | 02 | 2 | SAS-04 | integration | `pytest tests/test_billing.py::TestEntitlementDependencies::test_free_user_can_access_core_features` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Stripe Verification (MCP-verified)

| Entity | Stripe ID | Status |
|--------|-----------|--------|
| Synco Pro product | `prod_UCaotXOG9ipoY2` | ✅ exists |
| Synco Family Plus product | `prod_UCaojfikOxH9SB` | ✅ exists |
| Pro monthly price (19.99 PLN) | `price_1TEBccFf0OCpe7nWJMCTj6UV` | ✅ exists |
| Family Plus monthly price (34.99 PLN) | `price_1TEBchFf0OCpe7nW0E7VQXMD` | ✅ exists |
| Test customer | `cus_UCdRb6lb7RacHO` | ✅ exists |

## Supabase Schema (MCP-verified)

| Table | Columns | RLS | Status |
|-------|---------|-----|--------|
| subscriptions | id, user_id, stripe_customer_id, stripe_subscription_id, plan, status, current_period_end, cancel_at_period_end, created_at, updated_at | ✅ | ✅ created |
| billing_events | id, user_id, event_type, plan, stripe_event_id, metadata, created_at | ✅ | ✅ created |

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements. InMemoryStore extended with subscriptions and billing_events tables.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Stripe Checkout redirects to payment page | SAS-02 | Requires browser + real Stripe session | Click upgrade button on /billing/settings, verify redirect to Stripe |
| Stripe Portal manages subscription | SAS-05 | Requires active Stripe subscription | Subscribe, then click "Manage Subscription" on /billing/settings |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-03-23

---

## Validation Audit 2026-03-23

| Metric | Count |
|--------|-------|
| Gaps found | 5 |
| Resolved | 5 |
| Escalated | 0 |

Created tests/test_billing.py with 52 tests + 5 live Stripe API tests (skipped without key).
Supabase migration applied — subscriptions and billing_events tables created.
Stripe products, prices, and test customer verified via MCP.

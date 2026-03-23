---
phase: 29-billing
plan: 01
subsystem: billing
tags: [stripe, subscriptions, webhooks, checkout, billing-events]

requires: []
provides:
  - Subscription and BillingEvent dataclasses in models.py
  - BillingRepository with get/upsert_subscription and log_billing_event
  - BillingService with Stripe checkout, portal, and webhook handling
  - Billing routes (POST /api/billing/checkout, /webhook, /portal)
  - Supabase migration for subscriptions + billing_events tables
affects: [29-02, 30-saas, 33-launch]

tech-stack:
  added: [stripe>=8.0.0]
  patterns:
    - "Stripe Checkout Session redirect flow for subscription creation"
    - "Webhook signature verification with stripe.Webhook.construct_event"
    - "Billing event logging for SaaS analytics"

key-files:
  created:
    - app/billing/__init__.py
    - app/billing/schemas.py
    - app/billing/repository.py
    - app/billing/service.py
    - app/billing/routes.py
    - supabase/migrations/20260323_billing.sql
  modified:
    - app/database/models.py
    - config.py
    - requirements.txt
    - main.py
    - app/middleware/auth_middleware.py

key-decisions:
  - "Stripe products/prices created via MCP: Pro (price_1TEBccFf0OCpe7nWJMCTj6UV, 19.99 PLN/mo), Family Plus (price_1TEBchFf0OCpe7nW0E7VQXMD, 34.99 PLN/mo)"
  - "Webhook handles 4 event types: checkout.session.completed, customer.subscription.updated, customer.subscription.deleted, invoice.payment_failed"
  - "User-subscription is 1:1 (user_id UNIQUE on subscriptions table)"
  - "Billing events table logs all subscription lifecycle changes for SAS-06 analytics"

patterns-established:
  - "BillingRepository follows same SupabaseStore pattern as NotificationRepository"
  - "BillingService encapsulates all Stripe API calls with proper error logging"
  - "Webhook endpoint is public (no auth), uses Stripe signature verification"

requirements-completed:
  - SAS-02
  - SAS-03
  - SAS-06

duration: 8min
completed: 2026-03-23
---

# Plan 29-01: Billing Data Model, Stripe Checkout, and Webhook Handler

**Integrated Stripe subscription billing with checkout, webhook processing, and billing event analytics.**

## Performance

- **Duration:** 8 min
- **Tasks:** 2/2 completed
- **Files created:** 6, modified: 5

## Accomplishments
- Created Supabase migration with subscriptions + billing_events tables (RLS, indexes)
- Added Subscription and BillingEvent dataclasses to models.py
- Built BillingRepository with subscription CRUD and billing event logging
- Created BillingService with Stripe checkout session, portal session, and 4-event webhook handler
- Registered 3 billing API routes (checkout, webhook, portal) in main.py
- Stripe products created via MCP: Synco Pro (19.99 PLN/mo) and Synco Family Plus (34.99 PLN/mo)

## Task Commits

1. **Task 1: Billing data model and Supabase migration** — `0e528a0` (feat)
2. **Task 2: Stripe checkout and webhook endpoints** — `aee5b4d` (feat)

## Files Created/Modified
- `supabase/migrations/20260323_billing.sql` — subscriptions + billing_events tables with RLS
- `app/billing/__init__.py` — Module init
- `app/billing/schemas.py` — CheckoutRequest, SubscriptionInfo, BillingEventCreate
- `app/billing/repository.py` — BillingRepository (SupabaseStore pattern)
- `app/billing/service.py` — BillingService (Stripe checkout, portal, webhook handling)
- `app/billing/routes.py` — POST /api/billing/checkout, /webhook, /portal
- `app/database/models.py` — Added Subscription, BillingEvent dataclasses
- `config.py` — Added STRIPE_* config vars
- `requirements.txt` — Added stripe>=8.0.0
- `main.py` — Registered billing_router
- `app/middleware/auth_middleware.py` — Added /api/billing/webhook to public routes

## Decisions Made
- Created Stripe products/prices via MCP Stripe tools (live mode)
- Webhook endpoint uses raw body + signature verification (no auth middleware)
- User ID resolved from metadata first, then stripe_customer_id lookup fallback

## Deviations from Plan
None — plan executed exactly as written.

## Issues Encountered
None.

# Phase 29: Billing, Plans, and Entitlements Core - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Integrate subscription billing, define the plan model (Free / Pro / Family Plus), implement entitlement checks that gate premium features in backend and UI, provide a billing portal from app settings, and capture basic SaaS analytics events. This phase focuses on the billing and entitlement **core** — production deployment and operations belong to Phase 30.

Requirements addressed: SAS-02, SAS-03, SAS-04, SAS-05, SAS-06.

</domain>

<decisions>
## Implementation Decisions

### Billing Provider
- **Stripe** is the billing provider (not Paddle).
- Rationale: best Python SDK (`stripe` package), industry standard, most documentation/examples, full control over checkout UX, Stripe Customer Portal for self-service billing management.
- Webhook handling for subscription lifecycle events (checkout.session.completed, customer.subscription.updated, customer.subscription.deleted, invoice.payment_failed).
- Stripe Checkout Sessions for subscription creation (redirect flow — no embedded form needed for v4.0).
- Stripe Customer Portal for plan changes, cancellations, and invoice history (SAS-05).

### Plan Structure & Feature Gating
- Three tiers as defined in MONETIZATION.md: **Free**, **Pro**, **Family Plus**.
- **Freemium model** — Free tier is always available (not a time-limited trial). Users upgrade when they want premium features.
- Plan stored on user/calendar level in Supabase with a `subscription_plan` field (e.g., `free`, `pro`, `family_plus`).
- Stripe Product + Price objects map to plan tiers. Plan ID stored alongside Stripe customer/subscription IDs.
- Feature gating examples (to be finalized in planning):
  - Free: core calendar + budget, 1 custom category, basic shopping list.
  - Pro: unlimited categories, expense charts, advanced NLP/OCR, priority support.
  - Family Plus: everything in Pro + extended storage, email notification alerts, priority email support.

### Entitlement Architecture
- **FastAPI dependency injection** pattern, matching existing `get_current_user` — a new `get_current_plan` or enriched user dependency that includes the active plan.
- Backend entitlement check via a reusable dependency (e.g., `require_plan("pro")`) that returns 403 if the user's plan is insufficient.
- UI entitlement: Jinja2 template context includes `user_plan` so templates can conditionally show/hide premium features and display upgrade prompts.
- No client-side-only gating — all entitlement enforcement happens server-side. UI hints are progressive disclosure only.

### Analytics & Conversion Flow
- **Stripe webhooks + Supabase event log table** for SAS-06 analytics.
- Track key events: `signup`, `trial_start` (if trial ever added), `subscribe`, `plan_change`, `cancel`, `churn` (subscription ended).
- Simple `billing_events` table: `id`, `user_id`, `event_type`, `plan`, `stripe_event_id`, `metadata`, `created_at`.
- No external analytics service in v4.0 — query directly from Supabase for initial metrics.

### Claude's Discretion
- Database schema design for subscriptions/billing tables (column names, indexes).
- Stripe webhook signature verification implementation details.
- Error handling and retry logic for Stripe API calls.
- Specific Stripe API version to pin.
- How to structure the billing settings page layout.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Licensing & Monetization Model
- `COMMERCIAL-LICENSE.md` — Dual-license commercial terms (SaaS + self-hosted paths)
- `MONETIZATION.md` — Free vs paid model, tier descriptions, AGPL obligations FAQ
- `LICENSE` — AGPL-3.0 full text

### Phase 28 Deliverables
- `.planning/phases/28-licensing/28-01-SUMMARY.md` — Commercial license and monetization docs created
- `.planning/phases/28-licensing/28-02-SUMMARY.md` — LICENSE verification and README licensing section
- `.planning/phases/28-licensing/28-RESEARCH.md` — AGPL-3.0 dual-licensing research

### Requirements
- `.planning/REQUIREMENTS.md` — SAS-01 through SAS-06, plan tier definitions, traceability matrix

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app/auth/dependencies.py` → `get_current_user` dependency: pattern to extend with plan-aware user model. Returns `User` or `AuthenticatedUser` with `id`, `email`, `name`, `calendar_id`.
- `app/middleware/auth_middleware.py` → `SessionValidationMiddleware`: pattern for request-level checks. Could inform entitlement middleware if needed.
- `app/database/supabase_store.py` → `SupabaseStore`: all DB operations go through this Supabase REST client with httpx pooling. New billing tables will use same pattern.
- `config.py` → `Settings(BaseSettings)`: pydantic-settings with `.env` — add `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PUBLISHABLE_KEY` here.

### Established Patterns
- **FastAPI dependency injection** for auth (`get_current_user`) — extend for plan checks.
- **SupabaseStore** for all data access — no SQLAlchemy/ORM, direct REST API via httpx.
- **Jinja2 templates** with i18n context injection (`inject_template_i18n`) — plan info follows same pattern.
- **Router modules** per feature domain (e.g., `app/budget/routes.py`, `app/shopping/routes.py`) — billing gets `app/billing/` module.
- **Dataclass models** in `app/database/models.py` — add `Subscription` dataclass here.

### Integration Points
- `app/database/models.py` → Add `subscription_plan`, `stripe_customer_id`, `stripe_subscription_id` fields to User model or create separate Subscription model.
- `main.py` → Register new billing router, add Stripe webhook endpoint.
- `app/templates/base.html` → Add billing/settings link in navigation for logged-in users.
- `app/locales/en.json` + `app/locales/pl.json` → Add billing-related i18n keys.

</code_context>

<specifics>
## Specific Ideas

- Stripe Checkout Session with redirect (not embedded) — simpler integration, Stripe hosts the payment page.
- Stripe Customer Portal for self-service billing management (SAS-05) — link from app settings page, no need to build custom billing UI.
- Webhook endpoint at `/api/billing/webhook` with Stripe signature verification.
- Plan info visible on dashboard or settings page showing current plan + upgrade CTA for free users.

</specifics>

<deferred>
## Deferred Ideas

- Annual billing discount (post-v4.0 experiment).
- Coupon/promo code support — not needed for launch.
- Usage-based billing — not applicable for household app.
- Self-hosted license key verification — Phase 31 scope (SHS-02).
- Stripe Tax / automatic tax calculation — can add later if needed.

</deferred>

---

*Phase: 29-billing*
*Context gathered: 2026-03-23*

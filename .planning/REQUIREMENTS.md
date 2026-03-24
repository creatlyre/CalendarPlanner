# Requirements: CalendarPlanner

**Defined:** 2026-03-23
**Milestone:** v4.0 Monetization Foundation
**Scope Choice:** Option 3 (Both - SaaS primary + self-hosted purchase option)
**Core Value:** Keep the product open-source and trustworthy while creating a clear path to recurring and one-time revenue.

## v4.0 Requirements

### Licensing and Commercial Model

- [ ] **MON-01**: Repository license is AGPL-3.0 for the core product.
- [ ] **MON-02**: Commercial license exception terms are defined for customers who need non-AGPL use.
- [ ] **MON-03**: Monetization docs clearly explain what is free, what is paid, and obligations for hosted modified versions.

### SaaS Productization (Primary)

- [ ] **SAS-01**: Hosted deployment path exists (staging + production) with environment-based configuration.
- [ ] **SAS-02**: Subscription billing provider integrated (Stripe or Paddle) with webhook handling.
- [ ] **SAS-03**: Plan model implemented (for example: Free, Pro, Family Plus).
- [ ] **SAS-04**: Entitlement checks gate premium features in backend and UI.
- [ ] **SAS-05**: Account billing portal is accessible from app settings.
- [ ] **SAS-06**: Basic SaaS analytics are captured (signup, trial start, subscribe, churn).

### Self-Hosted Commercial Package (Secondary)

- [ ] **SHS-01**: Docker Compose production package exists for paid self-hosted buyers.
- [ ] **SHS-02**: License-key or purchase-token verification flow exists for commercial self-hosted distribution.
- [ ] **SHS-03**: Versioned upgrade path exists for self-hosted customers (release notes + migration instructions).
- [ ] **SHS-04**: Buyer-facing setup guide is complete and reproducible.

### Mobile Distribution Strategy

- [ ] **MOB-01**: Web app is hardened as installable PWA (manifest, icons, install prompt, offline shell for key pages).
- [ ] **MOB-02**: Android wrapper distribution path is defined and tested (e.g., Trusted Web Activity or Capacitor).
- [ ] **MOB-03**: Native iOS/Android full rewrite is explicitly deferred pending monetization validation.

### Go-to-Market and Sales Readiness

- [ ] **GTM-01**: Pricing page defines SaaS tiers and self-hosted one-time package.
- [ ] **GTM-02**: Landing page communicates value proposition for couples/households and includes conversion CTA.
- [ ] **GTM-03**: Checkout flow works for both recurring SaaS and one-time self-hosted purchase.
- [ ] **GTM-04**: Legal basics are published (terms, privacy, refund policy).
- [ ] **GTM-05**: Launch checklist exists with measurable success criteria for first 30 days.

## Platform Choice (Web vs Android vs Native Mobile)

**Chosen implementation order for v4.0:**

1. Web app SaaS (primary revenue channel)
2. Paid self-hosted package (secondary one-time revenue)
3. Mobile access through PWA + Android wrapper only

**Rationale:**
- Web SaaS has the fastest path to paid conversion and easiest iteration on pricing/packaging.
- Self-hosted package captures privacy-focused buyers without forcing full managed-service dependency.
- Full native mobile app would delay monetization and increase maintenance burden too early.

## Out of Scope (v4.0)

- Full native iOS app
- Full native Android app rewrite
- Team/multi-tenant organizations beyond two-person household model
- Enterprise SSO and advanced compliance certifications

## Traceability (Requirements -> Planned Phases)

| Requirement | Phase | Planned Status |
|-------------|-------|----------------|
| MON-01, MON-02, MON-03 | 28 | Planned |
| SAS-01, SAS-02, SAS-03, SAS-04, SAS-05, SAS-06 | 29-30 | Planned |
| SHS-01, SHS-02, SHS-03, SHS-04 | 31 | Planned |
| MOB-01, MOB-02, MOB-03 | 32 | Planned |
| GTM-01, GTM-02, GTM-03, GTM-04, GTM-05 | 33 | Planned |

---
*Last updated: 2026-03-23 for v4.0 milestone initialization*

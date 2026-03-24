# Phase 33: Go-to-Market, Pricing, and Launch Funnel - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning
**Source:** Auto mode (--auto) — deep research with Todoist/Notion/Coda pricing analysis, HubSpot landing page best practices, GHCR/GitHub Actions CI/CD docs, and legal template research

<domain>
## Phase Boundary

Phase 33 delivers everything needed to ship Synco to real paying users: a pricing page with SaaS tiers and self-hosted option, a landing page with value proposition and conversion CTA, working checkout flow for both recurring and one-time purchases, legal pages (terms, privacy, refund), Docker image publishing via CI/CD, and a launch checklist with 30-day success criteria.

Requirements addressed: GTM-01, GTM-02, GTM-03, GTM-04, GTM-05.

**What is NOT in scope:**
- Play Store listing/submission (documented in Phase 32, deferred post-launch)
- Marketing campaigns, SEO optimization, or paid advertising
- Analytics beyond basic Stripe/billing events already in Phase 29
- A/B testing infrastructure
- Custom domain setup (Railway handles this via dashboard)

</domain>

<decisions>
## Implementation Decisions

### Pricing Page Design & Amounts — LOCKED
- **Three-column card layout** matching existing app dark theme (#0f0a2e background, indigo accents)
- Pricing in **PLN (Polish Zloty)** as primary currency — target audience is Polish households
- **Monthly and annual toggle** — annual billing at ~17% discount (2 months free pattern, industry standard from Todoist/Notion)
- Tier pricing (researched against Todoist 19 PLN/mo Pro, Notion €9.50/mo Plus):

  | Tier | Monthly | Annual (per month) | Annual total |
  |------|---------|-------------------|-------------|
  | **Free** | 0 zł | — | — |
  | **Pro** | 19 zł | 15 zł | 180 zł |
  | **Family Plus** | 29 zł | 24 zł | 288 zł |
  | **Self-Hosted** | — | — | 199 zł one-time |

- Free tier: core calendar + budget, 1 custom category per type, basic shopping list
- Pro tier: unlimited categories, expense charts, NLP/OCR, priority support, email notifications
- Family Plus: everything in Pro + extended storage, all premium features, priority email support
- Self-hosted: shown as a separate card below the SaaS tiers with "One-time purchase" badge
- **Pro tier highlighted as "Recommended"** with accent border (industry standard from Notion's "Recommended" badge)
- Feature comparison table below the cards (collapsible accordion, following Todoist pattern)
- "Start for free" as primary CTA on Free tier, "Get started" on paid tiers
- Self-hosted card links to checkout for one-time Stripe payment, then delivers license key + Docker access docs
- Page route: `/pricing` — public, no auth required

### Landing Page Scope & Tone — LOCKED
- **Minimal but complete landing page** — NOT a full marketing site. Single scrollable page with sections:
  1. **Hero**: Headline + subtitle + CTA + app screenshot/mockup
  2. **Features**: 4-6 feature cards (calendar, budget, shopping, notifications, sync, categories)
  3. **How It Works**: 3-step visual (Sign up → Add partner → Stay in sync)
  4. **Pricing**: Embedded pricing section (same content as /pricing standalone page)
  5. **Footer**: Legal links + contact
- **Benefit-first headline**: "Jeden kalendarz dla dwojga" (PL) / "One calendar for two" (EN) — clear value prop in hero
- **Bilingual**: Full PL + EN via existing i18n system (locale cookie, same as rest of app)
- **Target audience**: Polish couples/households primarily, but landing page works in English too
- **Tone**: Warm, personal, practical — NOT corporate. Speaks to real couples managing a household together
- **No navigation menu** on landing page (remove distractions per best practices). Just logo + "Zaloguj się"/"Sign in" link
- **Social proof section**: Skip for v1 launch (no testimonials yet). Add a "Trusted by X households" counter later
- **Page route**: Root `/` for unauthenticated users. Authenticated users get redirected to `/dashboard` (existing behavior)
- **Mobile-first responsive** — most couples will discover this on phone
- **No autoplay media** — static app screenshot or simple CSS illustration in hero
- Built as Jinja2 template (landing.html) using existing SSR stack — NOT a separate static site

### Checkout Flow — LOCKED
- **SaaS checkout**: Existing Stripe Checkout Session redirect flow from Phase 29 — no changes needed to the billing backend
- Pricing page "Get started" buttons create a Stripe Checkout Session with the correct Price ID and redirect
- After successful checkout, Stripe webhook updates the user's plan (already implemented in Phase 29)
- **Self-hosted checkout**: Stripe Checkout Session in `payment` mode (one-time) instead of `subscription` mode
- After self-hosted purchase completes:
  1. Webhook fires `checkout.session.completed` with `mode=payment`
  2. Backend generates HMAC license key (using existing `app.licensing.generate`)
  3. License key + setup instructions delivered via Stripe Checkout success page and/or confirmation email
- **No custom checkout UI** — Stripe Checkout handles payment form, card validation, SCA/3DS. Keeps PCI scope minimal
- Stripe Price IDs configured via environment variables (STRIPE_PRICE_PRO_MONTHLY, STRIPE_PRICE_PRO_ANNUAL, etc.)

### Legal Pages — LOCKED
- **Three legal pages**: Terms of Service, Privacy Policy, Refund/Cancellation Policy
- **Plain language, not heavy legalese** — written for real people, matching Synco's warm tone
- **Governing law: Polish law** (Polish Civil Code, GDPR via EU regulation) — developer and target users are Polish
- **GDPR compliance**: Data processing basis stated (contract performance for account data, consent for optional email notifications), data subject rights section (access, rectification, deletion, portability), data retention periods, no data sold to third parties
- **Cookie disclosure**: Minimal — Synco uses session cookies for auth only, no third-party tracking cookies. Brief cookie section in privacy policy rather than a separate cookie banner/policy
- **Refund policy**: 14-day money-back guarantee for SaaS subscriptions (EU consumer right for digital services). Self-hosted license: no refund after key delivery (license key is non-returnable digital good, but offer pre-purchase demo via free tier)
- **Contact**: email address (support@synco.app or similar) for privacy/legal inquiries
- Pages built as Jinja2 templates, route: `/terms`, `/privacy`, `/refund`
- Bilingual (PL/EN) via existing i18n, with Polish as the legally binding version
- **NOT using a legal generator service** — write concise, app-specific pages. Can be reviewed by a lawyer later. These are sufficient for launch
- Footer links on all app pages (terms, privacy, refund) — standard placement

### Docker Registry & CI/CD — LOCKED
- **GitHub Container Registry (GHCR)** — not Docker Hub
  - Free for public packages (matches AGPL open-source model)
  - Integrated with GitHub Actions via `GITHUB_TOKEN` — no separate credentials needed
  - Package URL: `ghcr.io/OWNER/synco:tag`
  - OCI labels in Dockerfile: `org.opencontainers.image.source`, `org.opencontainers.image.description`, `org.opencontainers.image.licenses=AGPL-3.0-only`
- **GitHub Actions workflow** triggered on:
  - Git tag push matching `v*` pattern (e.g., `v4.0.0`)
  - Builds multi-platform image (linux/amd64 only for now — ARM64 can be added later)
  - Tags: `latest`, version tag (e.g., `4.0.0`), major version (e.g., `4`)
- **Public image** — anyone can pull. License enforcement is at runtime via `LicenseCheckMiddleware` (Phase 31), NOT at image level. This is consistent with the AGPL model: source and images are open, commercial buyers get a license key for banner-free experience
- **Update self-hosted docker-compose.yml** to reference `ghcr.io/OWNER/synco:latest` instead of local build
- **Workflow file**: `.github/workflows/docker-publish.yml`
- Steps: checkout → setup Docker Buildx → login to GHCR → build & push → (optional) create GitHub Release

### Launch Checklist (GTM-05) — LOCKED
- Create `LAUNCH.md` in project root with:
  - Pre-launch checklist (env vars configured, Stripe products created, domain set, legal pages live, Docker image pushed)
  - Day-1 actions (announce on relevant channels, monitor error tracking, check webhook delivery)
  - 30-day success criteria:
    - At least 1 paying subscriber (proof of conversion)
    - Self-hosted package download/purchase (proof of distribution path)
    - Zero critical bugs in production
    - PWA installable on Android and desktop
  - Post-launch monitoring (Sentry errors, Stripe webhooks, health endpoint)
- This is a documentation task, not code

### Claude's Discretion
- Exact Stripe Price ID environment variable naming
- Landing page screenshot/illustration approach (CSS-only vs static image)
- GitHub Actions workflow details (caching, build args)
- Legal page section ordering and exact clause wording
- Whether to include FAQ section on pricing page

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Project vision, key decisions, requirement status
- `.planning/REQUIREMENTS.md` — GTM-01 through GTM-05 definitions
- `MONETIZATION.md` — Pricing model, tiers, AGPL obligations, mobile strategy

### Prior Phase Artifacts
- `.planning/phases/29-billing/29-01-SUMMARY.md` — Stripe checkout, webhook, plan model implementation
- `.planning/phases/29-billing/29-02-SUMMARY.md` — Entitlement gating, billing settings UI
- `.planning/phases/30-saas-production/30-01-SUMMARY.md` — Dockerfile, Railway deployment
- `.planning/phases/31-self-hosted/31-01-SUMMARY.md` — License key system, Docker Compose package
- `.planning/phases/31-self-hosted/31-02-SUMMARY.md` — Setup guide, license tests

### Existing Code
- `app/billing/routes.py` — Stripe checkout session creation, webhook handler, portal
- `app/billing/views.py` — Billing settings page
- `app/billing/schemas.py` — Billing data models
- `app/licensing/keys.py` — HMAC license key generation/validation
- `app/licensing/generate.py` — CLI license key generation
- `app/templates/base.html` — Base template with nav, footer, theme
- `app/templates/billing_settings.html` — Existing billing UI
- `self-hosted/docker-compose.yml` — Self-hosted Docker Compose (needs image reference update)
- `Dockerfile` — Multi-stage build for production
- `COMMERCIAL-LICENSE.md` — Commercial license terms
- `config.py` — Environment variable settings

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app/billing/routes.py`: Stripe Checkout Session creation already exists — extend for one-time payment mode
- `app/billing/service.py`: BillingService with plan management — add self-hosted purchase handling
- `app/licensing/generate.py`: License key CLI — reuse for automated key generation on purchase
- `app/templates/base.html`: Dark theme base template with nav — landing page can extend or standalone
- `app/i18n.py`: i18n injection for Jinja2 templates — all new pages get bilingual support automatically
- `app/locales/en.json` + `app/locales/pl.json`: Locale files — add new keys for pricing/landing/legal

### Established Patterns
- **SSR with Jinja2**: All pages render server-side with HTMX enhancements — landing/pricing/legal follow this pattern
- **Route organization**: API routes in `routes.py`, HTML views in `views.py` per module — new pages follow same split
- **i18n via template injection**: `inject_template_i18n` middleware makes `t()` available in all templates
- **Stripe integration**: Checkout redirect flow (not embedded), webhook handler pattern in billing routes

### Integration Points
- `main.py`: New routers for landing/pricing/legal pages registered here
- `app/templates/base.html`: Footer needs legal page links (terms, privacy, refund)
- `app/billing/routes.py`: Extend checkout endpoint for self-hosted one-time payment
- `self-hosted/docker-compose.yml`: Update image reference from local build to `ghcr.io/OWNER/synco:latest`
- `Dockerfile`: Add OCI labels for GHCR metadata

</code_context>

<specifics>
## Specific Ideas

- Pricing amounts (19/29 PLN) researched against Todoist Pro (19 PLN/mo) and Notion Plus (€9.50/mo ≈ 40 PLN) — positioned at the lower end since Synco is a household tool, not a business productivity suite
- Self-hosted at 199 PLN one-time is positioned as "buy once, own forever" — clear value vs recurring SaaS
- Annual discount follows the "2 months free" pattern used universally by Todoist, Notion, Coda
- Landing page hero "Jeden kalendarz dla dwojga" mirrors how real Polish couples would describe the need
- Legal pages in plain language because the app targets non-technical household users
- GHCR chosen over Docker Hub because: free for public (AGPL), no rate limits for authenticated pulls, integrated auth with GitHub Actions

</specifics>

<deferred>
## Deferred Ideas

- A/B testing on pricing page — revisit after launch with real traffic data
- Testimonials/social proof section — add once real users provide feedback
- Annual-only discount landing page experiment
- Stripe Customer Portal link on pricing page for existing subscribers
- Marketing/SEO/paid acquisition campaigns — separate post-launch effort
- Play Store listing — Phase 32 documents the path, actual submission is post-launch

</deferred>

---

*Phase: 33-go-to-market*
*Context gathered: 2026-03-23*

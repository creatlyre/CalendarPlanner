# Phase 28: Licensing and Commercial Terms Foundation — Research

**Date:** 2026-03-23
**Phase:** 28-licensing
**Requirements:** MON-01, MON-02, MON-03

## Research Question

"What do I need to know to PLAN a licensing and commercial terms foundation for an AGPL-3.0 open-source project transitioning to dual-license monetization?"

## Current State

- LICENSE file: AGPL-3.0 already in repository root ✓
- pyproject.toml: project name "synco", version 3.0.0
- README.md: no licensing section beyond implicit open-source
- No commercial license terms exist
- No monetization documentation exists
- No source file copyright headers
- No NOTICE file
- No CLA (Contributor License Agreement)

## Domain Research: AGPL-3.0 Dual-Licensing

### How AGPL-3.0 Dual-Licensing Works

AGPL-3.0 is a strong copyleft license that requires:
1. Source code distribution for any modifications
2. **Network use provision (Section 13):** If you run a modified version as a network service, you must offer source code to users of that service
3. All derivative works must also be AGPL-3.0

**Dual-licensing** means the copyright holder offers the same codebase under two licenses:
- **AGPL-3.0** — free for open-source use, community, self-hosting (with AGPL obligations)
- **Commercial license** — paid license that removes AGPL obligations (no source disclosure requirement)

### Prerequisite: Copyright Ownership

Dual-licensing only works if the copyright holder has the right to grant commercial licenses. For a solo developer project (Wojciech), this is straightforward — the author holds full copyright. If outside contributors ever contribute, a CLA (Contributor License Agreement) would be needed to maintain the right to dual-license.

### Successful AGPL Dual-License Models

| Project | Open License | Commercial Model |
|---------|-------------|-----------------|
| Grafana | AGPL-3.0 | Cloud SaaS + Enterprise license |
| Mattermost | AGPL-3.0 (Team) + proprietary (Enterprise) | Enterprise self-hosted + Cloud |
| Nextcloud | AGPL-3.0 | Enterprise subscription for support + features |
| MongoDB (pre-SSPL) | AGPL-3.0 | Commercial license for embedding |

### What a Commercial License Exception Contains

A commercial license exception typically includes:
1. **Grant of rights** — Use, modify, deploy without AGPL source obligations
2. **Scope** — Single organization, single deployment, or unlimited
3. **Restrictions** — No redistribution of the licensed code, no sublicensing
4. **Support terms** — Whether support is included or separate
5. **Duration** — Perpetual with version lock, or subscription-based
6. **Price** — One-time or recurring

For Synco's case, two commercial license variants are needed:
- **SaaS commercial license** — implicit (Synco runs its own SaaS, so this is just the hosted offering)
- **Self-hosted commercial license** — explicit (buyers get a license key to run without AGPL obligations)

### What Monetization Documentation Should Cover

Per MON-03, clear documentation explaining:
1. **What is free:** AGPL-3.0 core, self-hosting with AGPL compliance, community support
2. **What is paid:** Hosted SaaS plans, commercial self-hosted license (no AGPL obligations), priority support
3. **AGPL obligations:** If you modify and host, you must share source. Commercial license removes this.

## Standard Artifacts to Create

### 1. LICENSE (already exists) — MON-01
- Current AGPL-3.0 file is correct
- Verify copyright year and holder name

### 2. COMMERCIAL-LICENSE.md — MON-02
A public-facing document explaining:
- What the commercial license grants (use without AGPL obligations)
- Who needs it (companies modifying Synco for internal use, SaaS providers)
- How to purchase (link to pricing/contact)
- Basic terms (scope, restrictions, warranty disclaimer)

This is NOT a full legal contract — it's a clear explanation of what buyers get. The actual purchase agreement would be generated per-transaction in phase 29+ (Stripe/Paddle checkout).

### 3. MONETIZATION.md — MON-03
Clear public-facing explanation:
- Free tier: what you get at no cost
- SaaS tiers: what paid plans include
- Self-hosted commercial: what you get with a license purchase
- AGPL obligations summary: plain-language explanation

### 4. NOTICE file (recommended)
Standard open-source practice — lists copyright, third-party attributions, trademarks.

### 5. Source file headers (recommended but deferrable)
Adding AGPL copyright headers to .py files is good practice but can be automated. Not strictly required for MON-01/02/03.

## Validation Architecture

### Testable Behaviors

| Truth | Verification |
|-------|-------------|
| AGPL-3.0 license file exists and is correct | `grep "GNU AFFERO GENERAL PUBLIC LICENSE" LICENSE` |
| Commercial license terms are defined | `test -f COMMERCIAL-LICENSE.md` + `grep "commercial" COMMERCIAL-LICENSE.md` |
| Monetization docs explain free vs paid | `grep -c "free\|paid\|AGPL" MONETIZATION.md` returns 3+ matches |
| README links to license docs | `grep "license\|License" README.md` |

### Key Risks

1. **Legal accuracy** — License text should be clear but must include disclaimer that it's informational, not legal advice
2. **CLA timing** — Not needed now (solo developer), but should be mentioned for future contributor onboarding
3. **Price anchoring** — Monetization docs should explain the model without locking in specific prices (prices belong in phase 33 GTM)

## Recommendations for Planning

### Discovery Level: 0 (Skip)
This is purely internal documentation work — no new libraries, no external APIs, no code integration. All work follows established patterns (Markdown documentation).

### Task Breakdown Suggestion

**Plan 01 (2 tasks):** License foundation
- Task 1: Create COMMERCIAL-LICENSE.md with dual-license terms
- Task 2: Create MONETIZATION.md explaining the model

**Plan 02 (2 tasks):** Repository hygiene and README integration
- Task 1: Add NOTICE file and update LICENSE copyright
- Task 2: Update README.md with licensing section and links

### Scope Estimate
- 2 plans, all Wave 1 (independent)
- Pure documentation — no code changes
- ~15-20% context each (small tasks)

## Don't Hand-Roll

- Do NOT write a full legal contract — use standard dual-license explanation patterns
- Do NOT lock in specific prices — that's phase 33 (GTM)
- Do NOT add CLA infrastructure yet — only note it's needed for future contributors
- Do NOT add license headers to every .py file — deferrable and can be automated later

---

*Research completed: 2026-03-23*

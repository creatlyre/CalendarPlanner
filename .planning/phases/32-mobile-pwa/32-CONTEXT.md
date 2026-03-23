# Phase 32: Mobile Distribution Path (PWA + Android Wrapper) - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning
**Source:** Auto mode (--auto) — recommended defaults selected

<domain>
## Phase Boundary

Phase 32 makes the Synco web app installable as a Progressive Web App (PWA) and defines the Android distribution path via Trusted Web Activity. This covers requirements MOB-01 through MOB-03:

- Harden the web app as an installable PWA (manifest, icons, install prompt, offline shell)
- Define and test the Android wrapper distribution path (TWA via Bubblewrap)
- Explicitly defer native iOS/Android full rewrite (document this decision)

This phase does NOT change the app's core functionality — it wraps the existing HTMX SSR web app for mobile installation.

**What is NOT in scope:**
- Native iOS or Android app development (explicitly deferred per MOB-03)
- Full offline data sync or offline CRUD operations
- Push notifications via Web Push API (users get push via Google Calendar sync)
- App store listing or Play Store submission (Phase 33 GTM scope)

</domain>

<decisions>
## Implementation Decisions

### PWA Offline Strategy — LOCKED
- **Minimal offline shell approach** — show cached app shell with "You're offline" message for key pages
- HTMX SSR architecture makes full offline data sync impractical without major rearchitecture
- Cache static assets (CSS, fonts, icons) with cache-first strategy
- Cache app shell HTML for dashboard and calendar pages
- API calls are NOT cached — show offline message instead
- Service worker update: skipWaiting + reload prompt (toast to refresh on new version)
- Cache strategy: cache-first for versioned static assets, network-first for HTML pages

### Android Wrapper Approach — LOCKED
- **Trusted Web Activity (TWA) via Bubblewrap CLI** — lightest approach, no native code
- Generate signed APK/AAB for sideloading and documenting Play Store upload steps
- Defer actual Play Store listing to Phase 33 GTM
- Custom splash screen with Synco branding
- Status bar color matching theme-color (#1e1553)
- Standalone display mode (no URL bar)
- Target: Chrome 72+ (TWA support), Android 7.0+ (Nougat)

### Install Experience — LOCKED
- Show install banner on second visit (use beforeinstallprompt event with dismiss option)
- App icons generated from existing SVG calendar icon — 192x192 and 512x512 PNG + maskable variant
- Indigo brand color (#6366f1 primary, #1e1553 dark) preserved
- Manifest: name "Synco", short_name "Synco", start_url "/dashboard"
- Splash screen auto-generated from manifest (background + icon + name)
- Display mode: standalone

### Native App Deferral (MOB-03) — LOCKED
- Document in MONETIZATION.md or dedicated doc that native iOS/Android is explicitly deferred
- Rationale: PWA + TWA covers mobile access; native rewrite only after monetization validation
- This is a documentation-only task, no code needed

### Claude's Discretion
- Service worker registration approach (inline script vs separate registration file)
- Exact offline page design and messaging
- Bubblewrap configuration details
- Whether to include optional web app features (shortcuts, share_target)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Context
- `.planning/PROJECT.md` — Project vision, key decisions including "Web app first; PWA and Android wrapper"
- `.planning/REQUIREMENTS.md` — MOB-01, MOB-02, MOB-03 requirement definitions
- `MONETIZATION.md` — Current monetization model (native deferral note goes here)

### Existing Code
- `app/templates/base.html` — Base HTML template with existing theme-color meta tag
- `public/css/style.css` — Static CSS (already served from /static/)
- `main.py` — App entry with StaticFiles mount at /static -> public/
- `Dockerfile` — Container build (COPY . . includes public/ directory)

### Prior Phases
- `.planning/phases/30-saas-production/30-02-SUMMARY.md` — Security headers, CORS config affecting service worker

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app/templates/base.html` already has `<meta name="theme-color" content="#1e1553">` — can add manifest link here
- `public/` directory with `css/` — natural home for PWA static assets (icons, manifest, sw.js)
- `main.py` mounts `StaticFiles(directory="public")` at `/static` — manifest and sw.js may need root-level serving

### Established Patterns
- HTMX + server-side rendering — no SPA, no client-side routing, no JS framework
- Jinja2 templates with i18n via `t()` function
- Static assets served from `/static/` with 7-day cache headers (StaticCacheMiddleware)

### Integration Points
- `base.html <head>` — add `<link rel="manifest">` and service worker registration script
- `main.py` — may need root-level routes for `/manifest.json` and `/sw.js` (service workers must be at root scope)
- `Dockerfile` — no changes needed, public/ already COPY'd
- `config.py` — no changes needed for PWA

</code_context>

<specifics>
## Specific Ideas

No specific requirements — open to standard PWA and TWA approaches following web platform best practices.

</specifics>

<deferred>
## Deferred Ideas

- Web Push notifications (users already get push via Google Calendar sync)
- Full offline data sync with background sync API
- iOS-specific PWA improvements (Apple's PWA support is limited)
- Play Store submission and listing optimization (Phase 33 GTM)

</deferred>

---

*Phase: 32-mobile-pwa*
*Context gathered: 2026-03-23*

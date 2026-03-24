---
phase: 31-self-hosted
plan: 01
subsystem: licensing, infra
tags: [hmac, docker-compose, caddy, postgrest, license-key]

requires:
  - phase: 30-saas-production
    provides: Dockerfile, production config, security middleware

provides:
  - HMAC-based license key generation and validation
  - LicenseCheckMiddleware for self-hosted banner injection
  - Docker Compose package (app + postgres + postgrest + caddy)
  - Self-hosted .env.template and Caddyfile

affects: [31-self-hosted]

tech-stack:
  added: [postgrest, caddy]
  patterns: [HMAC license keys, middleware-based license enforcement]

key-files:
  created:
    - app/licensing/keys.py
    - app/licensing/middleware.py
    - app/licensing/generate.py
    - app/licensing/__main__.py
    - self-hosted/docker-compose.yml
    - self-hosted/.env.template
    - self-hosted/Caddyfile
  modified:
    - config.py
    - main.py
    - .env.example

key-decisions:
  - "HMAC-SHA256 with hex encoding for license keys (simple, offline validation)"
  - "License middleware is outermost (before SecurityHeaders) to modify HTML responses"
  - "PostgREST as Supabase-compatible REST API for self-hosted deployments"
  - "Caddy for automatic HTTPS with Let's Encrypt"

patterns-established:
  - "License key format: SYNCO-{8hex}-{8hex}-{8hex}-{8hex}-{8hex_check}"
  - "Self-hosted config via .env.template with ENVIRONMENT=self-hosted"

requirements-completed: [SHS-01, SHS-02]

duration: 8min
completed: 2026-03-23
---

# Plan 31-01: License Key System & Docker Compose Package

**HMAC license keys with self-hosted Docker Compose deployment package (app + postgres + postgrest + caddy)**

## Performance

- **Duration:** 8 min
- **Tasks:** 2/2
- **Files created:** 7
- **Files modified:** 3

## Accomplishments

- License key generation via `python -m app.licensing.generate <secret>` producing `SYNCO-*` format keys
- HMAC-SHA256 validation with constant-time comparison (`hmac.compare_digest`)
- `LicenseCheckMiddleware` injects warning banner on HTML pages when license is invalid/missing in self-hosted mode
- Middleware skips JSON/API responses and health endpoints
- Docker Compose with 4 services: app, PostgreSQL, PostgREST, Caddy
- `.env.template` with all configuration options documented
- Caddyfile with reverse proxy and auto-HTTPS via environment variable domain

## Self-Check: PASSED
- License key generation produces valid SYNCO-* format ✓
- Valid key validates, invalid/wrong-secret rejected ✓
- App loads with 94 routes and LicenseCheckMiddleware ✓
- Docker Compose has all 4 services ✓
- .env.template has all required variables ✓

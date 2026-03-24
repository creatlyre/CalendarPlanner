---
phase: 04-admin-dashboard-user-management-plan-assignment-admin-privileges-and-statistics
plan: 02
subsystem: admin-ui
tags: [admin, jinja2, glassmorphic, i18n, html]

requires:
  - phase: 04-01
    provides: Admin API routes, AdminService, get_admin_user dependency

provides:
  - Admin dashboard HTML page with stats cards
  - User management table with search and pagination
  - User detail page with plan change and admin toggle forms
  - Admin nav link in base.html (conditional on is_admin)
  - 30 admin i18n keys in EN and PL

affects: []

tech-stack:
  added: []
  patterns: [admin views pattern matching billing/dashboard views]

key-files:
  created:
    - app/admin/views.py
    - app/templates/admin_dashboard.html
    - app/templates/admin_users.html
    - app/templates/admin_user_detail.html
  modified:
    - app/templates/base.html
    - app/locales/en.json
    - app/locales/pl.json
    - main.py
    - tests/test_admin.py

key-decisions:
  - "Non-admin /admin access redirected to /dashboard via 403 exception handler"
  - "Plan map computed per-request for user list (acceptable for admin-only page)"

patterns-established:
  - "Admin views follow same inject_template_i18n pattern as billing/dashboard views"

requirements-completed: [ADM-01, ADM-02, ADM-03, ADM-04]

duration: 10min
completed: 2026-03-24
---

# Plan 04-02: Admin HTML Views, Templates, Nav Link & i18n

**Full admin web interface — dashboard stats, user management table, detail page with plan/admin controls — matching Synco's glassmorphic theme with EN/PL translations**

## Performance

- **Duration:** 10 min
- **Tasks:** 1/1 auto tasks completed (checkpoint pending)
- **Files modified:** 9

## Accomplishments
- Admin dashboard at /admin with stats cards (total users, recent signups, active subs) and plan distribution bars
- User management table at /admin/users with search, pagination, plan badges
- User detail page at /admin/users/{id} with plan dropdown + admin toggle (self-protection on own user)
- Conditional admin nav link with shield icon in navbar
- Non-admins redirected to /dashboard when accessing /admin
- 30 i18n keys in EN and PL

## Task Commits

1. **Task 1: Admin views, templates, nav link, i18n** - `fca938c`

## Files Created/Modified
- `app/admin/views.py` - 3 admin HTML view routes
- `app/templates/admin_dashboard.html` - Stats cards, plan distribution, quick actions
- `app/templates/admin_users.html` - User table with search and pagination
- `app/templates/admin_user_detail.html` - User detail with plan change and admin toggle forms
- `app/templates/base.html` - Conditional admin shield icon nav link
- `app/locales/en.json` - 30 admin keys (EN)
- `app/locales/pl.json` - 30 admin keys (PL)
- `main.py` - Registered admin_views_router, added 403 redirect for /admin
- `tests/test_admin.py` - 6 additional view tests (21 total)

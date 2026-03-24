---
plan: 03-02
status: complete
completed: 2026-03-24
---

# Summary: Forgot Password, Email Verification & Password Update (03-02)

## What Was Built
- **3 new Supabase auth functions** in `supabase_auth.py`: password reset request, OTP verification, password update.
- **Forgot password page** (`/auth/forgot-password`): Email form that requests a Supabase password recovery email. Never reveals whether the email exists (security).
- **Email confirmation callback** (`/auth/confirm`): Handles both signup confirmation and password recovery tokens. Exchanges OTP for session, upserts local user, redirects appropriately.
- **Update password page** (`/auth/update-password`): Session-protected form to set a new password after recovery.
- **i18n**: 16 new keys added to both en.json and pl.json.
- **Tests**: 10 new tests covering all flows, security behavior, and edge cases.

## Key Files

### Created
- `app/templates/forgot_password.html` — Forgot password form page
- `app/templates/update_password.html` — Set new password form page

### Modified
- `app/auth/supabase_auth.py` — 3 new async functions
- `app/auth/routes.py` — 6 new route handlers + 2 Pydantic models
- `app/locales/en.json` — 16 new auth.* keys
- `app/locales/pl.json` — 16 new auth.* keys
- `tests/test_auth.py` — 10 new tests (23 total)

## Decisions
- Used non-deprecated `TemplateResponse(request, name, context)` API
- Forgot-password POST always returns 200 regardless of email existence (security best practice)
- Confirm callback handles both `type=recovery` and `type=signup` in a single handler
- Update-password requires session cookie (set by confirm callback)

## Self-Check: PASSED
- [x] All 23 auth tests pass (546 total suite)
- [x] Forgot-password never reveals email existence
- [x] Confirm callback creates session for both recovery and signup
- [x] Update-password validates min length and requires session
- [x] i18n keys complete in both locales

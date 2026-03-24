---
phase: 03
slug: login-and-register-pages-email-password-authentication-with-google-oauth
status: complete
nyquist_compliant: true
wave_0_complete: true
created: 2026-03-24
updated: 2026-03-24
---

# Phase 03 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `python -m pytest tests/test_auth.py -x --tb=short` |
| **Full suite command** | `python -m pytest tests/ -x --tb=short` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_auth.py -x --tb=short`
- **After every plan wave:** Run `python -m pytest tests/ -x --tb=short`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | AUTH-01 | unit+integration | `python -m pytest tests/test_auth.py::test_login_page_renders tests/test_auth.py::test_login_google_redirect tests/test_auth.py::test_register_page_renders tests/test_auth.py::test_login_page_has_google_oauth_button tests/test_auth.py::test_register_page_has_google_oauth_button -x --tb=short` | ✅ | ✅ green |
| 03-01-02 | 01 | 1 | AUTH-01 | integration | `python -m pytest tests/test_auth.py -k "login_page or register_page or google" -x --tb=short` | ✅ | ✅ green |
| 03-02-01 | 02 | 2 | AUTH-02 | unit+integration | `python -m pytest tests/test_auth.py::test_forgot_password_page_renders tests/test_auth.py::test_forgot_password_submit_returns_success tests/test_auth.py::test_forgot_password_nonexistent_email_still_succeeds tests/test_auth.py::test_confirm_callback_recovery_redirects_to_update_password tests/test_auth.py::test_confirm_callback_signup_redirects_to_home tests/test_auth.py::test_confirm_callback_missing_params_redirects_to_login -x --tb=short` | ✅ | ✅ green |
| 03-02-02 | 02 | 2 | AUTH-02 | integration | `python -m pytest tests/test_auth.py::test_update_password_page_requires_session tests/test_auth.py::test_update_password_page_renders_with_session tests/test_auth.py::test_update_password_submit tests/test_auth.py::test_update_password_too_short -x --tb=short` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements. `tests/test_auth.py` and `tests/conftest.py` already exist. All 15 phase-specific tests written and passing.*

---

## Requirement-to-Test Coverage

### AUTH-01: Login & Register Pages
| Test | Behavior Verified |
|------|-------------------|
| `test_login_page_renders` | GET /auth/login returns 200 HTML with password-login form + register link |
| `test_login_google_redirect` | GET /auth/login?provider=google redirects to OAuth provider |
| `test_register_page_renders` | GET /auth/register returns 200 HTML with registration form + login link |
| `test_login_page_has_google_oauth_button` | Login page contains Google OAuth link |
| `test_register_page_has_google_oauth_button` | Register page contains Google OAuth link |

### AUTH-02: Forgot Password, Email Confirm, Update Password
| Test | Behavior Verified |
|------|-------------------|
| `test_forgot_password_page_renders` | GET /auth/forgot-password returns 200 HTML form |
| `test_forgot_password_submit_returns_success` | POST /auth/forgot-password returns 200 on valid email |
| `test_forgot_password_nonexistent_email_still_succeeds` | POST /auth/forgot-password returns 200 even for unknown email (security) |
| `test_confirm_callback_recovery_redirects_to_update_password` | GET /auth/confirm?type=recovery creates session, redirects to /auth/update-password |
| `test_confirm_callback_signup_redirects_to_home` | GET /auth/confirm?type=signup creates session, redirects to / |
| `test_confirm_callback_missing_params_redirects_to_login` | GET /auth/confirm without params redirects to /auth/login |
| `test_update_password_page_requires_session` | GET /auth/update-password without session redirects to login |
| `test_update_password_page_renders_with_session` | GET /auth/update-password with session renders form |
| `test_update_password_submit` | POST /auth/update-password with valid password returns 200 |
| `test_update_password_too_short` | POST /auth/update-password with <6 char password returns 400 |

### Key Links Verified
| From | To | Pattern | Found |
|------|----|---------|-------|
| login.html | /auth/password-login | `fetch.*password-login` | ✅ |
| login.html | /auth/login?provider=google | `auth/login.*google` | ✅ |
| register.html | /auth/register | `fetch.*auth/register` | ✅ |
| auth_middleware.py | /auth/login | `/auth/login` | ✅ |
| routes.py | supabase_request_password_reset | function call | ✅ |
| routes.py | supabase_verify_otp | function call | ✅ |
| routes.py | supabase_update_user_password | function call | ✅ |

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Glassmorphic UI matches Synco brand | AUTH-01 | Visual design | Visit /auth/login and /auth/register, verify dark theme, blur cards, gradient buttons |
| Google OAuth button launches flow | AUTH-01 | External service | Click "Sign in with Google" on login page, verify redirect to Google |
| Password reset email arrives | AUTH-02 | External email | Submit forgot-password form, check inbox for Supabase recovery email |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 15s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** ✅ PASSED — 2026-03-24

---

## Validation Audit 2026-03-24

| Metric | Count |
|--------|-------|
| Requirements | 2 (AUTH-01, AUTH-02) |
| Automated tests | 15 |
| Key links verified | 7/7 |
| Gaps found | 0 |
| Manual-only items | 3 (visual design, Google OAuth external, email delivery) |
| Full suite | 546 passed, 0 failed |

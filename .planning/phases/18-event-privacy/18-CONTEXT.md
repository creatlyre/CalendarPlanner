# Phase 18: Event Privacy - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Validate and harden the event visibility toggle so private events are invisible to partner across web views and Google Calendar. Backend is ~90% complete — phase focuses on UI indicators, form hardening, sync retraction on visibility change, and import validation.

</domain>

<decisions>
## Implementation Decisions

### Lock Icon & Visual Indicators
- Lock icon appears in both month grid and day view — consistent experience matching PRIV-03 "calendar grid"
- Style: small 🔒 emoji before event title — minimal, works in truncated cells, no extra SVG needed
- No different background color for private events — same `bg-indigo-500/25`, lock icon is sufficient
- No lock indicator in "+N more" overflow count — user sees lock when they expand day view

### Sync Retraction (Shared → Private)
- Delete from partner's Google Calendar immediately on visibility change — clean and predictable per PRIV-04
- If GCal delete fails: log warning and continue — don't block the local update, retract on next sync
- Private → shared: auto-push to partner's GCal — consistent behavior, mirrors the retraction
- Fix `export_month` to pass `requesting_user_id` — prevents private titles leaking into memory/logs

### Form & Import Hardening
- Add visibility dropdown to `event_form.html` (simple form) — same as entry modal, both creation paths support privacy
- Fix JavaScript to populate visibility on edit — read event visibility and set select value to prevent accidental loss
- Import validation: skip private events where `cp_owner_id` ≠ importing user — prevents ownership confusion
- Quick-add modal: do not add visibility — quick-add is for speed, default "shared" is correct for fast entry

### Claude's Discretion
- No items deferred to Claude's discretion — all decisions resolved

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `Event.visibility` field already exists in `app/database/models.py` (defaults to "shared")
- `EventCreate` / `EventUpdate` schemas already validate `Literal["shared", "private"]` in `app/events/schemas.py`
- `_visible_to()` filter method in `app/events/repository.py` — applied in `list_for_day()`, `list_for_month()`, `list_recurrence_roots_until()`
- Visibility dropdown already in `app/templates/partials/event_entry_modal.html`
- i18n keys complete: `qa.visibility`, `qa.visibility_shared`, `qa.visibility_private`, `qa.visibility_help` in both en.json and pl.json
- 9 existing visibility tests in `tests/test_events_api.py`
- `_sync_recipients()` in `app/sync/service.py` already filters private events to owner-only sync
- `_extract_cp_visibility()` in sync service already reads visibility from Google Calendar extended properties

### Established Patterns
- Jinja2 templates with Tailwind CSS utility classes
- HTMX for partial page updates
- Glass-morphism UI style (`glass-input`, `bg-indigo-500/25`)
- Service → Repository layered architecture
- `inject_template_i18n()` for template localization

### Integration Points
- `app/templates/partials/month_grid.html` — event rendering in calendar grid (needs lock icon)
- `app/templates/partials/day_events.html` — day event list (needs lock icon)
- `app/templates/partials/event_form.html` — simple event form (needs visibility dropdown)
- `app/sync/service.py` — sync_event_for_household (needs retraction logic)
- `app/events/service.py` — update_event, delete_event (privacy enforcement already done)

</code_context>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches. Lock icon uses 🔒 emoji for simplicity.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

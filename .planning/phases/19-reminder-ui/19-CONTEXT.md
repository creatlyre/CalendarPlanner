# Phase 19: Reminder UI - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Wire reminder controls into event forms so users can configure event reminders that sync to Google Calendar. Backend is 100% complete (schemas, validation, sync payload, tests) — phase is purely frontend: form UI, JavaScript handlers, and i18n keys.

</domain>

<decisions>
## Implementation Decisions

### Reminder Layout & Toggle Behavior
- Place reminder controls below visibility dropdown, before submit buttons — logical flow: dates → repeat → visibility → reminders → submit
- Enabled by default with 2 defaults: 30 min and 2880 min (2 days) — matches REM-01 household defaults spec
- Display defaults as pre-populated chip list — each chip shows "30 min" and "2 days" with × to remove
- Do not include reminders in quick-add modal — quick-add is for speed, defaults apply automatically when not specified

### Multi-Reminder Editing (Chip-Based UI)
- Chip add interaction: "+ Add reminder" button below chips, opens inline row with minutes input + method select
- Reminder method per REM-03: select with "popup" and "email" options, default "popup" — popup maps to mobile notifications
- Max reminders display: show "max 5" counter text, disable "Add" button when 5 reached — clear per Google API limit
- Free-form minutes input (plain number) — flexible, validation handles 0–40320 range

### Sync Helper Text & Form Integration
- Helper text below reminders section: "Reminders sync to Google Calendar" — matches REM-03 requirement
- Add reminders to simple event_form.html — same controls for form parity per Phase 18 pattern
- Edit mode: populate existing reminders by reading event's reminder_minutes_list and rendering chips
- Toggling reminders off: clear the reminder_minutes_list, send empty array — uses Google Calendar defaults instead

### Claude's Discretion
- No items deferred to Claude's discretion — all decisions resolved

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `Event.reminder_minutes` (single, backward compat) and `Event.reminder_minutes_list` (list) in `app/database/models.py`
- `Event.effective_reminders` property — returns list if set, else single, else empty
- `EventCreate` / `EventUpdate` schemas validate `reminder_minutes` and `reminder_minutes_list` in `app/events/schemas.py`
- Pydantic validator ensures non-negative values, max 40320 minutes (4 weeks)
- `_event_body()` in `app/sync/service.py` builds Google Calendar reminder payload — `popup` method, `useDefault` fallback
- `GOOGLE_EVENT_REMINDER_MINUTES = 30` in `config.py`
- Existing sync tests in `tests/test_sync_api.py` cover reminder payload generation

### Established Patterns
- Jinja2 templates with Tailwind CSS utility classes
- Glass-morphism UI style (`glass-input`, `bg-indigo-500/25`)
- JavaScript in `calendar.html` script block — `submitEventEntry()`, `submitEventForm()` functions
- Visibility dropdown pattern from Phase 18 (select with i18n labels)
- HTMX for partial page updates

### Integration Points
- `app/templates/partials/event_entry_modal.html` — main event form (needs reminder section)
- `app/templates/partials/event_form.html` — simple form (needs reminder section for parity)
- `app/templates/calendar.html` — JavaScript handlers for form submission and populate-on-edit
- `app/locales/en.json` and `app/locales/pl.json` — need reminder i18n keys
- `app/events/routes.py` — API already accepts reminder fields, no changes needed

</code_context>

<specifics>
## Specific Ideas

Chip-based UI for reminders: each reminder displays as a small rounded chip (e.g., "30 min ×", "2 days ×") with delete button. "+" button adds new reminder with minutes input and method select.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

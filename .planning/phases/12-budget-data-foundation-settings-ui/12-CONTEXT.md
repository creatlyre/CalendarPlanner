# Phase 12: Budget Data Foundation & Settings UI - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Users can configure their budget parameters (3 hourly rates in PLN, flat monthly ZUS + accounting costs, initial bank account balance) via a dedicated settings page integrated into the app navigation. All values persist across sessions and are editable at any time. This phase delivers the data layer (models, persistence) and settings UI only — no income calculation, expense tracking, or year overview.

</domain>

<decisions>
## Implementation Decisions

### Settings Page Structure
- Dedicated full page at its own route (e.g., `/budget/settings`) — first "second page" in the app beyond the calendar
- Navigation via a button in the top nav bar (alongside existing logo, language switcher, logout)
- Left sidebar menu on budget pages for section navigation (settings, and later phases will add more sections)
- Always a visible back button/link to return to the calendar view
- Single form with all budget settings (rates, costs, balance) on one page

### Rate Field Identity
- Rates labeled generically: Rate 1, Rate 2, Rate 3
- Fixed 3 slots — not expandable or user-nameable
- All rate values in PLN

### Save & Feedback Behavior
- All monetary/numeric inputs must be positive (validation rule)
- Save mechanism is Claude's discretion — auto-save on blur or explicit submit button, whichever works best with the form layout and UX

### Data Ownership
- Budget settings are shared per household — same model as the calendar
- Both partners see and can edit the same budget settings
- Tied to the shared calendar/household, not to individual users

### Claude's Discretion
- Save mechanism choice (auto-save vs submit button)
- Exact form layout and field grouping within the settings page
- Left sidebar visual design (consistent with glass morphism system)
- Loading/error states for the settings page
- Database table structure and column types

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements & Roadmap
- `.planning/REQUIREMENTS.md` — BSET-01 through BSET-05 (settings requirements), BL-01 (budget localization)
- `.planning/ROADMAP.md` — Phase 12 goal, success criteria, and dependency info

### Existing Patterns (follow these)
- `app/database/models.py` — Dataclass model pattern (User, Calendar, Event) to follow for budget models
- `app/database/schemas.py` — Pydantic schema pattern for API validation
- `app/database/supabase_store.py` — SupabaseStore CRUD pattern (select, insert, update)
- `app/events/repository.py` — Repository pattern with `_to_model()` helpers and filter syntax
- `app/events/service.py` — Service layer pattern (validation + repository calls)
- `app/views/calendar_routes.py` — HTMX view route pattern for HTML rendering
- `app/templates/base.html` — Nav bar structure where budget link must be added
- `app/templates/calendar.html` — Glass morphism CSS classes and layout patterns
- `app/i18n.py` — i18n system with `t()` helper and dotted key namespacing
- `app/locales/pl.json` — Polish locale file pattern for adding `budget.*` keys
- `app/locales/en.json` — English locale file pattern
- `main.py` — Router registration pattern for new modules
- `config.py` — Pydantic Settings pattern

### Prior Phase Decisions
- `08-CONTEXT.md` — i18n foundation: key-based translations, Polish default, `{{ t('key') }}` in templates

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SupabaseStore` class: Direct Supabase REST client — reuse for budget table CRUD
- Glass morphism CSS system: `.glass`, `.glass-btn-primary`, `.glass-btn-secondary`, `.glass-input` classes
- `base.html` nav bar: Extend with budget settings link
- i18n system: `t()` function + JSON locale files — add `budget.*` namespace keys
- Auth dependencies: `get_current_user`, `get_db` — reuse for budget routes

### Established Patterns
- Service → Repository → SupabaseStore layering
- Dataclass models + Pydantic schemas (separate concerns)
- HTMX-driven HTML partials for views
- Soft deletes with `is_deleted` flag (if applicable)
- Tailwind CSS utility classes with glass morphism custom styles
- Dark/light mode support via theme toggle

### Integration Points
- `base.html` nav bar — add budget settings link/button
- `main.py` — register new budget router(s)
- `app/locales/*.json` — add budget translation keys
- Supabase — new table(s) for budget settings data
- Household/calendar linkage — budget settings tied to same calendar_id used by events

</code_context>

<specifics>
## Specific Ideas

- Left sidebar menu sets the pattern for budget section navigation (Phase 13-15 will add more sections like Income, Expenses, Year Overview)
- The settings page is the first non-calendar page — establishes the multi-page navigation pattern for the app
- Follow existing glass morphism design language for all new UI elements

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 12-budget-data-foundation-settings-ui*
*Context gathered: 2026-03-20*

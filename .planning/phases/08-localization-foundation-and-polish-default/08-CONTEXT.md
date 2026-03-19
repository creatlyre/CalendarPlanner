# Phase 8: Localization Foundation and Polish Default - Context

**Gathered:** 2026-03-19
**Status:** Ready for planning
**Source:** User milestone request

<domain>
## Phase Boundary

Deliver localization foundations and Polish-default behavior across current app views and user-facing API messages. This phase includes translation resources and rendering/formatting updates, but does not include user-visible language switching controls.

</domain>

<decisions>
## Decisions

### Locked Decisions
- Polish must be the default language for the entire application experience.
- Translation coverage must include all current user-facing components in auth, calendar, events, sync status, NLP quick-add, and OCR quick-add flows.
- Translation resources must include Polish and English in preparation for later switching.
- Date/time display must follow Polish conventions in default mode.

### Claude's Discretion
- Internal implementation shape for translation storage and lookup helpers.
- Exact split between server-side and client-side localization helpers.
- Test file layout and marker assertions used to validate translated content.

</decisions>

<specifics>
## Specific Ideas

- Prefer key-based translations over hardcoded strings.
- Avoid dependence on OS process locale for month/day labels.
- Keep compatibility with existing quick-add and manual modal flows.

</specifics>

<deferred>
## Deferred Ideas

- Runtime language switcher UI and persistence behavior (planned for Phase 9).

</deferred>

---

*Phase: 08-localization-foundation-and-polish-default*
*Context gathered: 2026-03-19*

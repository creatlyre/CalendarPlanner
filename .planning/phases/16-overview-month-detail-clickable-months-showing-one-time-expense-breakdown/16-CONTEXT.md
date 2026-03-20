# Phase 16: Overview Month Detail - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Users can click any month row in the Year Overview table to expand an inline detail showing the one-time expense breakdown for that month. The detail supports full CRUD (add, edit, delete) for one-time expenses directly within the overview page. No changes to recurring expenses, income, or settings in this phase.

</domain>

<decisions>
## Implementation Decisions

### Month Click Interaction
- Expandable row below — click month row to expand/collapse inline detail section
- Whole row is clickable with cursor:pointer and hover highlight
- Accordion pattern — one month expandable at a time, clicking new collapses previous
- Chevron icon (▸/▾) in month cell, rotates on expand

### Detail Content & Layout
- Table of one-time expenses for that month — columns: Name, Amount (PLN)
- Include inline "add expense" form in the detail (name + amount + add button)
- Empty month shows "Brak jednorazowych wydatków" message with the add form still visible
- Small total row at bottom of detail matching the one-time expense column value

### Data & API Approach
- Extend overview API — include one-time expense arrays (with id, name, amount) per month in the existing response
- Preload with overview — single API call, instant expand
- Full CRUD in detail — inline edit (click to edit name/amount), delete (✕ button), add (inline form) — mirror expenses page patterns
- CSS slide-down animation — `max-height` transition for smooth expand/collapse

### Claude's Discretion
- Exact styling of expanded detail area (glass sub-panel, indentation)
- Toast feedback after add/edit/delete operations
- Responsive behavior for narrow screens
- Whether to show month name header in expanded section

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app/budget/overview_service.py` — `get_year_overview()` returns monthly data, needs expense detail arrays added
- `app/budget/overview_routes.py` — `GET /api/budget/overview?year=N` endpoint to extend
- `app/budget/expense_routes.py` — existing CRUD endpoints (POST/PUT/DELETE `/api/budget/expenses`)
- `app/templates/budget_overview.html` — current overview table with year picker, inline one-time edit
- Glass morphism CSS: `.glass`, `.glass-btn-*`, `.glass-input` classes
- `app/i18n.py` with `{{ t('key') }}` template helper
- Existing inline edit pattern in overview template (ot-editable cells)

### Established Patterns
- Overview table renders via JS `render(data)` function from fetch response
- Inline editing: click/dblclick → input swap → save via fetch → reload()
- Toast-style feedback after mutations
- Year picker with prev/next navigation and `reload()` function

### Integration Points
- `OverviewService.get_year_overview()` — extend to include expense items per month
- `ExpenseRepository.get_by_calendar_year()` — already returns all expenses for a year
- Overview template `render()` function — add click handlers and expanded row rendering
- Existing expense API endpoints for CRUD operations from detail view

</code_context>

<specifics>
## Specific Ideas

- Reuse the compact row style from the expenses page for the detail table
- CRUD operations in detail should use existing `/api/budget/expenses` endpoints (no new API for mutations)
- After any CRUD operation in detail, reload the full overview to recalculate totals

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

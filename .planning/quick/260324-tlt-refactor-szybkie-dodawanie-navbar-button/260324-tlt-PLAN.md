---
phase: quick-260324-tlt
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - app/templates/base.html
  - app/locales/pl.json
  - app/locales/en.json
autonomous: true
---

<objective>
Refactor the "Szybkie dodawanie" (Quick Add) navbar button and mobile FAB so they open
a chooser modal with 3 options — Wydarzenie (Event), Wydatek (Expense), Zakupy (Shopping) —
instead of directly opening the event quick-add modal.

Purpose: Users need a single entry-point that lets them pick *what* to quick-add before
showing the relevant form/page.

Output: A glass-styled chooser modal in base.html, new i18n keys, wired to existing
quick-add flows.
</objective>

<context>
@app/templates/base.html (navbar, quick-add modal JS, FAB)
@app/templates/partials/quick_add_modal.html (existing event quick-add)
@app/locales/pl.json
@app/locales/en.json
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add chooser modal HTML, i18n keys, and JS wiring</name>
  <files>app/templates/base.html, app/locales/pl.json, app/locales/en.json</files>
  <action>
1. Add i18n keys to both locale files:
   - "qa.chooser_title": "What do you want to add?" / "Co chcesz dodać?"
   - "qa.chooser_event": "Event" / "Wydarzenie"
   - "qa.chooser_expense": "Expense" / "Wydatek"
   - "qa.chooser_shopping": "Shopping" / "Zakupy"

2. In base.html, BEFORE the existing quick_add_modal.html include, add a new chooser modal
   `#qa-chooser-modal`. Glass-styled overlay + centered panel with 3 large buttons arranged
   vertically (each full-width, min-h-[56px]):
   - Event button (glass-btn-primary, lightning icon) → closes chooser, calls window.qaOpenModal()
   - Expense button (glass-btn-info, dollar icon) → closes chooser, navigates to /calendar?open=expense
   - Shopping button (glass-btn-secondary, shopping bag icon) → closes chooser, navigates to /shopping

   Each button shows an icon + the translated label. Panel has a close X button and
   closes on Escape or backdrop click.

3. Change the qa-global-btn and qa-fab click handlers: instead of calling openModal() directly,
   open the chooser. The existing `qa-open-btn` on the calendar page should continue to
   open the event quick-add directly (unchanged).

4. In the Quick Add Modal IIFE, keep `window.qaOpenModal = openModal;` so the chooser's
   Event button can call it.
  </action>
  <verify>
    Run the dev server, click "Szybkie dodawanie" in the navbar → chooser modal appears
    with 3 buttons. Click "Wydarzenie" → event quick-add opens. Click "Wydatek" → navigates
    to /calendar?open=expense. Click "Zakupy" → navigates to /shopping. Mobile FAB also
    opens chooser.
  </verify>
  <done>
    Navbar quick-add button and mobile FAB open a 3-option chooser modal. Each option routes
    to the correct existing flow. Calendar page's inline quick-add button still opens the
    event modal directly.
  </done>
</task>

</tasks>

<verification>
- Navbar "Szybkie dodawanie" opens chooser (not event modal directly)
- Mobile FAB opens chooser
- Calendar page inline "quick add" button still opens event modal directly
- Chooser closes on Escape, backdrop click, or X button
- All 3 buttons work and route correctly
- Both PL and EN locales render correctly
</verification>

<success_criteria>
- Chooser modal visible on click of navbar button and FAB
- 3 buttons: Event (opens event quick-add), Expense (navigates to expense), Shopping (navigates to shopping)
- Existing calendar page quick-add unchanged
</success_criteria>

<output>
After completion, create `.planning/quick/260324-tlt-refactor-szybkie-dodawanie-navbar-button/260324-tlt-SUMMARY.md`
</output>

# UI/UX Improvements — Phase 7

**Phase Goal:** Eliminate navigation friction and improve event entry workflow through four targeted UX fixes: back navigation on invite page, modal-based event input, user-friendly date/time picker, and real-time form validation.

**Design System Reference:** Glassmorphism (blur: 24px, inset glow, transparency), dark/light theme toggle (CSS custom properties), color palette (Indigo #6366F1, Red #EF4444, Green #22C55E), responsive grid scaling.

---

## 1. Back Button on Invite Page

### Problem Statement
Users navigate to the invite page (`/invite`) to add household members but have no way to return to the calendar without using browser back button. This violates standard UI affordances and creates perceived "trap" feeling.

### Design Contract

**Component:** Navigation Button  
**Location:** Top-left of invite form card, above email input field  
**Behavior:**
- Text: "← Back to Calendar"
- Click action: Navigate to `/calendar` (hardcoded link, no JS required)
- Visual: Glass button style with secondary color (blue/info), 0.3s transition on hover
- Icon: Left arrow (Unicode ← or CSS chevron-left from Tailwind)
- Mobile: Full-width button on small screens, inline-left on desktop (sm:)

**Template Location:** `app/templates/invite.html` (above form heading)

**Acceptance Criteria:**
1. Button renders above the invite heading
2. Button styles match glass button system (`.glass-btn-secondary`)
3. Click navigates to `/calendar` without error
4. Accessible: Button focusable via Tab, press Enter works
5. Mobile: Button size 44px minimum height for touch targets

**Example:** 
```html
<a href="/calendar" class="glass-btn-secondary mb-4 inline-block">
  ← Back to Calendar
</a>
```

---

## 2. Modal-Based Event Input

### Problem Statement
Current event entry uses sidebar form (right panel on desktop), which is:
- Cumbersome on mobile (requires horizontal scroll or constant panel toggle)
- Takes up 30% of screen real estate on desktop
- Forces user to see form while browsing calendar
- Mixes input state with calendar state (unclear when user is editing)

### Design Contract

**Component:** Floating Modal Overlay  
**Trigger:** 
- Current: Click "Add Event" button or quick-add modal "Use Manual Form" button
- New: Same triggers, but launches floating modal instead of sidebar reveal
- Keyboard: Press "E" key to open new event modal (global shortcut)

**Visual Design:**
- Width: 90vw max-width:500px on desktop, full width on mobile
- Backdrop: Semitransparent dark overlay (rgba(0,0,0,0.5), blur backdrop)
- Position: Centered (flexbox center)
- Glass panel with padding 24px (4-space units)
- Close button: X in top-right corner (tap/click)
- Entrance: Scale-up + fade-in (0.3s ease-out)
- Exit: Fade-out (0.15s ease-in)

**Form Contents (Migrate from `event_form.html`):**
- Title input (required, focus on open)
- Date picker input (see Section 3 for picker spec)
- Start time picker (see Section 3)
- End time picker (optional, default to +1 hour)
- Recurrence selector (optional, standard select for FREQ)
- Submit button: "Save Event" (right-aligned)
- Cancel button: "Cancel" (left, secondary style)
- Form validation feedback (see Section 4)

**Template Location:** 
- New partial: `app/templates/partials/event_entry_modal.html`
- Integration: `app/templates/calendar.html` (add modal structure below calendar grid)

**JavaScript Behavior:**
- Modal hidden by default (`hidden` class or `display:none`)
- Modal.open() function: Show modal, focus title input
- Modal.close() function: Hide modal, clear form, restore focus to trigger button
- Modal.toggle() function: Open if closed, close if open
- Pressing Escape key: Close modal

**Acceptance Criteria:**
1. Modal renders centered and responsive (full width on mobile, max-width 500px on desktop)
2. Modal styles match glass design system (.glass panel with inset border)
3. Form fields migrated from sidebar (all inputs present)
4. Modal opens/closes without errors
5. Closing modal clears form state (empty inputs, no leftover data)
6. Mobile: Modal full-width with padding (not edge-to-edge)
7. Keyboard: E key opens, Escape closes, Tab cycles focus
8. Calendar grid still visible and responsive behind modal

**Example Layout (Simplified):**
```
┌─────── Event Entry Modal ──────────────────────┐
│                                             [X] │
│  Title:  [                                   ] │
│                                                 │
│  Date:   [  date-picker  ]  Time: [time]       │
│                                                 │
│  End:    [optional]                             │
│                                                 │
│  Repeat: [select: Never ▼]                      │
│                                                 │
│  [Cancel]                              [Save]   │
└─────────────────────────────────────────────────┘
```

---

## 3. User-Friendly Date/Time Picker

### Problem Statement
Native `<input type="datetime-local">` is:
- Difficult to use on mobile (tiny calendar popup, hard to tap dates)
- Not customizable for visual consistency with glassmorphism theme
- No affordance for relative dates ("tomorrow", "next Monday")
- Time selection via number spinners is cumbersome for users

### Design Contract

**Date Input Behavior:**
- Type: `<input type="date">` (not datetime-local, separate date + time)
- Visual: Glass input with placeholder "Select date"
- Picker: Native mobile date picker (browser-provided widget)
- Desktop: Click field to show mini-calendar (Flatpickr library integration optional; fallback to date picker)
- Keyboard: Arrows to +/- 1 day, Shift+Arrow for +/- 1 week
- Quick shortcuts (optional): 
  - T = today
  - + = tomorrow
  - M = Monday
  - (If implemented, show in tooltip on focus)

**Time Input Behavior:**
- Type: `<input type="time">` (separate from date, for clarity)
- Visual: Glass input with placeholder "HH:MM"
- Picker: Native time picker (browser-provided)
- Keyboard: Arrow keys to increment/decrement (15-min steps)
- Format: 24-hour (HH:MM)
- Validation: Must be valid time, no negative durations

**Database / API:**
- Store as ISO 8601 (date and time separate, or combined after merge)
- No changes to backend; frontend only converts `date` + `time` inputs to `datetime` before POST

**Template Location:** 
- Update `event_entry_modal.html` date/time fields
- Update `event_form.html` sidebar if still used for editing

**Library Decision:**
- Primary: Use native HTML5 `<input type="date">` and `<input type="time">` (zero dependencies, works on all browsers)
- Secondary: If UX testing shows mobile frustration, integrate Flatpickr (lightweight, themeable, no jQuery)
- Avoid: jQuery UI Date Picker (too heavy), custom JS date picker (maintenance burden)

**Accessibility:**
- Inputs have explicit `<label>` tags (not placeholder-only)
- Labels visible at all times (not floating)
- Time inputs keyboard-navigable
- Mobile: Native pickers respect system accessibility settings

**Acceptance Criteria:**
1. Date input renders with glass style and placeholder "Select date"
2. Time input renders with glass style and placeholder "HH:MM" (or "—:—")
3. Clicking date input opens browser's native date picker
4. Clicking time input opens browser's native time picker
5. Form submission includes valid date + time (no empty values)
6. Validation prevents end time before start time (see Section 4)
7. Mobile: Native pickers accessible and usable without zooming
8. Keyboard: Tab navigates between inputs, arrow keys adjust time

**Example HTML:**
```html
<div class="grid grid-cols-2 gap-2">
  <div>
    <label class="mb-1 block text-xs font-medium uppercase text-white/60">Date</label>
    <input id="event-date" type="date" required class="glass-input" />
  </div>
  <div>
    <label class="mb-1 block text-xs font-medium uppercase text-white/60">Time</label>
    <input id="event-time" type="time" required class="glass-input" />
  </div>
</div>
```

---

## 4. Real-Time Form Validation Feedback

### Problem Statement
Current form allows invalid submissions:
- Empty title (caught server-side after submit)
- Invalid/missing date or time (caught server-side)
- End time before start time (caught server-side if implemented)
- Submit button always enabled, even with missing fields
- No inline error feedback; errors only appear after server response

### Design Contract

**Validation Rules (Client-Side):**
1. **Title:** Non-empty, 3–200 characters
   - Error: "Title must be 3–200 characters"
   - Feedback: Real-time as user types
2. **Date:** Valid date, not in past (allow today)
   - Error: "Please select a valid date (not in the past)"
   - Feedback: After date picker closes or on blur
3. **Time:** Valid HH:MM, 00:00–23:59
   - Error: "Please enter a valid time (HH:MM)"
   - Feedback: On blur or after time picker closes
4. **Duration:** End time ≥ start time + 15 min (minimum event length)
   - Error: "Event must be at least 15 minutes long"
   - Feedback: After end-time input loses focus
5. **Recurrence:** If FREQ selected, validate DTSTART + RRULE combination
   - Error: "Invalid recurrence rule"
   - Feedback: When user changes FREQ selector

**Inline Error Display:**
- Error text: Below input field, color red (#EF4444), font-size 0.75rem (12px)
- Error state: Input border highlights red on invalid (or subtle glow)
- Clear error when user corrects input (real-time)
- Do not show error state until user interacts with field (blur or change event)

**Submit Button State:**
- Disabled (opacity 0.5, cursor:not-allowed) if any required field invalid or empty
- Enabled (full opacity, cursor:pointer) once all required fields valid
- Loading state (after click): Spinner or "Saving..." text, button disabled to prevent double-submit

**Visual Feedback:**
- Valid input: Green checkmark icon (optional, right side of input)
- Invalid input: Red exclamation icon (optional, right side of input)
- Or: Subtle red border on invalid input (simpler, less visual clutter)

**HTML Structure:**
```html
<div>
  <label for="event-title" class="mb-1 block text-xs font-medium uppercase text-white/60">
    Title *
  </label>
  <input 
    id="event-title"
    type="text"
    required
    class="glass-input"
    minlength="3"
    maxlength="200"
  />
  <div class="text-red-500 text-xs mt-1" id="event-title-error" style="display:none;"></div>
</div>
```

**JavaScript Behavior:**
```javascript
const form = document.getElementById('event-entry-form');
const titleInput = document.getElementById('event-title');
const submitBtn = document.getElementById('submit-event-btn');

// Real-time validation as user types
titleInput.addEventListener('input', (e) => {
  const value = e.target.value.trim();
  const error = document.getElementById('event-title-error');
  
  if (value.length < 3) {
    error.textContent = 'Title must be at least 3 characters';
    error.style.display = 'block';
    updateSubmitButtonState();
  } else if (value.length > 200) {
    error.textContent = 'Title must not exceed 200 characters';
    error.style.display = 'block';
    updateSubmitButtonState();
  } else {
    error.style.display = 'none';
    updateSubmitButtonState();
  }
});

// Check all fields on each change to enable/disable submit
function updateSubmitButtonState() {
  const isValid = isFormValid();
  submitBtn.disabled = !isValid;
}

function isFormValid() {
  const title = titleInput.value.trim();
  const date = document.getElementById('event-date').value;
  const time = document.getElementById('event-time').value;
  // Add other validations...
  return title.length >= 3 && title.length <= 200 && date && time;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!isFormValid()) return; // Double-check before submit
  
  submitBtn.disabled = true;
  submitBtn.textContent = 'Saving...';
  
  try {
    const response = await fetch('/api/events', { method: 'POST', body: ... });
    // Handle response...
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Save Event';
  }
});
```

**Accessibility:**
- Error messages associated with inputs via `aria-describedby`
- Error text reads aloud for screen readers
- Invalid inputs marked with `aria-invalid="true"`
- Submit button state changes announced (if using live region)

**Acceptance Criteria:**
1. Form shows no errors on load (fresh form)
2. Title field shows error if user types <3 chars, clears when corrected
3. Submit button disabled until all required fields valid and pass validation
4. Submit button enabled once all validation passes
5. Error messages display below their respective inputs in red text
6. End-time validation prevents events <15 min duration
7. Form does not submit if validation fails (client-side `e.preventDefault()`)
8. Loading state appears after submit (button disabled, text changes)
9. Mobile: Errors readable without zooming, form flows naturally

---

## 5. Implementation Priority & Dependencies

**Wave 1 (Easy Wins):**
1. Back button on invite page (5 min, no dependencies)
2. Real-time validation on existing sidebar form (30 min, high ROI)

**Wave 2 (Core Refactor):**
3. Event entry modal structure (30 min, integrates into calendar.html)
4. Date/time picker inputs (15 min, replace datetime-local)
5. Form validation in modal (15 min, reuses Wave 1 validation logic)

**Wave 3 (Polish):**
6. Loading states and error recovery (15 min)
7. Keyboard shortcuts (E key, Escape key) (10 min)
8. Mobile button sizing and spacing (10 min)

**Estimated Total:** 2–3 hours execution time

---

## 6. Testing Strategy

**Manual UAT Walkthrough:**
1. Invite flow: Click back button, verify navigation to `/calendar`
2. Event entry modal: Press E, form opens, press Escape, form closes
3. Date/time inputs: Click date, native picker opens; click time, native picker opens
4. Validation: Type 1 char in title, submit button disabled; type 3 chars, button enabled
5. Submission: Fill valid form, click Save, event appears in calendar
6. Mobile: Rotate device, modal responsive, buttons touchable (44px+)

**Automated Tests:**
- Test: Back button href points to `/calendar`
- Test: Modal open/close functions work correctly
- Test: Form validation functions return correct boolean
- Test: Submit button state updates on input changes
- Test: Date + time combine into valid ISO 8601 datetime before POST
- Regression: All 52 existing tests still pass

**Accessibility Testing:**
- Tab navigation cycles through form fields in logical order
- Error messages readable by screen reader (VoiceOver, NVDA)
- Modal triggers focus trap (Tab stays within modal until closed)
- Color contrast: Red error text ≥4.5:1 ratio against glass background

---

## 7. Success Criteria (Phase-Level)

1. ✓ Back button renders on invite page and navigates correctly
2. ✓ Event entry modal opens/closes without errors
3. ✓ Date and time inputs render and accept user input
4. ✓ Form validation prevents invalid submission and shows error messages
5. ✓ Submit button state correctly reflects validation result
6. ✓ Modal and form styles match glassmorphism design system
7. ✓ All 52 existing tests pass (no regressions)
8. ✓ Manual UAT walkthrough passes all steps
9. ✓ Keyboard navigation (Tab, Escape, E key) works as documented
10. ✓ Mobile responsive: full-width modal, 44px+ touch targets

---

## 8. Design System Constraints

**Color Palette (Must Maintain):**
- Primary: Indigo #6366F1 (buttons, links, focus states)
- Secondary: Blue #3B82F6 (info buttons)
- Danger: Red #EF4444 (delete, error states, invalid inputs)
- Success: Green #22C55E (valid inputs, success messages)
- Glass background: `rgba(255, 255, 255, 0.07)` dark mode, `rgba(0, 0, 0, 0.05)` light mode
- Border: `1px solid rgba(255, 255, 255, 0.2)` dark mode, `1px solid rgba(0, 0, 0, 0.1)` light mode

**Spacing Scale (Tailwind):**
- Form gap: `gap-3` (12px) between fields
- Button padding: `px-4 py-2` (must be 44px min height on mobile)
- Modal padding: `24px` (4 units × 6px)

**Typography:**
- Heading: 18px, font-weight 600, Tailwind `font-semibold`
- Label: 12px, font-weight 500, uppercase tracking, `text-white/60` (dark) or `text-black/60` (light)
- Input: 14px, regular weight, `text-white` (dark) or `text-black` (light)
- Error: 12px, regular weight, red color, below input

**Transitions:**
- Modal entrance: `scale-up + fade-in (0.3s ease-out)`
- Modal exit: `fade-out (0.15s ease-in)`
- Button hover: `0.3s` all properties (opacity, shadow, bg color)
- Input focus: `outline-2 rounded` (matches Tailwind default)

**Responsive Breakpoints (Tailwind sm:):**
- Mobile: < 640px (full-width modal, single-column form)
- Desktop: ≥ 640px (max-width 500px modal, responsive grid)

---

## 9. Notes & Edge Cases

- **Thread safety:** No changes to backend; all validation frontend-only
- **Backward compatibility:** Sidebar form can remain for edit flows (not removed, just hidden when modal open)
- **Copy:** Button text and error messages must be clear, concise, scannable (no jargon)
- **Progressive enhancement:** If JavaScript disabled, form still submits (server-side validation catches errors). Not ideal UX but acceptable fallback.
- **Browser support:** Target all modern browsers (Chrome, Firefox, Safari, Edge). HTML5 date/time inputs have ~90% support; fallback gracefully if not supported.


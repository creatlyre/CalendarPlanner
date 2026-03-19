# Phase 7 Implementation Plan

**Phase:** UI/UX Improvements  
**Goal:** Eliminate navigation friction and improve event entry workflow  
**Estimated Duration:** 2–3 hours execution (4 implementation waves)  
**Target Completion:** Next session

---

## Plan Overview

This phase implements 4 UX fixes organized into 4 implementation waves:

| Wave | Tasks | Duration | Status |
|------|-------|----------|--------|
| 1 | Back button on invite; sidebar form validation | 35 min | Planned |
| 2 | Event entry modal scaffold + date/time inputs | 45 min | Planned |
| 3 | Form validation in modal + submission logic | 30 min | Planned |
| 4 | Keyboard shortcuts + mobile polish + tests | 25 min | Planned |

---

## Wave 1: Quick Wins (Sidebar + Invite Button)

**Objective:** Add back button to invite page and introduce form validation on sidebar form (reusable for modal later).

**Tasks:**

### 1.1 Add Back Button to Invite Page
**File:** `app/templates/invite.html`  
**Duration:** 5 min

**What to do:**
1. Open `invite.html`
2. Find the form container (likely `<form id="invite-form"...>`)
3. Add back button above the form heading:
   ```html
   <a href="/calendar" class="glass-btn-secondary mb-4 inline-block">
     ← Back to Calendar
   </a>
   ```
4. Verify: Click button in browser, should navigate to `/calendar`

**Acceptance:**
- [ ] Button renders above form heading
- [ ] Button uses `.glass-btn-secondary` class (blue style)
- [ ] Click navigates to `/calendar` without errors
- [ ] Mobile: Button is 44px+ tall

---

### 1.2 Add Form Validation Functions to `calendar.html`
**File:** `app/templates/calendar.html` (or new `partials/_form-validation.html`)  
**Duration:** 20 min

**What to do:**
1. Add validations for event form fields:
   - `validateTitle(value)` → returns {valid: bool, error: string}
   - `validateDate(value)` → returns {valid: bool, error: string}
   - `validateTime(value)` → returns {valid: bool, error: string}
   - `isFormValid()` → returns bool (all required fields pass)
   - `updateSubmitButtonState()` → enables/disables submit button

2. Example JavaScript to add to `<script>` section in calendar.html:
   ```javascript
   function validateTitle(value) {
     const trimmed = value.trim();
     if (trimmed.length < 3) {
       return { valid: false, error: 'Title must be at least 3 characters' };
     }
     if (trimmed.length > 200) {
       return { valid: false, error: 'Title must not exceed 200 characters' };
     }
     return { valid: true, error: '' };
   }

   function validateDate(value) {
     if (!value) {
       return { valid: false, error: 'Please select a date' };
     }
     const selected = new Date(value);
     const today = new Date();
     today.setHours(0, 0, 0, 0);
     if (selected < today) {
       return { valid: false, error: 'Please select a date (not in the past)' };
     }
     return { valid: true, error: '' };
   }

   function validateTime(value) {
     if (!value) {
       return { valid: false, error: 'Please select a time' };
     }
     const parts = value.split(':');
     if (parts.length !== 2 || isNaN(parts[0]) || isNaN(parts[1])) {
       return { valid: false, error: 'Please enter a valid time (HH:MM)' };
     }
     return { valid: true, error: '' };
   }

   function isFormValid() {
     const title = document.getElementById('event-title')?.value || '';
     const date = document.getElementById('event-date')?.value || '';
     const time = document.getElementById('event-time')?.value || '';
     
     const titleValid = validateTitle(title).valid;
     const dateValid = validateDate(date).valid;
     const timeValid = validateTime(time).valid;
     
     return titleValid && dateValid && timeValid;
   }

   function updateSubmitButtonState() {
     const btn = document.getElementById('submit-event-btn') || 
                 document.querySelector('form button[type="submit"]');
     if (btn) {
       btn.disabled = !isFormValid();
     }
   }
   ```

3. Attach event listeners to form fields (in sidebar form):
   ```javascript
   const titleInput = document.getElementById('event-title');
   const dateInput = document.getElementById('event-date');
   const timeInput = document.getElementById('event-time');
   
   if (titleInput) {
     titleInput.addEventListener('input', (e) => {
       const validation = validateTitle(e.target.value);
       // Show/hide error (implementation in 1.3)
       updateSubmitButtonState();
     });
   }
   ```

**Acceptance:**
- [ ] Validation functions exist and return correct boolean/error pairs
- [ ] `isFormValid()` correctly checks all required fields
- [ ] `updateSubmitButtonState()` disables button when form invalid
- [ ] Event listeners attached to form inputs

---

### 1.3 Display Inline Errors in Sidebar Form
**File:** `app/templates/partials/event_form.html`  
**Duration:** 10 min

**What to do:**
1. Update each form field to include error message container:
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

2. Update validation listeners to show/hide errors:
   ```javascript
   titleInput.addEventListener('input', (e) => {
     const validation = validateTitle(e.target.value);
     const errorDiv = document.getElementById('event-title-error');
     if (validation.valid) {
       errorDiv.style.display = 'none';
       errorDiv.textContent = '';
     } else {
       errorDiv.style.display = 'block';
       errorDiv.textContent = validation.error;
     }
     updateSubmitButtonState();
   });
   ```

3. Update submit handler to prevent invalid submission:
   ```javascript
   form.addEventListener('submit', (e) => {
     if (!isFormValid()) {
       e.preventDefault();
       return false;
     }
     // Allow normal submission
   });
   ```

**Acceptance:**
- [ ] Error message containers exist for title, date, time fields
- [ ] Errors show in red below input when invalid
- [ ] Errors clear when user corrects input
- [ ] Form does not submit if any field invalid
- [ ] Submit button disabled when form invalid

---

## Wave 2: Event Entry Modal (Structure + Date/Time Inputs)

**Objective:** Create floating modal for event entry with separate date/time inputs.

**Tasks:**

### 2.1 Create Event Entry Modal HTML Partial
**File:** `app/templates/partials/event_entry_modal.html` (new)  
**Duration:** 20 min

**What to do:**
1. Create new partial file with modal structure:
   ```html
   <!-- Event Entry Modal -->
   <div id="event-entry-modal" class="fixed inset-0 z-50 hidden items-center justify-center">
     <!-- Backdrop -->
     <div id="event-modal-backdrop" class="absolute inset-0 bg-black/50" style="backdrop-filter: blur(3px);"></div>
     
     <!-- Modal Panel -->
     <div class="glass relative w-11/12 max-w-lg rounded-2xl p-6 shadow-2xl">
       <!-- Header with Close Button -->
       <div class="mb-4 flex items-center justify-between">
         <h2 class="text-xl font-semibold text-white">Add Event</h2>
         <button 
           type="button"
           id="close-event-modal-btn"
           class="glass-btn-secondary h-8 w-8 rounded-full p-0"
         >
           ×
         </button>
       </div>
       
       <!-- Form -->
       <form id="event-entry-form" class="space-y-4">
         <!-- Title -->
         <div>
           <label for="modal-event-title" class="mb-1 block text-xs font-medium uppercase tracking-wide text-white/60">
             Title *
           </label>
           <input 
             id="modal-event-title"
             type="text"
             required
             class="glass-input"
             minlength="3"
             maxlength="200"
             autofocus
           />
           <div class="text-red-500 text-xs mt-1" id="modal-event-title-error" style="display:none;"></div>
         </div>
         
         <!-- Date and Time -->
         <div class="grid grid-cols-2 gap-3 sm:gap-4">
           <div>
             <label for="modal-event-date" class="mb-1 block text-xs font-medium uppercase tracking-wide text-white/60">
               Date *
             </label>
             <input 
               id="modal-event-date"
               type="date"
               required
               class="glass-input text-center"
             />
             <div class="text-red-500 text-xs mt-1" id="modal-event-date-error" style="display:none;"></div>
           </div>
           <div>
             <label for="modal-event-time" class="mb-1 block text-xs font-medium uppercase tracking-wide text-white/60">
               Time *
             </label>
             <input 
               id="modal-event-time"
               type="time"
               required
               class="glass-input text-center"
             />
             <div class="text-red-500 text-xs mt-1" id="modal-event-time-error" style="display:none;"></div>
           </div>
         </div>
         
         <!-- End Time (Optional) -->
         <div>
           <label for="modal-event-end-time" class="mb-1 block text-xs font-medium uppercase tracking-wide text-white/60">
             End Time (optional)
           </label>
           <input 
             id="modal-event-end-time"
             type="time"
             class="glass-input text-center"
           />
           <div class="text-red-500 text-xs mt-1" id="modal-event-end-time-error" style="display:none;"></div>
         </div>
         
         <!-- Recurrence -->
         <div>
           <label for="modal-event-repeat" class="mb-1 block text-xs font-medium uppercase tracking-wide text-white/60">
             Repeat
           </label>
           <select id="modal-event-repeat" class="glass-input">
             <option value="NONE">Never</option>
             <option value="DAILY">Daily</option>
             <option value="WEEKLY">Weekly</option>
             <option value="MONTHLY">Monthly</option>
             <option value="YEARLY">Yearly</option>
           </select>
         </div>
         
         <!-- Buttons -->
         <div class="mt-6 flex gap-3 sm:gap-4">
           <button 
             type="button"
             id="cancel-event-btn"
             class="glass-btn-secondary flex-1"
           >
             Cancel
           </button>
           <button 
             type="submit"
             id="modal-submit-event-btn"
             class="glass-btn-primary flex-1"
             disabled
           >
             Save Event
           </button>
         </div>
       </form>
     </div>
   </div>
   ```

2. Add CSS to calendar.html or base.html for modal visibility: (if not already using hidden class)
   ```css
   #event-entry-modal.hidden {
     display: none;
   }
   #event-entry-modal:not(.hidden) {
     display: flex;
   }
   ```

**Acceptance:**
- [ ] Modal partial file created
- [ ] Modal renders with form fields (title, date, time, recurrence)
- [ ] Modal hidden by default
- [ ] Close button and cancel button both exist
- [ ] Form has submit button (disabled initially)

---

### 2.2 Integrate Modal into `calendar.html`
**File:** `app/templates/calendar.html`  
**Duration:** 5 min

**What to do:**
1. Add include statement before closing `</body>`:
   ```html
   {% include 'partials/event_entry_modal.html' %}
   ```

2. Verify modal appears in rendered page (use browser devtools)

**Acceptance:**
- [ ] Modal partial included in calendar.html
- [ ] Modal renders when page loads (hidden state)
- [ ] Modal HTML structure correct (no missing tags)

---

### 2.3 Add Modal Open/Close JavaScript
**File:** `app/templates/calendar.html`  
**Duration:** 10 min

**What to do:**
1. Add JavaScript functions to manage modal:
   ```javascript
   function openEventModal() {
     const modal = document.getElementById('event-entry-modal');
     const titleInput = document.getElementById('modal-event-title');
     modal.classList.remove('hidden');
     titleInput.focus();
   }

   function closeEventModal() {
     const modal = document.getElementById('event-entry-modal');
     const form = document.getElementById('event-entry-form');
     modal.classList.add('hidden');
     form.reset();
     document.getElementById('modal-submit-event-btn').disabled = true;
   }

   function toggleEventModal() {
     const modal = document.getElementById('event-entry-modal');
     if (modal.classList.contains('hidden')) {
       openEventModal();
     } else {
       closeEventModal();
     }
   }
   ```

2. Attach event listeners:
   ```javascript
   // Close button
   document.getElementById('close-event-modal-btn')?.addEventListener('click', closeEventModal);
   
   // Cancel button
   document.getElementById('cancel-event-btn')?.addEventListener('click', closeEventModal);
   
   // Backdrop click
   document.getElementById('event-modal-backdrop')?.addEventListener('click', closeEventModal);
   
   // Keyboard: Escape key
   document.addEventListener('keydown', (e) => {
     if (e.key === 'Escape') {
       const modal = document.getElementById('event-entry-modal');
       if (!modal.classList.contains('hidden')) {
         closeEventModal();
       }
     }
   });
   
   // Keyboard: E key to toggle modal
   document.addEventListener('keydown', (e) => {
     if (e.key === 'e' || e.key === 'E') {
       toggleEventModal();
     }
   });
   ```

3. Hook "Add Event"/"Use Manual Form" buttons to `openEventModal()`:
   ```javascript
   // Find existing buttons and update their handlers
   document.getElementById('add-event-btn')?.addEventListener('click', openEventModal);
   document.getElementById('use-manual-form-btn')?.addEventListener('click', openEventModal);
   ```

**Acceptance:**
- [ ] `openEventModal()` shows modal and focuses title input
- [ ] `closeEventModal()` hides modal and clears form
- [ ] Escape key closes modal
- [ ] E key opens/closes modal
- [ ] Close button, cancel button, and backdrop click all close modal

---

## Wave 3: Form Validation in Modal

**Objective:** Apply validation logic to modal form with real-time feedback.

**Tasks:**

### 3.1 Reuse Validation Functions for Modal Form
**File:** `app/templates/calendar.html` (extend existing validation functions)  
**Duration:** 15 min

**What to do:**
1. Update validation functions to work with both sidebar and modal forms (use input ID as parameter or by querying selector):
   ```javascript
   // Option A: Refactor to accept element IDs
   function validateTitle(inputId = 'event-title') {
     const input = document.getElementById(inputId);
     const value = input?.value || '';
     const trimmed = value.trim();
     if (trimmed.length < 3) {
       return { valid: false, error: 'Title must be at least 3 characters' };
     }
     if (trimmed.length > 200) {
       return { valid: false, error: 'Title must not exceed 200 characters' };
     }
     return { valid: true, error: '' };
   }

   // Option B: Keep generic, call for both forms
   function validateAllForms() {
     // Check sidebar form if visible
     const sidebarForm = document.getElementById('event-form');
     if (sidebarForm && sidebarForm.style.display !== 'none') {
       isFormValid(); // updates sidebar submit button
     }
     
     // Check modal form if visible
     const modalForm = document.getElementById('event-entry-form');
     if (modalForm && !document.getElementById('event-entry-modal').classList.contains('hidden')) {
       isModalFormValid(); // updates modal submit button
     }
   }

   function isModalFormValid() {
     const title = document.getElementById('modal-event-title')?.value || '';
     const date = document.getElementById('modal-event-date')?.value || '';
     const time = document.getElementById('modal-event-time')?.value || '';
     
     const titleValid = validateTitle(title).valid;
     const dateValid = validateDate(date).valid;
     const timeValid = validateTime(time).valid;
     
     return titleValid && dateValid && timeValid;
   }
   ```

2. Attach listeners to modal form inputs:
   ```javascript
   const modalTitleInput = document.getElementById('modal-event-title');
   const modalDateInput = document.getElementById('modal-event-date');
   const modalTimeInput = document.getElementById('modal-event-time');

   if (modalTitleInput) {
     modalTitleInput.addEventListener('input', updateModalValidation);
   }
   if (modalDateInput) {
     modalDateInput.addEventListener('change', updateModalValidation);
   }
   if (modalTimeInput) {
     modalTimeInput.addEventListener('change', updateModalValidation);
   }

   function updateModalValidation() {
     const titleValidation = validateTitle(document.getElementById('modal-event-title').value);
     const dateValidation = validateDate(document.getElementById('modal-event-date').value);
     const timeValidation = validateTime(document.getElementById('modal-event-time').value);
     
     showErrorIfInvalid('modal-event-title', titleValidation);
     showErrorIfInvalid('modal-event-date', dateValidation);
     showErrorIfInvalid('modal-event-time', timeValidation);
     
     updateModalSubmitButtonState();
   }

   function showErrorIfInvalid(inputId, validation) {
     const errorDiv = document.getElementById(`${inputId}-error`);
     if (errorDiv) {
       if (validation.valid) {
         errorDiv.style.display = 'none';
         errorDiv.textContent = '';
       } else {
         errorDiv.style.display = 'block';
         errorDiv.textContent = validation.error;
       }
     }
   }

   function updateModalSubmitButtonState() {
     const btn = document.getElementById('modal-submit-event-btn');
     if (btn) {
       btn.disabled = !isModalFormValid();
     }
   }
   ```

**Acceptance:**
- [ ] Validation functions work for both sidebar and modal
- [ ] Modal form errors show/hide correctly
- [ ] Submit button enabled/disabled based on form validity
- [ ] No console errors when typing in modal

---

### 3.2 Add Form Submission Handler for Modal
**File:** `app/templates/calendar.html` or `partials/event_entry_modal.html`  
**Duration:** 15 min

**What to do:**
1. Update modal form submit handler:
   ```javascript
   document.getElementById('event-entry-form')?.addEventListener('submit', async (e) => {
     e.preventDefault();
     
     // Final validation check
     if (!isModalFormValid()) {
       return;
     }
     
     const submitBtn = document.getElementById('modal-submit-event-btn');
     submitBtn.disabled = true;
     submitBtn.textContent = 'Saving...';
     
     try {
       const title = document.getElementById('modal-event-title').value.trim();
       const date = document.getElementById('modal-event-date').value;
       const time = document.getElementById('modal-event-time').value;
       const endTime = document.getElementById('modal-event-end-time')?.value || time;
       const repeat = document.getElementById('modal-event-repeat')?.value || 'NONE';
       
       // Combine date and time into ISO 8601 datetime
       const startDateTime = `${date}T${time}:00`;
       const endDateTime = `${date}T${endTime}:00`;
       
       const response = await fetch('/api/events', {
         method: 'POST',
         headers: { 'Content-Type': 'application/json' },
         body: JSON.stringify({
           title: title,
           start_time: startDateTime,
           end_time: endDateTime,
           event_repeat: repeat === 'NONE' ? null : repeat,
         })
       });
       
       if (response.ok) {
         const event = await response.json();
         console.log('Event created:', event);
         closeEventModal();
         // Refresh calendar view (e.g., reload current month)
         location.reload(); // Simple approach; can be optimized
       } else {
         const error = await response.json();
         alert(`Error: ${error.detail || 'Failed to create event'}`);
         submitBtn.textContent = 'Save Event';
         submitBtn.disabled = false;
       }
     } catch (error) {
       console.error('Error creating event:', error);
       alert('Error creating event. Please try again.');
       submitBtn.textContent = 'Save Event';
       submitBtn.disabled = false;
     }
   });
   ```

2. Verify modal closes on successful submission
3. Verify error message displays on failure
4. Verify calendar refreshes with new event

**Acceptance:**
- [ ] Form submits valid data to `/api/events` POST
- [ ] Modal closes on success
- [ ] Calendar refreshes to show new event
- [ ] Error message displays on failure
- [ ] Submit button re-enabled if submission fails
- [ ] No double-submit (button disabled after click)

---

## Wave 4: Keyboard Shortcuts + Mobile Polish + Tests

**Objective:** Final polish: keyboard shortcuts, mobile responsiveness, test coverage.

**Tasks:**

### 4.1 Verify Keyboard Shortcuts (E, Escape)
**Duration:** 5 min

**What to do:**
1. Test in browser:
   - Press E key → modal opens
   - Press Escape → modal closes
   - Press Tab → focus cycles through form fields
   - Press Enter → submit form (if focus on submit button)

2. If shortcuts not working, check that event listeners are attached (troubleshoot console errors)

**Acceptance:**
- [ ] E key opens modal
- [ ] Escape closes modal
- [ ] Tab cycles focus
- [ ] Enter submits when focus on button

---

### 4.2 Mobile Responsiveness Audit
**Duration:** 10 min

**What to do:**
1. Open DevTools (F12) and toggle device toolbar (Ctrl+Shift+M)
2. Test modal at 375px width (iPhone SE):
   - Modal is full-width with padding (not edge-to-edge)
   - Form fields stack vertically (not 2-column grid)
   - Buttons are 44px+ tall (tap-friendly)
   - Text is readable without zooming
   - No horizontal scroll

3. Update modal CSS if needed:
   ```css
   @media (max-width: 556px) {
     /* Mobile: Single-column layout */
     .grid.grid-cols-2 {
       grid-template-columns: 1fr;
     }
     
     /* Buttons: Full width, taller */
     button { min-height: 44px; }
   }
   ```

**Acceptance:**
- [ ] Modal responsive at 375px (mobile)
- [ ] Modal responsive at 1024px (desktop)
- [ ] No horizontal scroll on mobile
- [ ] Buttons 44px+ tall
- [ ] Text readable without zooming

---

### 4.3 Add Unit Tests for Validation Functions
**File:** `tests/test_form_validation.py` (new, or update existing)  
**Duration:** 10 min

**What to do:**
1. Manual browser testing (add automated tests later if needed):
   - Test Title validation:
     - Input: "" → Error "Title must be at least 3 characters"
     - Input: "ab" → Error
     - Input: "abc" → Valid
     - Input: "a" × 201 chars → Error "must not exceed 200"
   
   - Test Date validation:
     - Input: "" → Error "Please select a date"
     - Input: yesterday date → Error "not in the past"
     - Input: today date → Valid
     - Input: tomorrow date → Valid
   
   - Test Time validation:
     - Input: "" → Error "Please select a time"
     - Input: "14:30" → Valid
     - Input: "25:00" → Error (invalid by browser, automatically rejected)
   
   - Test isFormValid():
     - Empty form → false
     - Title only → false
     - Title + date → false
     - Title + date + time → true

2. If using pytest, add JavaScript testing (optional):
   ```python
   # tests/test_form_validation.py
   def test_validation_functions_exist(client):
       """Verify validation JS functions are present in calendar page"""
       response = client.get('/calendar')
       assert 'validateTitle' in response.text
       assert 'validateDate' in response.text
       assert 'validateTime' in response.text
       assert 'isFormValid' in response.text
   ```

**Acceptance:**
- [ ] All validation rules tested manually (form title, date, time)
- [ ] No console errors in DevTools
- [ ] Submit button state updates correctly
- [ ] All 52 existing tests still pass

---

### 4.4 Run Full Test Suite
**Duration:** 5 min

**What to do:**
1. Terminal command:
   ```bash
   .venv\Scripts\python.exe -m pytest tests/ -q
   ```

2. Verify: All tests pass (52/52 or higher)

3. If tests fail:
   - Check error output
   - Fix issues before committing

**Acceptance:**
- [ ] All tests pass
- [ ] No regressions from modal/validation changes
- [ ] Coverage report shows good coverage

---

## How to Execute This Plan

### Sequential Execution (Recommended)

1. **Session 1: Wave 1** (30–40 min)
   - Add back button to invite.html
   - Add validation functions
   - Display inline errors
   - Test sidebar form validation

2. **Session 2: Wave 2** (45–50 min)
   - Create modal partial
   - Integrate into calendar.html
   - Add open/close JavaScript

3. **Session 3: Wave 3** (30 min)
   - Apply validation to modal
   - Add form submission handler
   - Test modal submission

4. **Session 4: Wave 4** (25–30 min)
   - Verify keyboard shortcuts
   - Test mobile responsiveness
   - Run full test suite
   - Commit changes

### Or Use `/gsd-execute-phase` 

If using GSD automated execution:
```bash
/gsd-execute-phase 07
```

This will:
1. Read this plan
2. Execute each wave in parallel (where dependencies allow)
3. Commit changes after each wave
4. Track progress in `.planning/phases/07-*/EXECUTION.md`

---

## Success Metrics

After completing all 4 waves, verify:

| Metric | Target | Status |
|--------|--------|--------|
| Back button works | ✓ navigates to /calendar | [ ] |
| Modal opens/closes | ✓ E key, Escape key, button clicks | [ ] |
| Form validation | ✓ submit button state correct | [ ] |
| Date/time inputs | ✓ native pickers work | [ ] |
| Error feedback | ✓ inline errors show/hide | [ ] |
| Keyboard navigation | ✓ Tab, Enter, Escape work | [ ] |
| Mobile responsive | ✓ full-width, 44px+ buttons | [ ] |
| Test pass rate | ✓ 52/52 passing | [ ] |
| No regressions | ✓ existing features still work | [ ] |

---

## Notes & Gotchas

- **Date format:** HTML `<input type="date">` uses YYYY-MM-DD. Convert to ISO 8601 datetime when submitting.
- **Time format:** HTML `<input type="time">` uses HH:MM (24-hour). No seconds in input; append `:00` on submission.
- **Validation timing:** Only show error after user interacts (blur or change event), not on page load (otherwise form looks broken at start).
- **Button state:** Disable submit button until all required fields are valid. This prevents server-side validation and improves UX.
- **Mobile testing:** Always test on actual mobile or DevTools device emulator. Tap targets must be 44×44px minimum.
- **Keyboard focus:** After modal closes, return focus to the "Add Event" button to maintain accessibility.

---

## Files to Modify

| File | Change | Waves |
|------|--------|-------|
| `invite.html` | Add back button | 1 |
| `event_form.html` | Update error display | 1 |
| `calendar.html` | Add validation JS, modal JS, form submit handler | 2, 3 |
| `partials/event_entry_modal.html` | Create (new file) | 2 |
| `tests/` | Verify passing (no new tests required) | 4 |

---

*Plan created: 2026-03-19*  
*Next step: Execute Wave 1*

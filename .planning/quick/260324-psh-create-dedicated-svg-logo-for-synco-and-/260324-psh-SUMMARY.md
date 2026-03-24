---
quick_id: 260324-psh
status: complete
started: 2026-03-24T17:34:10Z
completed: 2026-03-24T17:40:00Z
commits:
  - hash: 03f92b3
    message: "feat(branding): add dedicated SVG logo and replace inline star/calendar SVGs"
---

## What Changed

Created a dedicated SVG logo for Synco (`public/icons/logo.svg`) and replaced all inline SVGs used as brand marks across templates.

### Logo Design
- **Concept:** Calendar body (rounded rect) with two sync-cycle arrows inside, matching the "Synco" name
- **Colors:** Indigo (#6366f1) → Purple (#8b5cf6) gradient matching the design system
- **Format:** SVG for infinite scalability (works at 16px favicon and 512px app icon)

### Files Modified

| File | Change |
|------|--------|
| `public/icons/logo.svg` | New file — dedicated logo mark |
| `app/templates/landing.html` | Replaced navbar star SVG with `<img>` logo; updated favicon to SVG file ref |
| `app/templates/base.html` | Replaced navbar star SVG with `<img>` logo; updated favicon to SVG file ref |
| `public/offline.html` | Replaced star SVG with `<img>` logo |

### Not Changed (by design)
- `billing_settings.html` star SVGs — these are Pro plan tier badges, not brand logos

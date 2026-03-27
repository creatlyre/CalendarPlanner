# Summary: 260327-ko6 — Fix Mobile Nav Overflow

## Problem
Desktop navigation links (5 pages + admin + Quick Add) appeared at the `md` breakpoint (768px), overflowing on tablets and large phones. The mobile bottom nav simultaneously hid at the same 768px threshold, leaving no usable navigation on 768–1023px screens.

## Solution
Raised all navigation breakpoints from `md` (768px) to `lg` (1024px):

- **base.html**: Changed 7× `hidden md:inline-flex` → `hidden lg:inline-flex` for desktop nav links; changed FAB `md:hidden` → `lg:hidden`
- **input.css**: Changed `@media (max-width: 767px)` → `@media (max-width: 1023px)` for mobile-compact styles; changed `@media (min-width: 768px)` → `@media (min-width: 1024px)` for hiding `.mobile-bottom-nav`
- **style.css**: Rebuilt via Tailwind CLI

## Files Changed
| File | Change |
|------|--------|
| app/templates/base.html | 8 class changes (md→lg) |
| public/css/input.css | 2 media query threshold changes |
| public/css/style.css | Rebuilt |

## Verification
All 5 must-have truths confirmed. No `767px`/`768px` breakpoints remain in built CSS.

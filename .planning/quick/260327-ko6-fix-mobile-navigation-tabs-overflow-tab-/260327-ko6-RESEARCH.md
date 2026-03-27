# Quick Task 260327-ko6: Mobile Nav Overflow - Research

## Problem Analysis

The top nav bar overflows on devices with viewport widths between 768px-1023px (tablets, large phones). The desktop nav links use `hidden md:inline-flex` showing at 768px+, but there are too many items to fit:
- Brand "Dobry Plan" (takes ~120px)
- 5 nav links: Główna, Kalendarz, 💰 Budżet, 🛒 Zakupy, Plan (~450px total)
- Quick Add button (~100px)
- Theme toggle, notifications, language switcher, logout (~220px)

Total ~890px needed vs 768px available = overflow.

## Files Requiring Changes

### 1. `app/templates/base.html`
- **Lines 31-39**: 6 nav links use `hidden md:inline-flex` → change to `hidden lg:inline-flex`
- **Line 47**: Quick Add button uses `hidden md:inline-flex` → change to `hidden lg:inline-flex`
- **Line 195**: FAB button uses `md:hidden` → change to `lg:hidden`

### 2. `public/css/input.css`
- **Line 817**: `@media (max-width: 767px)` → change to `@media (max-width: 1023px)`
- **Line 1171**: `@media (min-width: 768px) { .mobile-bottom-nav { display: none; } }` → change to `@media (min-width: 1024px)`

### 3. `public/css/style.css` (rebuilt from input.css via Tailwind)
- Must be rebuilt after input.css changes

## Approach

Raise the desktop nav appearance breakpoint from `md` (768px) to `lg` (1024px):
- Simple, low-risk change
- Consistent with the existing mobile bottom nav design
- Tablets/large phones use the well-designed bottom nav
- No layout redesign needed

## Pitfalls
- The mobile-specific CSS rules (max-width: 767px) need to be raised to 1023px too, otherwise devices between 768-1023px won't get compact nav styling
- Must rebuild the Tailwind CSS output after template class changes
- Budget sidebar nav pills also use `lg:flex-col` which already works correctly

# Quick Task 260327-ko6: Fix mobile navigation tabs overflow - Context

**Gathered:** 2026-03-27
**Status:** Ready for planning

<domain>
## Task Boundary

Fix the top navigation bar overflowing on mobile/tablet devices. Currently the desktop nav links use `md:inline-flex` (768px+) which causes them to show on devices that are too narrow to fit all items. The mobile bottom nav hides at the same 768px breakpoint, creating a problematic transition gap.

</domain>

<decisions>
## Implementation Decisions

### Breakpoint Strategy
- Raise all desktop nav link breakpoints from `md` (768px) to `lg` (1024px)
- This gives enough room for brand + 5 nav links + utility buttons

### Mobile Bottom Nav
- Keep mobile bottom nav visible up to `lg` (1024px) instead of current `md` (768px)
- 768-1024px devices will use the bottom nav for page navigation

### Top Bar on Tablets (768-1024px)
- Show only: brand, theme toggle, notification bell, language switcher, logout
- Hide: nav links and Quick Add button (available via bottom nav + FAB)

### Claude's Discretion
- Exact styling adjustments for the 768-1024px range

</decisions>

<specifics>
## Specific Ideas

- The desktop nav links in base.html use `hidden md:inline-flex` — change to `hidden lg:inline-flex`
- Quick Add button uses `hidden md:inline-flex` — change to `hidden lg:inline-flex`
- Mobile bottom nav CSS: change `@media (min-width: 768px) { .mobile-bottom-nav { display: none; } }` to use 1024px
- The `body { padding-bottom: 4.5rem; }` rule needs to stay active until lg breakpoint
- The FAB button already uses `md:hidden` — should be `lg:hidden`

</specifics>

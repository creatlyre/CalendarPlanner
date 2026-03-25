# Dobry Plan — Brand Guide

> Single source of truth for the Dobry Plan visual identity.

## Colors

### Primary Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--brand-bg` | `#0f0a2e` | Page background, dark surfaces |
| `--brand-primary` | `#6366f1` | Primary actions, links, highlights (Indigo 500) |
| `--brand-accent` | `#8b5cf6` | Gradients, secondary highlights (Violet 500) |
| `--brand-success` | `#34d399` | Positive indicators, confirmations (Emerald 400) |

### Extended Palette

| Name | Hex | Context |
|------|-----|---------|
| Card bg base | `#1a1444` / `rgba(26,20,68,*)` | Card/panel gradient start |
| Nav bg | `rgba(15,10,46,0.85)` | Sticky nav with backdrop-blur |
| CTA gradient | `#6366f1 → #8b5cf6` | Primary call-to-action buttons |
| CTA hover | `#818cf8 → #a78bfa` | Hover state for CTA buttons |
| Text gradient | `#c7d2fe → #a5b4fc → #818cf8 → #c084fc` | Hero headline accent |
| PWA theme | `#1e1553` | `<meta name="theme-color">` and manifest |

### RGB Values (for rgba usage)

| Token | RGB | Example |
|-------|-----|---------|
| `--brand-bg-rgb` | `15, 10, 46` | `rgba(var(--brand-bg-rgb), 0.85)` |
| `--brand-card-rgb` | `26, 20, 68` | Card gradient overlays |
| `--brand-primary-rgb` | `99, 102, 241` | Glow effects, transparent overlays |
| `--brand-accent-rgb` | `139, 92, 246` | Accent glow effects |

## Typography

| Role | Font | Weights | Usage |
|------|------|---------|-------|
| Display | Plus Jakarta Sans | 500, 600, 700, 800 | Headings, nav brand, pricing titles |
| Body | DM Sans | 400, 500, 600 (+ italic) | Body text, labels, descriptions |
| Code | JetBrains Mono | 400 | Code snippets (admin/dev pages only) |

### CSS Classes

- `.font-display` → Plus Jakarta Sans
- Default body → DM Sans
- Tailwind `font-mono` → JetBrains Mono

## Logo Files

| File | Format | Size | Purpose |
|------|--------|------|---------|
| `public/icons/logo.svg` | SVG | 32×32 viewBox | Favicon, inline icon |
| `public/images/logo-mark.webp` | WebP | Small | Nav logo mark |
| `public/images/logo-wordmark.webp` | WebP | Wide | OG images, social cards |
| `public/icons/icon-192.png` | PNG | 192×192 | PWA icon |
| `public/icons/icon-512.png` | PNG | 512×512 | PWA splash |
| `public/icons/logo-app-512.png` | PNG | 512×512 | App store icon, apple-touch-icon |
| `public/icons/icon-maskable-192.png` | PNG | 192×192 | PWA maskable (safe zone) |
| `public/icons/icon-maskable-512.png` | PNG | 512×512 | PWA maskable (safe zone) |

### Logo Usage

- **Nav:** Use `logo-mark.webp` (small, rounded) next to app name text
- **Favicon:** SVG `logo.svg` with PNG fallback `icon-192.png`
- **Social/OG:** Use `logo-wordmark.webp` for Open Graph images
- **PWA install:** Use `logo-app-512.png` for apple-touch-icon and high-res icon
- **Minimum size:** Logo mark should not appear smaller than 24×24px
- **Clear space:** Maintain at least 4px padding around the logo mark

### Logo Design

The logo is a calendar icon with sync arrows, rendered in an indigo-to-violet gradient. It communicates the core value: a synchronized household calendar.

## Tone & Voice

- **Friendly and practical** — not corporate, not overly casual
- **Outcome-focused** — describe what users achieve, not technical features
- **Polish household context** — relatable to couples and families managing daily life
- **Positioning:** "Your household, finally in sync" (PL: "Twój dom, wreszcie ogarnięty")

### Do

- Use "you" and "your" to address the user directly
- Lead with benefits: "See everyone's schedule in one place"
- Keep sentences short and scannable
- Use the brand name "Dobry Plan" (not "DP" or abbreviations)

### Don't

- Use jargon: "NLP parsing", "OCR engine", "CRUD operations"
- Overclaim: "The best calendar app ever"
- Use passive voice in CTAs: "An account can be created" → "Create your account"

## Contrast Requirements

All text must meet WCAG AA contrast ratios against the dark background (#0f0a2e):

| Text Class | Ratio vs #0f0a2e | Status |
|-----------|-------------------|--------|
| `text-white` | 16.7:1 | ✅ Pass |
| `text-gray-300` | 9.5:1 | ✅ Pass |
| `text-gray-400` | 5.5:1 | ✅ Pass AA |
| `text-gray-500` | 3.3:1 | ❌ Fail AA (use gray-400 for body text) |
| `text-indigo-400` | 4.8:1 | ✅ Pass AA |
| `text-emerald-400` | 6.2:1 | ✅ Pass AA |

**Rule:** Never use `text-gray-500` for readable body text on the dark background. Use `text-gray-400` minimum.

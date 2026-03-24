---
created: 2026-03-24T15:49:56.095Z
title: "Design main page branding - logo and background imagery"
area: ui
files:
  - app/templates/landing.html
  - public/icons/
  - public/css/style.css
---

## Problem

The Synco landing page (`app/templates/landing.html`) currently uses a simple star icon + text for the logo and animated decorative CSS orbs for background. There is no distinctive brand logo or curated background imagery. The page would benefit from a proper logo mark and a hero background image/illustration to establish stronger visual identity.

Current state:
- Logo: inline SVG star icon with "Synco" text in the navbar
- Background: dark navy `#0f0a2e` with animated gradient orbs (pure CSS)
- App icons: generic calendar icons in `public/icons/`
- Design system: dark theme, indigo→purple gradient accents, Plus Jakarta Sans / DM Sans fonts

## Solution

Use AI image generation to create:

### 1. Logo

**Prompt for AI logo generation:**
> Design a modern, minimal logomark for "Synco" — a calendar planning and budgeting web app. The logo should combine a subtle calendar/planner motif with a sync/flow concept (reflecting the name "Synco"). Use clean geometric shapes. Color palette: indigo (#6366f1) to purple (#8b5cf6) gradient on a transparent background. Style: flat, modern SaaS logo — no gradients on the mark itself, just solid shapes that work at 16px favicon and 512px app icon sizes. Think Notion, Linear, or Cal.com aesthetic. Output as SVG.

### 2. Background Hero Image/Illustration

**Prompt for AI background generation:**
> Create an abstract, dark-themed hero background illustration for a SaaS landing page. Deep navy base (#0f0a2e) with subtle flowing geometric shapes, soft glowing indigo (#6366f1) and purple (#8b5cf6) light trails or mesh gradients. The design should feel premium, modern, and slightly futuristic — like a constellation map or data-flow visualization fading into the dark background. No text, no people. Ultra-wide aspect ratio (roughly 1920×900). The image should be subtle enough to serve as a background behind white text and UI elements without competing for attention.

### Implementation
- Replace the star SVG logo in the navbar and footer with the new logo
- Regenerate PWA icons (icon-192, icon-512, maskable variants) from the new logo
- Update the og-image.png for social sharing
- Add the hero background image to the landing page hero section (with fallback to current CSS orbs)
- Optimize images (WebP, lazy-loading, appropriate compression)

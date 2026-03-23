# Phase 25: Shopping List - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Shared household shopping list with add/delete, multi-item paste, and **store-section grouping** that auto-categorizes items by Biedronka aisle layout for route-optimized shopping. Both household users share the same list.

**Requirement deviation:** SHOP-03 (check off / uncheck) is **replaced** by simple delete. User explicitly chose no check/uncheck — items are either on the list or removed. Edit is supported for corrections.

</domain>

<decisions>
## Implementation Decisions

### Item Lifecycle
- Items support **add, edit, and delete** only — no check/uncheck toggle
- Quantities and details are part of the free-text item name (e.g., "masło x4", "2 kg ziemniaków")
- No per-item notes/hints field — plain text only
- Items are free-text strings, no structured quantity/unit/price fields (per out-of-scope)

### Store-Section Grouping (Core Feature)
- Items are **auto-categorized** into store sections via keyword mapping (same pattern as `app/budget/category_keywords.json`)
- Grouping by section is the primary value — keeps related items together so user doesn't backtrack through aisles
- Section order is a nice-to-have; what matters is items are grouped, not interleaved
- **10 preset Biedronka sections** in default store-walk order:
  1. 🍅 Warzywa i Owoce (Produce)
  2. 🥩 Lada Tradycyjna / Mięso (Deli / Meat)
  3. 🐟 Ryby (Fish)
  4. 🧀 Nabiał i Lodówki (Dairy / Refrigerated)
  5. 🥫 Puszki, Sosy, Przetwory (Canned / Sauces)
  6. 🧁 Pieczenie / Bakalie (Baking / Nuts)
  7. 👶 Dział Dziecięcy (Baby)
  8. 🧃 Napoje (Drinks)
  9. 🍺 Alkohol (Alcohol)
  10. 🧻 Chemia / Higiena (Cleaning / Hygiene)
- Sections are editable — user can add, rename, reorder, or delete sections

### Unknown Item Learning
- When an item can't be auto-categorized, **prompt user to pick a section**
- **Save the user's choice** so the system remembers for next time (user-trained keyword mapping)
- Ambiguous items (e.g., "ananas" = fresh or canned) default to the most common category; user can reassign

### Multi-Item Input
- Supports **comma-separated** and **newline-separated** input for bulk adding
- Single items via text input + Enter
- No preview step — items are added instantly and auto-categorized

### Sharing Model
- One shared list per household (tied to `calendar_id`, same as all other shared features)
- Both users see the same list in real-time (page refresh)
- No attribution of who added what (not needed per user)

### Claude's Discretion
- Keyword mapping JSON structure and initial keyword set
- API endpoint design (REST pattern matching existing budget/events)
- DB table/migration structure
- UI layout details within existing glass-morphism design system
- Polling vs manual refresh for partner changes

</decisions>

<specifics>
## Specific Ideas

- User's mental model: "Biedronka optimized shopping route" — the list matches physical store aisles so you walk the store once without backtracking
- The keyword mapping should ship with a rich Polish grocery vocabulary (the user's examples include ~50+ common items spanning all 10 sections)
- Sections use emoji prefixes for quick visual scanning (🍅🥩🐟🧀🥫🧁👶🧃🍺🧻)
- The learning system is like "ML where the user is the input" — each unknown item prompt enriches the keyword DB for future use

</specifics>

<canonical_refs>
## Canonical References

No external specs — requirements are fully captured in decisions above.

### Codebase patterns to follow
- `.planning/REQUIREMENTS.md` — SHOP-01 through SHOP-05 (note: SHOP-03 modified per user decision)
- `app/budget/category_keywords.json` — Keyword-to-category mapping pattern to replicate for store sections

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `app/budget/category_keywords.json` — exact same pattern needed for shopping item → store section mapping
- `app/database/supabase_store.py` — `SupabaseStore` with select/insert/update/delete for all DB operations
- `app/database/models.py` — dataclass pattern for all models (User, Event, Expense, EventCategory, etc.)
- `app/templates/base.html` — glass-morphism nav with mobile bottom bar (needs 4th "Shopping" tab)
- `app/i18n.py` + `app/locales/{en,pl}.json` — bilingual localization for all new strings

### Established Patterns
- API routes: `FastAPI APIRouter` with `/api/shopping` prefix (matches `/api/budget`, `/api/events`)
- View routes: separate `*_views.py` for HTML template rendering
- Repository layer: `*_repository.py` for DB operations via `SupabaseStore`
- Service layer: `*_service.py` for business logic
- Schemas: Pydantic models in `*_schemas.py`
- Models: dataclasses in `app/database/models.py`

### Integration Points
- `main.py` — register new shopping routers (API + views)
- `app/templates/base.html` — add Shopping nav link (desktop + mobile bottom bar)
- `supabase/migrations/` — new migration for shopping tables
- `app/locales/en.json` + `app/locales/pl.json` — new i18n keys

</code_context>

<deferred>
## Deferred Ideas

- Shopping list change notifications (tracked as NOTIF-09 in future requirements)
- Multiple shopping lists (explicitly out of scope)
- Quantities/units/prices as structured fields (explicitly out of scope — free-text is sufficient)

</deferred>

---

*Phase: 25-shopping-list*

# Quick Task 260327-jif: Biedronka Shopping Item Categorization - Research

**Researched:** 2026-03-27
**Domain:** Polish grocery item categorization / substring keyword matching
**Confidence:** HIGH

## Summary

The current keywords.json has 462 keywords across 10 sections but has **critical coverage gaps**: bread/bakery items, frozen foods, ready meals, pet food, and many common pantry/household items are completely uncategorized. Testing common Biedronka items reveals ~35% of a typical shopping list would fail categorization.

Additionally, the reverse-match logic (`norm in norm_kw` for items ≥3 chars) causes **false positives**: "mak" (poppy seeds) matches "makrela" in Ryby, "sos" (sauce) matches "łosoś" in Ryby. These must be fixed alongside the keyword expansion.

**Primary recommendation:** Add ~150-200 new keywords to keywords.json covering all identified gaps. Fix short-keyword collision bugs by using trailing spaces or more specific stems. Then generate 10×100 test lists and validate ≥95% categorization rate.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- UPDATE keywords.json with all missing items — goal is a complete keyword list
- Save categorization results as JSON files
- Generic human-style names like "mleko", "chleb", "masło" — NOT brand-specific
- 95%+ categorization rate target
- 10 lists × 100 items = 1000 total categorization attempts

### Claude's Discretion
- Script location and naming
- Exact item generation approach (curated realistic lists vs purely random)
- Whether to run as standalone script or pytest
</user_constraints>

## Current State Analysis

### Keywords per Section
| Section | Keywords | Coverage Quality |
|---------|----------|-----------------|
| Warzywa i Owoce | 88 | Good — comprehensive fruits/vegs/herbs |
| Lada Tradycyjna / Mięso | 54 | Good — meats and cold cuts well covered |
| Ryby | 32 | Adequate — common fish present |
| Nabiał i Lodówki | 49 | Good dairy, but missing ready meals |
| Puszki, Sosy, Przetwory | 61 | Good pantry staples, acts as catch-all dry goods |
| Pieczenie / Bakalie | 40 | Good baking, some overlaps with Puszki |
| Dział Dziecięcy | 22 | Minimal — only baby items |
| Napoje | 25 | Adequate — common drinks |
| Alkohol | 31 | Adequate — Polish beer/vodka brands |
| Chemia / Higiena | 60 | Good cleaning/hygiene, missing some household |

**Total: 462 keywords**

## Critical Coverage Gaps

### Gap 1: Bread / Bakery (COMPLETELY MISSING)
Biedronka has a dedicated pieczywo section. ZERO bread items are in keywords.json.

**Failing items:** chleb, bułka, bułki, rogal, rogalik, bagietka, croissant, drożdżówka, pączek, tort, ciasto, sernik, szarlotka, babka, makowiec, chleb tostowy, chleb żytni, bułka grahamka, wafle ryżowe

**Recommended section:** Split between:
- Fresh bread/pastries → **Pieczenie / Bakalie** (baking section = closest match)
- Cakes/tarts → **Pieczenie / Bakalie**

### Gap 2: Frozen Foods (NO COVERAGE)
**Failing items:** pizza mrożona, frytki, mrożonki, warzywa mrożone, lody (lody IS covered in Nabiał), pyzy, knedle mrożone, krokiety, naleśniki mrożone, ryba panierowana

**Recommended mapping:**
- Frozen vegetables → Warzywa i Owoce (add "mrożon warz", "mieszanka warz")
- Frozen fish/meat → Ryby / Mięso (add "ryba paniero", "nuggetsy")
- Frozen ready meals → Nabiał i Lodówki (the fridge/freezer section)
- Generic "mrożonki" → Nabiał i Lodówki

### Gap 3: Ready Meals / Deli
**Failing items:** pierogi, naleśniki, sałatka gotowa, danie gotowe, zupa instant, zupka chińska, kanapka, sushi

**Recommended section:** Nabiał i Lodówki (fridge section in Biedronka) or Puszki (for shelf-stable)

### Gap 4: Pet Food (NO COVERAGE)
**Failing items:** karma dla kota, karma dla psa, żwirek, przysmak dla psa

**Recommended section:** Chemia / Higiena (same aisle at Biedronka)

### Gap 5: Common Pantry Items Missing from Puszki
**Failing items:** bulion, kostka rosołowa, soda oczyszczona, panierka, bułka tarta, zupa w proszku

### Gap 6: Common Snacks Missing
**Failing items:** baton, batonik, ciastka, wafle, paluszki (some covered), popcorn, żelki, lizak

### Gap 7: Household Items Missing from Chemia
**Failing items:** żarówka, tabletki do zmywarki, płyn do płukania, żel do włosów, lakier do włosów, plaster, aspiryna, wkładki higieniczne

## Keyword Matching Pitfalls

### Bug 1: Reverse-match causes false positives (CRITICAL)
The engine has a reverse-match: `if len(norm) >= 3 and norm in norm_kw`. This means short item names match INSIDE long keywords.

| Item typed | Normalized | Matches keyword | Section (WRONG) | Should be |
|------------|-----------|----------------|-----------------|-----------|
| "mak" | "mak" | "makrela" | Ryby | Pieczenie / Bakalie |
| "sos" | "sos" | "losos" (łosoś) | Ryby | Puszki, Sosy, Przetwory |
| "sok" | "sok" | "sok" | Napoje (correct) | — |

**Fix:** The reverse match is useful for "ryb" matching items, but causes collisions. Solutions:
1. Add explicit keyword entries for these short words in their correct section (they'll match via `norm_kw in norm` before reverse-match triggers)
2. Actually, existing logic does `norm_kw in norm` first, then reverse. So if "mak" is already a keyword in Pieczenie, it depends on iteration ORDER. Since Ryby comes before Pieczenie in JSON, "makrela" reverse-matches first. **The fix is to add "mak " (with trailing space) won't work because user types just "mak".**

**Real fix approach:** For items like "mak" that are exactly 3 chars, the person likely means poppy seeds (mak = poppy). But the reverse match finds "makrela" in Ryby first. The item "mak" literally IS the keyword "mak" in Pieczenie, but since sections iterate in JSON order and Ryby comes first, the reverse match against "makrela" wins. **Solution: add check `if norm == norm_kw` (exact match) as highest priority before substring checks, OR reorder sections so Pieczenie comes before Ryby (fragile). Best: add the exact short keywords as their full word forms instead.**

### Bug 2: "ser " trailing space pattern
The keyword "ser " has trailing space to avoid matching "ser-wis", "serek" etc. But this means someone typing just "ser" (without trailing text) won't match! They'd need to type "ser żółty" or "ser gouda". Since "serek" is a separate keyword, "ser" alone fails. **Fix: add "ser" without space (it will match "ser", "serek", "ser żółty" etc. — but conflicts with words containing "ser" like "serwetki" in Chemia. The current trailing-space approach is intentional. "ser" alone is uncommon enough to accept this tradeoff, OR add "ser" as exact-match keyword.**

### Bug 3: "masło orzechowe" goes to Nabiał instead of Pieczenie
"masło" keyword in Nabiał matches before "krem orzechow" in Pieczenie. Fix: add "masło orzech" or "maslo orzech" to Pieczenie section keywords (it would need to appear BEFORE Nabiał in iteration, but since Nabiał is section 4 and Pieczenie is section 6, this won't help). **Better fix: add "orzechow" to Pieczenie; or accept current behavior since peanut butter IS near dairy in some stores.**

### Short keyword collision risk summary
| Keyword | Length | In Section | False positive risk |
|---------|--------|------------|-------------------|
| "sos" | 3 | Puszki | Matches "losos" in Ryby via reverse |
| "mak" | 3 | Pieczenie | Matches "makrela" in Ryby via reverse |
| "sol" | 3 | Puszki | Low risk — "sol" substring unlikely |
| "ryz" | 3 | Puszki | Low risk |
| "kaw" | 3 | Puszki | Low risk |
| "gin" | 3 | Alkohol | Could match "ginekolog" but unlikely grocery |
| "rum" | 3 | Alkohol | Could match "rumianek" (chamomile tea) via reverse — BUG |
| "ryb" | 3 | Ryby | Low risk |
| "sok" | 3 | Napoje | Matches correctly |

**"rum" → "rumianek" collision:** Someone typing "rum" (3 chars) would reverse-match "rumianek" if it existed. Currently "rumianek" is NOT a keyword, but if we add herbal teas, this becomes a problem. Not an issue today.

## Complete Missing Items by Section

### Pieczenie / Bakalie (BREAD + BAKING additions needed)
```
chleb, bułka, bułki, rogal, rogalik, bagietka, bagiet, croissant, 
drożdżówka, pączek, pączki, tort, ciasto, sernik, szarlotka, babka, 
makowiec, chleb tostowy, bułka tart, graham, wafle ryżow, 
ciastka, ciasteczk, herbatnik, kruche, pirog, soda oczyszczon,
kwasek cytryn, cukier wanili, aromat, esencja
```

### Nabiał i Lodówki (READY MEALS + FREEZER additions)
```
pierogi, naleśnik, nalesnik, pizza, krokiet, pyzy, knedle, 
sałatka gotow, salatka gotow, danie gotow, kanapk, wrap,
mrożonk, mrozonk, parmezan, cheddar, camembert (already has),
serek wiejsk, serek homogeniz, serek topion, serek kanapkow, 
kremówk, panna cotta, tiramisu, nuggets, frytki
```

### Puszki, Sosy, Przetwory (PANTRY STAPLES additions)
```
bulion, kostka rosołow, kostka rosolow, zupa instant, zupka, 
baton, batonik, wafle, żelki, zelki, lizak, guma do żucia, guma do zucia,
popcorn, prażynk, prazynk, paluszki (already has some),
sos sojow, pesto, tahini, sos teriyaki, tabasco, wasabi,
musztarda (already has musztard), kisiel (powder),
galaretka, budyń (the dry mix — but „budyn" is in Pieczenie!),
lane kluski, makaron instant
```

### Chemia / Higiena (HOUSEHOLD + PET additions)
```
karma, żwirek, zwirek, przysmak dla,
tabletki do zmywark, płyn do płukan, plyn do plukan, 
kapsułki do prani, kapsulki do prani, odplamiacz,
spray do szyb, płyn do podłóg, plyn do podlog, 
kostka do wc, żel do wc, zel do wc, odkamieniacz,
żarówka, zarowka, rękawice gumow, rekawice gumow,
żel do włos, zel do wlos, lakier do włos, pianka do włos,
plaster, opatrunek, bandaż, bandaz,
rajstopy, skarpet
```

### Napoje (additions)
```
smoothie, koktajl, woda smakow, syrop do wody,
herbata mrożon, yerba, mate, kawa rozpuszczal,
napój izotonicz, napoj izotonicz, woda kokosow
```

### Alkohol (additions)  
```
piwo bezalkoholow, piwo 0%, radler, wino musując,
wino bezalkoholow, drink, koktajl alkohol, miód pitny, miod pitny,
nalewka, grappa, calvados, sambuca
```

### Lada Tradycyjna / Mięso (additions)
```
smalec, słonina, slonina, bekon, hamburger, 
baleron, metka, krakowska, żywiecka, zywiecka,
podwawelska, kiszka, kaszanka, flaki, ozorki,
steak, stek, kości rosołow, kosci rosolow
```

### Ryby (additions)
```
morszczuk, anchois, wędzony łosoś, filet rybny, matjas,
śledzik, sledzik, ryba wędzon, ryba wedzon, 
kawior, ikra
```

### Warzywa i Owoce (additions)
```
daktyl, figa, granat, liczi, marakuja, papaja,
szparag, karczoch, trufl, rzep, kalarepa, 
jarzynka, warzywa mieszane, oliwki, oliwka,
kapary, kiszona (already has kapusta kiszon)
```

### Dział Dziecięcy (additions)
```
krem pod pieluszk, oliwka dla dziec, kąpiel dziec, kapiel dziec,
mleko następne, mleko nastepne, woda dla niemowl, herbatka dla dziec,
gryzak, śliniaczek, sliniaczek
```

## Architecture Patterns

### Categorization Engine Flow
```
User types "chleb" 
  → _normalize("chleb") → "chleb"
  → Check user overrides (learned keywords) — none
  → Iterate sections in JSON order:
    → Warzywa: no keyword contains "chleb" and "chleb" not in any keyword
    → Mięso: same
    → ... (all miss)
  → Return None → UNCATEGORIZED
```

**JSON iteration order matters for collisions.** Sections are visited in the order they appear in the JSON file. First match wins. When adding keywords, be aware that Ryby (section 3) is checked before Puszki (section 5) and Pieczenie (section 6).

### Test Script Pattern
```python
# Standalone script that:
# 1. Defines 10 lists of 100 curated items
# 2. Runs each through _normalize + keyword matching (no DB needed)
# 3. Reports per-list and overall categorization rate
# 4. Saves results as JSON
# 5. Lists all uncategorized items for keyword expansion
```

The test doesn't need the full ShoppingService (no DB). Just import `_normalize` and `SECTION_KEYWORDS` directly and simulate the matching logic.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead |
|---------|-------------|-------------|
| Item generation | Random word generator | Curated realistic lists based on Biedronka aisles |
| Categorization test | New matching engine | Reuse exact `_categorize_item` logic from service.py |
| Polish normalization | Custom diacritics code | Existing `_normalize()` function |

## Common Pitfalls

### Pitfall 1: Adding keywords that create new collisions
**What goes wrong:** Adding "pizza" to Nabiał causes "pizza sos" to match Nabiał instead of Puszki
**Prevention:** After adding keywords, run full test suite. Check that new keywords don't substring-match unintended items.

### Pitfall 2: Forgetting diacritics in keywords
**What goes wrong:** Adding "bułka" when the normalized form is "bulka" — but the engine normalizes keywords at load time, so this actually works. The keywords.json stores original Polish forms and they get normalized.
**Note:** This is NOT a pitfall — the engine handles it correctly.

### Pitfall 3: Duplicate normalized keywords
**What goes wrong:** Adding both "bułka" and "bulka" — both normalize to "bulka". Harmless but wasteful.
**Prevention:** Prefer the Polish-diacritics form in keywords.json for readability.

### Pitfall 4: JSON order = priority order
**What goes wrong:** An item matching keywords in two sections always goes to whichever section appears first in JSON.
**Prevention:** Put more specific/longer keywords before generic short ones within each section. For cross-section ambiguity, accept the JSON-order priority.

### Pitfall 5: Trailing space keywords break on end-of-string
**What goes wrong:** "por " matches "por suszony" but NOT "por" alone (user typed just "por")
**Current instances:** "por ", "bob ", "sum ", "ser " — all break when typed alone
**Accept or fix:** These are intentional to avoid false positives. "por" alone would match "porost", "porcelan", etc. Accept this tradeoff.

## Validation Architecture

### Test Approach
| Property | Value |
|----------|-------|
| Framework | Standalone Python script (no pytest needed) |
| Config file | None — self-contained |
| Quick run command | `python scripts/test_shopping_categorization.py` |
| Output | JSON files with per-list results + summary |

### Success Criteria
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Overall categorization rate | ≥ 95% | categorized_items / total_items × 100 |
| Per-list min rate | ≥ 90% | No single list below 90% |
| No wrong-section items | 0 critical | Manual spot-check of results |

## Metadata

**Confidence breakdown:**
- Coverage gaps: HIGH — tested against actual engine, verified failures
- Missing item lists: HIGH — based on Biedronka product knowledge + verified failures  
- Keyword collision bugs: HIGH — reproduced with actual engine code
- Fix recommendations: MEDIUM — some fixes may have edge cases

**Research date:** 2026-03-27
**Valid until:** Indefinite (Polish grocery vocabulary doesn't change fast)

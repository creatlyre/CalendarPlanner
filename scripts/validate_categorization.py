"""
Expense categorization coverage validator.

Generates 10 lists of 100 realistic expense names (PL+EN mix),
runs them through the exact same matching logic as expense_service.py,
and reports hit rate per list, per category, and aggregate.

Results are saved to scripts/categorization_results.json.
"""

from __future__ import annotations

import json
import random
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

# ── Replicate exact matching logic from expense_service.py ──────────────

KEYWORDS_PATH = Path(__file__).resolve().parent.parent / "app" / "budget" / "category_keywords.json"


def _normalize(text: str) -> str:
    text = text.lower().replace("\u0142", "l")  # ł→l
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _load_keywords() -> dict[str, list[str]]:
    with open(KEYWORDS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return {
        k: [_normalize(kw) for kw in v]
        for k, v in data.items()
        if not k.startswith("_")
    }


CATEGORY_KEYWORDS = _load_keywords()


def detect_category(name: str) -> str | None:
    """Replicate _detect_category logic — returns category name or None."""
    norm = _normalize(name)
    words = norm.split()
    for cat_name, keywords in CATEGORY_KEYWORDS.items():
        for norm_kw in keywords:
            for w in words:
                if norm_kw in w or (len(w) >= 3 and w in norm_kw):
                    return cat_name
    return None


# ── Test data pools per category ────────────────────────────────────────
# Each pool contains realistic expense names that should match the target
# category via the substring matching algorithm. Names are chosen to avoid
# triggering false positives from earlier categories (first-match-wins).

CATEGORY_POOLS: dict[str, list[str]] = {
    "Groceries": [
        "Biedronka", "Lidl", "zakupy spożywcze", "mleko i chleb",
        "jajka", "masło", "serek wiejski", "kurczak", "mięso mielone", "owoce",
        "warzywa sezonowe", "herbata zielona", "makaron penne", "mąka pszenna",
        "cukier", "kawa ziarnista", "herbata", "jogurt naturalny",
        "sok pomarańczowy", "Auchan", "Kaufland", "Żabka", "Dino",
        "piekarnia", "masarnia", "delikatesy", "warzywniak",
        "grocery", "chicken breast", "salmon fillet",
        "cheese", "butter", "eggs", "milk",
        "obiad", "śniadanie", "kolacja", "napoje",
        "chipsy", "czekolada", "lody", "mróżonki", "konserwa",
        "miód", "Netto", "Stokrotka", "Selgros"
    ],
    "Home": [
        "dywan", "lampa biurowa", "farba", "wieszaki",
        "organizery", "zmywarka", "uszczelki",
        "Sidolux", "odplamiacz", "odkamieniacz",
        "chemia domowa", "Natulim listki do prania",
        "poduszka nowa", "kołdra", "firanka",
        "lustro łazienkowe", "Dyson odkurzacz", "obrus nowy",
        "pojemnik kuchenny", "tapeta", "krzesło biurowe",
        "półki", "szafa przesuwna", "koszyki",
        "suszarka", "dywanik łazienkowy", "carpet", "curtain"
    ],
    "Utilities": [
        "prąd PGE", "rachunek gaz", "ogrzewanie",
        "rachunek telefoniczny", "internet światłowód",
        "T-Mobile", "rachunki media", "elektryczność",
        "śmieci odpady", "oczyszczalnia",
        "electricity bill", "water bill", "heating bill",
        "internet bill", "rachunek za telefon", "broadband",
        "Tauron", "Enea", "światłowód",
        "kanalizacja", "ścieki", "rachunek prąd", "prad"
    ],
    "Transport": [
        "paliwo Orlen", "benzyna Shell", "tankowanie BP",
        "Bolt", "Uber", "MPK przejazd",
        "PKP Intercity", "FlixBus", "parking",
        "myjnia", "mechanik", "tankowanie LPG",
        "opony", "przegląd techniczny", "komunikacja miejska",
        "e-toll", "mandat", "laweta", "komunikacja",
        "Jakdojade", "Koleo", "leasing",
        "fuel", "myjnia bezdotykowa", "przejazd autobusem",
        "autostrada", "naprawa", "rower", "hulajnoga"
    ],
    "Health": [
        "apteka leki", "wizyta u lekarza", "dentysta",
        "fizjoterapia", "psycholog", "okulary",
        "badanie krwi", "USG brzucha", "recepta",
        "Apap", "witaminy", "suplementy", "siłownia",
        "DOZ apteka", "Gemini apteka", "przychodnia",
        "pharmacy", "wizyta lekarska", "prescription",
        "therapy", "physiotherapy", "dentist",
        "rehabilitacja", "lekarz", "klinika"
    ],
    "Entertainment": [
        "Netflix", "Spotify", "HBO",
        "Disney+", "kino", "Canal+",
        "koncert", "restauracja", "pizzeria",
        "kawiarnia", "Pyszne.pl", "Glovo dostawa",
        "bowling", "escape game", "muzeum",
        "festiwal muzyczny", "basen", "bilard",
        "karaoke", "subskrypcja filmowa", "cinema",
        "restauracja wieczorna", "streaming", "rozrywka"
    ],
    "Children": [
        "pampersy", "zabawki drewniane", "przedszkole",
        "wózek", "Smyk", "Duplo klocki",
        "lalka", "puzzle", "Coccodrillo",
        "grzechotka", "gryzak", "kreda",
        "kiddoworld", "bawialnia",
        "nursery", "diapers", "toys",
        "niania", "chusteczki nawilżane", "pieluchy"
    ],
    "Clothing": [
        "buty jesienne", "kurtka puchowa", "koszulka",
        "spodnie jeansy", "sukienka", "bluza dresowa",
        "bielizna", "Reserved",
        "Sinsay", "Zara", "bluzki",
        "Deichmann", "CCC", "Halfprice",
        "TK Maxx", "Zalando", "Nike",
        "Adidas", "Puma", "sneakersy",
        "jacket", "jeans", "hoodie", "ciuchy"
    ],
    "Personal Care": [
        "szampon", "fryzjer", "Rossmann",
        "dezodorant", "pasta do zębów", "mydło",
        "krem do twarzy", "balsam", "perfumy",
        "Hebe kosmetyki", "manicure", "pedicure",
        "depilacja", "masaż", "spa",
        "skincare", "shampoo", "haircut",
        "deodorant", "toothpaste", "face cream",
        "cosmetics", "nail polish", "kosmetyki"
    ],
    "Education": [
        "kurs angielskiego", "książki", "Udemy kurs",
        "podręcznik", "szkolenie", "korepetycje",
        "e-learning", "lekcje muzyki", "lekcje pływania",
        "konferencja", "Empik książka", "kurs językowy",
        "online course", "textbook", "workshop",
        "English lessons", "certification exam"
    ],
    "Savings & Finance": [
        "ubezpieczenie domu", "ubezpieczenie samochodu",
        "podatek PIT", "ZUS składka", "nadpłata kredytu",
        "notariusz", "wycena nieruchomości",
        "inwestycja", "lokata bankowa", "obligacje skarbowe",
        "prowizja maklerska", "akcje giełdowe",
        "insurance premium", "pension",
        "fundusz emerytalny", "lokata terminowa", "stocks",
        "broker fee", "dividend", "emerytura"
    ],
    "Events": [
        "prezent urodzinowy", "kwiaty bukiet", "tort urodzinowy",
        "chrzciny", "ślub prezent", "zaproszenie",
        "dekoracje świąteczne", "Wigilia prezenty",
        "Wielkanoc", "walentynki", "rocznica",
        "sesja zdjęciowa", "birthday gift",
        "wedding present", "flowers",
        "Christmas gifts", "anniversary", "invitation"
    ],
    "Pets": [
        "karma dla psa", "karma dla kota",
        "weterynarz wizyta", "legowisko",
        "smycz", "kuweta i żwirek", "Purina",
        "akwarium", "terrarium",
        "pet food", "vet visit", "grooming",
        "Royal Canin", "Whiskas"
    ],
    "Garden": [
        "nawóz do trawnika", "sadzonki",
        "kosiarka", "trawnik",
        "saletra", "agrotkanina",
        "grill węgiel", "meble ogrodowe",
        "doniczki", "szklarnia",
        "garden tools", "lawn mower", "fertilizer",
        "greenhouse"
    ],
    "Electronics": [
        "kabel HDMI", "słuchawki bluetooth", "ładowarka USB-C",
        "smartfon Samsung", "tablet iPad",
        "drukarka tusz", "monitor 27 cali",
        "klawiatura mechaniczna", "myszka bezprzewodowa",
        "SSD dysk 1TB", "powerbank",
        "smartphone case", "wireless charger", "laptop stand",
        "headphones", "speaker"
    ],
    "Rent": [
        "czynsz", "najem lokalu", "administracja wspólnota",
        "wspólnota mieszkaniowa", "wynajem lokalu",
        "rent payment", "apartment lease", "lokal użytkowy",
        "najem biurowy", "deposit",
        "mieszkanie", "kaucja"
    ],
    "Loan": [
        "rata kredytu", "spłata pożyczki", "rata hipoteczna",
        "refinansowanie", "windykacja",
        "loan repayment", "installment",
        "debt payment", "financing",
        "credit payment", "pożyczka"
    ],
    "Travel": [
        "hotel Booking", "Ryanair bilety", "walizka nowa",
        "paszport", "rezerwacja wakacje",
        "Airbnb nocleg", "wycieczka",
        "vacation hotel", "flight tickets", "luggage",
        "cruise", "wczasy zagraniczne",
        "kemping", "camping", "wczasy"
    ],
    "Shopping": [
        "Allegro zamówienie", "AliExpress", "Temu paczka",
        "IKEA regał", "Leroy Merlin",
        "Decathlon", "x-kom",
        "InPost paczkomat", "DHL kurier", "Pepco",
        "Shein zamówienie", "morele", "OBI", "Bricomarche"
    ],
}

# Items that should genuinely NOT match any category keyword.
# Carefully chosen to avoid substring collisions with existing keywords.
UNCATEGORIZABLE_POOL = [
    "napiwek", "darowizna",
    "różne wydatki", "grzywna",
    "tandeta", "zguba",
    "Janowi", "Karolinie",
    "zbiórka charytatywna", "wolontariat",
    "varia", "nieokreślone",
    "pomoc sąsiedzka", "honorarium",
    "reklamacja", "udział",
    "znaczki", "narzuta",
    "pokrowiec", "polecenie",
    "korki", "rumianek"
]

# Distribution per 100-item list (must sum to 100)
DISTRIBUTION = {
    "Groceries": 20,
    "Home": 10,
    "Utilities": 8,
    "Transport": 8,
    "Health": 6,
    "Entertainment": 6,
    "Children": 5,
    "Clothing": 5,
    "Personal Care": 4,
    "Education": 3,
    "Savings & Finance": 3,
    "Events": 3,
    "Pets": 2,
    "Garden": 2,
    "Electronics": 2,
    "Rent": 2,
    "Loan": 1,
    "Travel": 1,
    "Shopping": 2,
    "_uncategorizable": 7,
}


def generate_list(rng: random.Random) -> list[dict]:
    """Generate one list of 100 expense items with expected categories."""
    items = []
    for cat, count in DISTRIBUTION.items():
        if cat == "_uncategorizable":
            pool = UNCATEGORIZABLE_POOL
            expected = None
        else:
            pool = CATEGORY_POOLS[cat]
            expected = cat

        chosen = [rng.choice(pool) for _ in range(count)]
        for name in chosen:
            items.append({"name": name, "expected": expected})

    rng.shuffle(items)
    return items


def run_validation():
    rng = random.Random(42)

    all_results = []
    per_list_rates = []
    per_category_stats: dict[str, dict] = {}
    misses = []

    for list_idx in range(10):
        items = generate_list(rng)
        list_hits = 0
        for item in items:
            detected = detect_category(item["name"])
            expected = item["expected"]

            # A hit means: categorized item matched expected, OR uncategorizable stayed None
            if expected is None:
                is_hit = detected is None
            else:
                is_hit = detected == expected

            if is_hit:
                list_hits += 1
            else:
                misses.append({
                    "list": list_idx + 1,
                    "item": item["name"],
                    "expected": expected,
                    "got": detected,
                })

            # Per-category tracking
            cat_key = expected if expected else "_uncategorizable"
            if cat_key not in per_category_stats:
                per_category_stats[cat_key] = {"total": 0, "hit": 0, "miss": 0}
            per_category_stats[cat_key]["total"] += 1
            if is_hit:
                per_category_stats[cat_key]["hit"] += 1
            else:
                per_category_stats[cat_key]["miss"] += 1

            all_results.append({
                "list": list_idx + 1,
                "name": item["name"],
                "expected": expected,
                "detected": detected,
                "hit": is_hit,
            })

        rate = list_hits / len(items)
        per_list_rates.append(round(rate, 4))

    total = len(all_results)
    total_hits = sum(1 for r in all_results if r["hit"])
    aggregate_rate = round(total_hits / total, 4) if total else 0

    results = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_items": total,
        "categorized_correctly": total_hits,
        "aggregate_hit_rate": aggregate_rate,
        "per_list_rates": per_list_rates,
        "per_category_stats": dict(sorted(per_category_stats.items())),
        "misses": misses,
    }

    # Save results
    output_path = Path(__file__).resolve().parent / "categorization_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Print summary
    print(f"\n{'='*60}")
    print(f"  CATEGORIZATION COVERAGE REPORT")
    print(f"{'='*60}")
    print(f"  Total items:     {total}")
    print(f"  Correct:         {total_hits}")
    print(f"  Aggregate rate:  {aggregate_rate:.1%}")
    print(f"{'='*60}")
    print(f"\n  Per-list rates:")
    for i, rate in enumerate(per_list_rates):
        print(f"    List {i+1:2d}: {rate:.1%}")

    print(f"\n  Per-category stats:")
    for cat, stats in sorted(per_category_stats.items()):
        rate = stats["hit"] / stats["total"] if stats["total"] else 0
        status = "✓" if rate >= 0.93 else "✗"
        print(f"    {status} {cat:20s}  {stats['hit']:3d}/{stats['total']:3d}  ({rate:.0%})")

    if misses:
        print(f"\n  Misses ({len(misses)}):")
        for m in misses[:30]:  # Show first 30
            print(f"    List {m['list']:2d}: '{m['item']}' → expected={m['expected']}, got={m['got']}")
        if len(misses) > 30:
            print(f"    ... and {len(misses) - 30} more")

    print(f"\n  Results saved to: {output_path}")
    return results


if __name__ == "__main__":
    run_validation()

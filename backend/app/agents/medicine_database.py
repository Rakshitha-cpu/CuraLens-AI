import csv
import re
from difflib import get_close_matches
from pathlib import Path

from app.knowledge.openfda import search_openfda

# ---------------------------------------------------
# Database Path
# ---------------------------------------------------

DATABASE_PATH = (
    Path(__file__).resolve().parents[2]
    / "database"
    / "medicines.csv"
)

MEDICINES = {}
MEDICINE_KEYS = set()


# ---------------------------------------------------
# Normalize Medicine Name
# ---------------------------------------------------

def normalize_name(name: str) -> str:

    if not name:
        return ""

    name = str(name).lower()

    prefixes = [
        "tablet",
        "tab",
        "tab.",
        "capsule",
        "cap",
        "cap.",
        "inj",
        "inj.",
        "injection",
        "syrup",
        "syr.",
        "cream",
        "ointment",
        "drops",
        "oral",
        "iv",
    ]

    for prefix in prefixes:
        name = name.replace(prefix, "")

    name = re.sub(r"\d+\s*(mg|ml|mcg|gm|g)", "", name)

    name = re.sub(r"[^a-z0-9 ]", " ", name)

    name = " ".join(name.split())

    return name.strip()


# ---------------------------------------------------
# Initialize Database
# ---------------------------------------------------

def initialize_database():

    global MEDICINES, MEDICINE_KEYS

    MEDICINES = {}

    if not DATABASE_PATH.exists():

        print("Medicine database not found.")
        return

    with open(DATABASE_PATH, "r", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        count = 0

        for row in reader:

            if not row:
                continue

            name = normalize_name(row.get("name"))

            if name:
                MEDICINES[name] = row
                count += 1

            generic = normalize_name(row.get("generic_name"))

            if generic:
                MEDICINES[generic] = row

            brand = normalize_name(row.get("brand_name"))

            if brand:
                MEDICINES[brand] = row

    MEDICINE_KEYS = set(MEDICINES.keys())

    print(f"Loaded {count} medicines.")


# ---------------------------------------------------
# Verify Medicine
# ---------------------------------------------------

def verify_medicine(name: str):

    if not name:

        return {
            "verified": False,
            "name": "UNKNOWN",
            "generic_name": "UNKNOWN",
            "brand_name": "UNKNOWN",
            "category": "UNKNOWN",
            "purpose": "UNKNOWN",
            "how_to_take": "UNKNOWN",
            "food_instruction": "UNKNOWN",
            "common_side_effects": "UNKNOWN",
            "warnings": "UNKNOWN",
            "storage": "UNKNOWN",
            "prescription_required": "UNKNOWN",
        }

    medicine = normalize_name(name)

    # ----------------------------
    # Exact Match
    # ----------------------------

    if medicine in MEDICINES:

        row = MEDICINES[medicine].copy()

        row["verified"] = True

        return row

    # ----------------------------
    # Fuzzy Match
    # ----------------------------

    matches = get_close_matches(
        medicine,
        list(MEDICINES.keys()),
        n=1,
        cutoff=0.80,
    )

    if matches:

        row = MEDICINES[matches[0]].copy()

        row["verified"] = True

        return row

    # ----------------------------
    # Substring / Contains Match
    # ----------------------------
    # Handwritten prescriptions often get OCR'd with extra description
    # merged into the name (e.g. "Hexigel gum paint massage" instead of
    # just "Hexigel"). Fuzzy ratio matching misses these because the
    # strings differ too much in length.
    #
    # With 200K+ entries, scanning every key with a regex (the original
    # approach) took ~6 seconds per lookup - too slow to use per medicine.
    # Instead, generate word n-grams from the query and do O(1) set
    # lookups against MEDICINE_KEYS, which stays fast regardless of how
    # large the database grows.

    words = medicine.split()

    for length in range(min(4, len(words)), 0, -1):
        for start in range(0, len(words) - length + 1):
            candidate = " ".join(words[start:start + length])
            if len(candidate) >= 4 and candidate in MEDICINE_KEYS:
                row = MEDICINES[candidate].copy()
                row["verified"] = True
                return row

    # ----------------------------
    # openFDA Fallback
    # ----------------------------
    # Local CSV is small by design (certainty over coverage). For names
    # it doesn't recognize, check openFDA before giving up - this mainly
    # helps with US-marketed brand/generic names (e.g. Augmentin).
    # Indian-only brand names (e.g. Enzoflam, Pan-D) generally won't be
    # in openFDA either - add those to database/medicines.csv directly.

    fda_result = search_openfda(name)

    if fda_result:
        return fda_result

    # ----------------------------
    # Not Found
    # ----------------------------

    return {
        "verified": False,
        "name": name,
        "generic_name": "UNKNOWN",
        "brand_name": "UNKNOWN",
        "category": "UNKNOWN",
        "purpose": "UNKNOWN",
        "how_to_take": "UNKNOWN",
        "food_instruction": "UNKNOWN",
        "common_side_effects": "UNKNOWN",
        "warnings": "UNKNOWN",
        "storage": "UNKNOWN",
        "prescription_required": "UNKNOWN",
    }


# ---------------------------------------------------
# Search Medicines
# ---------------------------------------------------

def search_medicines(query: str):

    query = normalize_name(query)

    results = []

    for key, value in MEDICINES.items():

        if query in key:
            results.append(value)

    return results


# ---------------------------------------------------
# Auto Load Database
# ---------------------------------------------------

initialize_database()
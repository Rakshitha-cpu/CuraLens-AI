import json
from pathlib import Path
from datetime import datetime, timedelta

# ---------------------------------------
# Cache Folder
# ---------------------------------------

CACHE_DIR = Path(__file__).resolve().parents[2] / "database" / "cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)

CACHE_EXPIRY_DAYS = 30


# ---------------------------------------
# Cache File Path
# ---------------------------------------

def cache_path(medicine_name: str):

    filename = medicine_name.lower().replace("/", "_").replace(" ", "_")

    return CACHE_DIR / f"{filename}.json"


# ---------------------------------------
# Save Cache
# ---------------------------------------

def save_cache(medicine_name: str, data: dict):

    file = cache_path(medicine_name)

    payload = {
        "updated": datetime.now().isoformat(),
        "data": data
    }

    with open(file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4, ensure_ascii=False)


# ---------------------------------------
# Load Cache
# ---------------------------------------

def load_cache(medicine_name: str):

    file = cache_path(medicine_name)

    if not file.exists():
        return None

    try:

        with open(file, "r", encoding="utf-8") as f:
            payload = json.load(f)

        updated = datetime.fromisoformat(payload["updated"])

        if datetime.now() - updated > timedelta(days=CACHE_EXPIRY_DAYS):

            return None

        return payload["data"]

    except Exception:

        return None


# ---------------------------------------
# Clear Cache
# ---------------------------------------

def clear_cache():

    if not CACHE_DIR.exists():
        return

    for file in CACHE_DIR.glob("*.json"):
        file.unlink()

    print("Medicine cache cleared.")
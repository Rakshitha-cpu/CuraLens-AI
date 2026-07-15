import json
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from app.agents.medicine_database import verify_medicine

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        f"""
GEMINI_API_KEY not found.

Get a free key from Google AI Studio: https://aistudio.google.com/apikey

Expected location:
{env_path}

Add this line to your .env file:

GEMINI_API_KEY=AIzaSy...
"""
    )

# ---------------------------------------------------
# Gemini Client
# ---------------------------------------------------

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"

# ---------------------------------------------------
# Safe AI Call (retry + backoff for transient errors)
# ---------------------------------------------------

def call_ai(prompt: str, max_retries: int = 3):
    """
    Calls Gemini with retry + exponential backoff for transient
    failures (rate limits, server errors). Without this, one
    rate-limited call in a batch of several medicines just silently
    returns nothing, while others in the same batch succeed.
    """

    last_error = None

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    system_instruction="You are an experienced clinical pharmacist. Always return ONLY valid JSON.",
                ),
            )

            text = response.text

            if not text:
                raise ValueError("Empty response from Gemini")

            text = text.replace("```json", "").replace("```", "").strip()

            return json.loads(text)

        except (ClientError, ServerError) as e:
            # ClientError covers 4xx including rate limits (429);
            # ServerError covers 5xx transient failures. Both are
            # worth retrying.
            last_error = e
            wait = 2 ** attempt  # 1s, 2s, 4s
            print(f"Gemini transient error (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait}s...")
            time.sleep(wait)

        except json.JSONDecodeError as e:

            # Malformed JSON from the model - retrying rarely helps,
            # fail fast instead of wasting retries.
            print("Invalid JSON from Gemini:", e)
            return None

        except Exception as e:

            print("Gemini Error:", e)
            return None

    print(f"Gemini: giving up after {max_retries} attempts. Last error: {last_error}")
    return None


# ---------------------------------------------------
# Explain Single Medicine
# ---------------------------------------------------

def explain_medicine(medicine_name: str):

    # -----------------------------
    # 1. Search Local CSV First
    # -----------------------------
    database = verify_medicine(medicine_name)

    # verify_medicine() ALWAYS returns a dict (never None), even for
    # "not found" - it just sets fields to "UNKNOWN". Only trust the
    # local database's education content when it's actually been
    # curated with real values - otherwise fall through to Gemini.

    has_real_education = (
        database
        and database.get("purpose")
        and database.get("purpose") not in ("UNKNOWN", "")
    )

    if has_real_education:

        return {
            "name": database.get("name", medicine_name),
            "purpose": database.get("purpose", "UNKNOWN"),
            "how_to_take": database.get("how_to_take", "UNKNOWN"),
            "food_instruction": database.get("food_instruction", "UNKNOWN"),
            "common_side_effects": database.get("common_side_effects", "").split(","),
            "warnings": database.get("warnings", "").split(","),
            "storage": database.get("storage", "UNKNOWN"),
            "when_to_call_doctor": "Consult your doctor if severe side effects occur."
        }

    # -----------------------------
    # 2. AI Fallback (Gemini)
    # -----------------------------
    # If we know the verified generic composition (from the bulk
    # database) but not the clinical narrative, tell Gemini what the
    # composition actually is - keeps the explanation grounded in the
    # real ingredient instead of guessing from an Indian brand name.

    known_generic = None
    if database and database.get("verified") and database.get("generic_name") not in (None, "", "UNKNOWN"):
        known_generic = database["generic_name"]

    composition_line = (
        f"Known composition (verified): {known_generic}\n"
        if known_generic else ""
    )

    prompt = f"""
Explain this medicine.

Medicine:
{medicine_name}
{composition_line}
Return ONLY JSON.

{{
"name":"",
"purpose":"",
"how_to_take":"",
"food_instruction":"",
"common_side_effects":[],
"warnings":[],
"storage":"",
"when_to_call_doctor":""
}}
"""

    result = call_ai(prompt)

    if result:
        return result

    return {
        "name": medicine_name,
        "purpose": "UNKNOWN",
        "how_to_take": "UNKNOWN",
        "food_instruction": "UNKNOWN",
        "common_side_effects": [],
        "warnings": [],
        "storage": "UNKNOWN",
        "when_to_call_doctor": "UNKNOWN"
    }


# ---------------------------------------------------
# Batch Medicines (parallel, not sequential)
# ---------------------------------------------------

def explain_medicines_batch(medicine_names):
    """
    Explains all medicines in parallel rather than one at a time.
    max_workers is capped so a prescription with many medicines
    doesn't fire a burst large enough to trigger rate limiting itself.
    """

    if not medicine_names:
        return []

    max_workers = min(4, len(medicine_names))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(explain_medicine, medicine_names))

    return results

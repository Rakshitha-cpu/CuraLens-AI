import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(dotenv_path=env_path, override=True)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        f"""
GEMINI_API_KEY not found.

Get a free key from Google AI Studio: https://aistudio.google.com/apikey

Expected .env location:

{env_path}

Add this line:

GEMINI_API_KEY=AIzaSy...
"""
    )

# ---------------------------------------------------
# Gemini Client
# ---------------------------------------------------

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"

# ---------------------------------------------------
# OCR Prompt
# ---------------------------------------------------

SYSTEM_PROMPT = """
You are an expert pharmacist and handwritten prescription OCR assistant.

Read the uploaded prescription carefully.

Extract:

- patient_name
- doctor_name
- hospital

For EVERY medicine extract:

- name
- confidence
- dosage
- frequency
- duration
- instructions

Interpret these abbreviations:

OD = once daily
BD = twice daily
TDS = three times daily
QID = four times daily
HS = bedtime
SOS = when required

Interpret dosage patterns:

1-0-1 = twice daily
1-1-1 = three times daily
1-0-0 = once daily
0-1-0 = once daily
0-0-1 = once daily

Interpret duration:

5D = 5 days
7D = 7 days
10D = 10 days
15D = 15 days

If handwriting is partially readable:

- Identify medicines only if visually supported.
- Never invent medicine names.
- If uncertain, return the visible text and set confidence to "low".

Return ONLY valid JSON, no markdown fences, no commentary.

{
  "patient_name":"",
  "doctor_name":"",
  "hospital":"",
  "medicines":[
    {
      "name":"",
      "confidence":"high",
      "dosage":"",
      "frequency":"",
      "duration":"",
      "instructions":""
    }
  ]
}
"""

# ---------------------------------------------------
# MIME type lookup (Gemini needs this per image part)
# ---------------------------------------------------

MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


def _guess_mime_type(image_path: str) -> str:
    ext = Path(image_path).suffix.lower()
    return MIME_TYPES.get(ext, "image/jpeg")


# ---------------------------------------------------
# OCR Function
# ---------------------------------------------------

def extract_prescription(image_path: str, max_retries: int = 3):

    last_error = None

    try:
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()
    except OSError as e:
        print("\nCould not read uploaded file:", e)
        return {
            "patient_name": "File Read Error",
            "doctor_name": "UNKNOWN",
            "hospital": "UNKNOWN",
            "medicines": []
        }

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=_guess_mime_type(image_path),
                    ),
                    SYSTEM_PROMPT,
                ],
                config=types.GenerateContentConfig(
                    temperature=0,
                ),
            )

            text = response.text

            if not text:
                raise ValueError("Gemini returned an empty response.")

            text = (
                text.replace("```json", "")
                    .replace("```", "")
                    .strip()
            )

            print("\n========== OCR OUTPUT ==========")
            print(text)
            print("================================\n")

            return json.loads(text)

        except json.JSONDecodeError as e:

            # Malformed JSON from the model - retrying rarely helps,
            # the model will likely produce the same output again.
            print("\nInvalid JSON returned from Gemini.")
            print(e)

            return {
                "patient_name": "OCR Failed",
                "doctor_name": "UNKNOWN",
                "hospital": "UNKNOWN",
                "medicines": []
            }

        except Exception as e:

            # Covers transient network issues (DNS hiccups, dropped
            # connections, timeouts) as well as Gemini rate limits/
            # server errors - all worth retrying. A single flaky
            # network moment (packet loss, brief DNS failure) should
            # not fail the entire prescription analysis.
            last_error = e
            wait = 2 ** attempt  # 1s, 2s, 4s

            print(f"\nGemini error on OCR (attempt {attempt + 1}/{max_retries}): {e}")

            if attempt < max_retries - 1:
                print(f"Retrying in {wait}s...")
                time.sleep(wait)

    print("\n========== Gemini Error (all retries exhausted) ==========")
    print(last_error)
    print("============================================================")

    return {
        "patient_name": "API Error",
        "doctor_name": "UNKNOWN",
        "hospital": "UNKNOWN",
        "medicines": []
    }

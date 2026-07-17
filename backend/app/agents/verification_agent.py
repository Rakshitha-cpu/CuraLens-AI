from concurrent.futures import ThreadPoolExecutor

from app.agents.medicine_database import verify_medicine


def is_missing(value):
    if value is None:
        return True

    value = str(value).strip().upper()

    return value in ["", "UNKNOWN", "N/A", "NONE"]


def verify_prescription(data):

    medicines = data.get("medicines", [])

    if not medicines:
        return []

    # Look up all medicines in parallel instead of one at a time.
    # Each lookup that isn't found locally falls back to an openFDA
    # API call (up to ~20s) - for a prescription with several
    # unrecognized medicines (common with Ayurvedic/regional brand
    # names), doing this sequentially could add well over a minute
    # to the total analysis time.
    names = [medicine.get("name", "") for medicine in medicines]
    max_workers = min(4, len(names))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        database_results = list(executor.map(verify_medicine, names))

    verified = []

    for medicine, database in zip(medicines, database_results):

        issues = []

        name = medicine.get("name", "")

        # -----------------------------
        # Name
        # -----------------------------
        if is_missing(name):
            issues.append("Medicine name missing")

        # -----------------------------
        # Database Verification
        # -----------------------------
        # verify_medicine() always returns a dict, even for "not found"
        # (it just sets fields to UNKNOWN) - so `if database:` alone is
        # always True. Check the actual verified flag instead, or this
        # silently marks every medicine as database-verified and the
        # "Medicine not found in database" issue never gets recorded.
        if database and database.get("verified"):

            medicine["database_verified"] = True

            # Use database values if OCR missed them
            if is_missing(medicine.get("dosage")):
                medicine["dosage"] = database.get("dosage", "UNKNOWN")

            if is_missing(medicine.get("instructions")):
                medicine["instructions"] = database.get(
                    "how_to_take",
                    "UNKNOWN"
                )

            medicine["purpose"] = database.get("purpose", "UNKNOWN")
            medicine["generic_name"] = database.get("generic_name", "")
            medicine["brand_name"] = database.get("brand_name", "")
            medicine["category"] = database.get("category", "")
            medicine["prescription_required"] = database.get("prescription_required", "UNKNOWN")

        else:

            medicine["database_verified"] = False
            medicine["generic_name"] = "UNKNOWN"
            medicine["brand_name"] = "UNKNOWN"
            medicine["category"] = "UNKNOWN"
            medicine["purpose"] = "UNKNOWN"
            medicine["prescription_required"] = "UNKNOWN"
            issues.append("Medicine not found in database")

        # -----------------------------
        # Dosage
        # -----------------------------
        if is_missing(medicine.get("dosage")):
            issues.append("Dosage missing")

        # -----------------------------
        # Frequency
        # -----------------------------
        if is_missing(medicine.get("frequency")):
            issues.append("Frequency missing")

        # -----------------------------
        # Duration
        # -----------------------------
        if is_missing(medicine.get("duration")):
            issues.append("Duration missing")

        # -----------------------------
        # Instructions
        # -----------------------------
        if is_missing(medicine.get("instructions")):
            issues.append("Instructions missing")

        # -----------------------------
        # Verification Status
        # -----------------------------
        medicine["verified"] = (
            medicine["database_verified"]
            and not is_missing(medicine.get("name"))
            and not is_missing(medicine.get("dosage"))
        )

        medicine["issues"] = issues

        verified.append(medicine)

    return verified
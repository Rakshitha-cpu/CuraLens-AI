from app.agents.medicine_database import verify_medicine


def is_missing(value):
    if value is None:
        return True

    value = str(value).strip().upper()

    return value in ["", "UNKNOWN", "N/A", "NONE"]


def verify_prescription(data):

    medicines = data.get("medicines", [])

    verified = []

    for medicine in medicines:

        issues = []

        name = medicine.get("name", "")

        database = verify_medicine(name)

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

        else:

            medicine["database_verified"] = False
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
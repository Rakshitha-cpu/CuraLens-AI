def is_missing(value):
    if value is None:
        return True

    value = str(value).strip().upper()

    return value in ["", "UNKNOWN", "N/A", "NONE"]


def calculate_score(prescription):

    score = 100
    reasons = []

    medicines = prescription.get("medicines", [])
    safety = prescription.get("safety", {})

    if not medicines:
        return {
            "score": 0,
            "risk_level": "HIGH RISK",
            "reasons": ["No medicines detected."]
        }

    # ----------------------------------------
    # Medicine Evaluation
    # ----------------------------------------

    for medicine in medicines:

        name = medicine.get("name", "Unknown Medicine")

        # Missing name
        if is_missing(name):
            score -= 20
            reasons.append("Medicine name could not be identified.")
            continue

        # Database verification
        if medicine.get("database_verified", False):
            score += 1
        else:
            score -= 5
            reasons.append(f"{name}: medicine not found in database.")

        # OCR verification
        if not medicine.get("verified", False):
            score -= 3
            reasons.append(f"{name}: OCR verification failed.")

        # Dosage
        if is_missing(medicine.get("dosage")):
            score -= 5
            reasons.append(f"{name}: dosage not specified.")

        # Frequency
        if is_missing(medicine.get("frequency")):
            score -= 2
            reasons.append(f"{name}: frequency not specified.")

        # Duration
        if is_missing(medicine.get("duration")):
            score -= 2
            reasons.append(f"{name}: duration not specified.")

        # Instructions
        if is_missing(medicine.get("instructions")):
            score -= 2
            reasons.append(f"{name}: instructions not specified.")

    # ----------------------------------------
    # Safety Evaluation
    # ----------------------------------------

    overall = safety.get("overall_risk", "SAFE")

    if overall == "HIGH":
        score -= 20
        reasons.append("High-risk drug interaction detected.")

    elif overall == "MODERATE":
        score -= 10
        reasons.append("Moderate-risk interaction detected.")

    elif overall == "LOW":
        score -= 2

    # Individual alerts
    alerts = safety.get("alerts", [])

    score -= len(alerts)

    # ----------------------------------------
    # Final Score
    # ----------------------------------------

    score = max(0, min(100, score))

    if score >= 90:
        level = "LOW RISK"

    elif score >= 70:
        level = "MEDIUM RISK"

    else:
        level = "HIGH RISK"

    return {
        "score": score,
        "risk_level": level,
        "reasons": reasons
    }
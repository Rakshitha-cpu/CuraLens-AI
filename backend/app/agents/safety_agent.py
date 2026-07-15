from app.services.interaction_service import InteractionService


def analyze_safety(medicines):

    alerts = []
    seen = set()

    # -----------------------------------
    # Check Individual Medicines
    # -----------------------------------

    for medicine in medicines:

        name = medicine.get("name", "UNKNOWN")

        key = name.lower().strip()

        # Duplicate medicine
        if key in seen:
            alerts.append({
                "type": "Duplicate Medicine",
                "severity": "MODERATE",
                "medicine": name,
                "message": f"{name} appears more than once."
            })
        else:
            seen.add(key)

        # Database verification
        if not medicine.get("database_verified", False):
            alerts.append({
                "type": "Unknown Medicine",
                "severity": "LOW",
                "medicine": name,
                "message": f"{name} is not available in the medicine database."
            })

        # Missing dosage
        if medicine.get("dosage") in ["", "UNKNOWN", None]:
            alerts.append({
                "type": "Missing Dosage",
                "severity": "MODERATE",
                "medicine": name,
                "message": "Dosage not specified."
            })

        # Missing frequency
        if medicine.get("frequency") in ["", "UNKNOWN", None]:
            alerts.append({
                "type": "Missing Frequency",
                "severity": "LOW",
                "medicine": name,
                "message": "Frequency not specified."
            })

        # Missing duration
        if medicine.get("duration") in ["", "UNKNOWN", None]:
            alerts.append({
                "type": "Missing Duration",
                "severity": "LOW",
                "medicine": name,
                "message": "Duration not specified."
            })

        # Missing instructions
        if medicine.get("instructions") in ["", "UNKNOWN", None]:
            alerts.append({
                "type": "Missing Instructions",
                "severity": "LOW",
                "medicine": name,
                "message": "Instructions not specified."
            })

    # -----------------------------------
    # Drug Interaction Check
    # -----------------------------------

    for i in range(len(medicines)):

        for j in range(i + 1, len(medicines)):

            interaction = InteractionService.check_interaction(
                medicines[i]["name"],
                medicines[j]["name"]
            )

            if interaction:
                alerts.append({
                    "type": interaction.get("type", "Drug Interaction"),
                    "severity": interaction.get("severity", "MODERATE"),
                    "medicine": f"{medicines[i]['name']} + {medicines[j]['name']}",
                    "message": interaction.get("message", "Potential interaction detected."),
                })

    # -----------------------------------
    # Overall Risk
    # -----------------------------------

    severities = [a["severity"] for a in alerts]

    if "HIGH" in severities:
        overall = "HIGH"

    elif "MODERATE" in severities:
        overall = "MODERATE"

    elif "LOW" in severities:
        overall = "LOW"

    else:
        overall = "SAFE"

    # -----------------------------------
    # Summary
    # -----------------------------------

    if not alerts:
        summary = "No safety issues detected."
    else:
        summary = f"{len(alerts)} safety issue(s) detected."

    return {
        "overall_risk": overall,
        "interaction_count": len(alerts),
        "alerts": alerts,
        "summary": summary
    }
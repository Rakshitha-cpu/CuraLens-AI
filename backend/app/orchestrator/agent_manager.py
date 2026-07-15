from app.agents.medication_agent import explain_medicines_batch
from app.agents.verification_agent import verify_prescription
from app.agents.vision_agent import extract_prescription
from app.agents.safety_agent import analyze_safety
from app.agents.score_agent import calculate_score
from app.agents.medicine_database import verify_medicine


class AgentManager:

    @staticmethod
    def process(image_path: str):

        # ---------------------------------------
        # Step 1 : OCR
        # ---------------------------------------

        prescription = extract_prescription(image_path)

        if not prescription:
            return {
                "patient_name": "UNKNOWN",
                "doctor_name": "UNKNOWN",
                "hospital": "UNKNOWN",
                "medicines": [],
                "safety": {
                    "overall_risk": "UNKNOWN",
                    "interaction_count": 0,
                    "alerts": []
                },
                "score": {
                    "score": 0,
                    "risk_level": "HIGH RISK",
                    "reasons": ["OCR failed."]
                }
            }

        # ---------------------------------------
        # Step 2 : Verification
        # ---------------------------------------

        verified_medicines = verify_prescription(prescription)

        # ---------------------------------------
        # Step 3 : AI Education
        # ---------------------------------------

        medicine_names = []

        for med in verified_medicines:

            if med.get("name"):
                medicine_names.append(med["name"])

        explanations = explain_medicines_batch(medicine_names)

        # explain_medicines_batch preserves order (ThreadPoolExecutor.map
        # is order-preserving), so match by position instead of by name.
        # Matching by name was unreliable because explain_medicine()
        # sometimes returns the DATABASE's canonical name (e.g. "Pan-D")
        # rather than the OCR-extracted name (e.g. "Pan D") - those two
        # strings don't match as dict keys even though they're the same
        # medicine, so real results were being silently dropped.
        explanations_by_index = dict(zip(medicine_names, explanations))

        medicines = []

        for medicine in verified_medicines:

            name = medicine.get("name", "")

            # -------------------------------
            # Database Verification
            # -------------------------------

            database = verify_medicine(name)

            if database is None:

                medicine["database_verified"] = False
                medicine["generic_name"] = "UNKNOWN"
                medicine["brand_name"] = "UNKNOWN"
                medicine["category"] = "UNKNOWN"
                medicine["purpose"] = "UNKNOWN"
                medicine["prescription_required"] = "UNKNOWN"

            else:

                medicine["database_verified"] = database.get("verified", False)
                medicine["generic_name"] = database.get("generic_name", "UNKNOWN")
                medicine["brand_name"] = database.get("brand_name", "UNKNOWN")
                medicine["category"] = database.get("category", "UNKNOWN")
                medicine["purpose"] = database.get("purpose", "UNKNOWN")
                medicine["prescription_required"] = database.get(
                    "prescription_required",
                    "UNKNOWN"
                )

            # -------------------------------
            # AI Education
            # -------------------------------

            medicine["education"] = explanations_by_index.get(name, {})

            medicines.append(medicine)

        prescription["medicines"] = medicines

        # ---------------------------------------
        # Step 4 : Safety
        # ---------------------------------------

        prescription["safety"] = analyze_safety(medicines)

        # ---------------------------------------
        # Step 5 : Score
        # ---------------------------------------

        prescription["score"] = calculate_score(prescription)

        return prescription
import pandas as pd
from pathlib import Path

# app/services/medicine_service.py -> parents[2] is the "backend" folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Dataset path
MEDICINE_FILE = BASE_DIR / "datasets" / "medicines" / "common_medicines.csv"

# Load dataset (fail soft - a missing file here should not crash the server)
try:
    medicine_df = pd.read_csv(MEDICINE_FILE)
    medicine_df = medicine_df.fillna("UNKNOWN")
except FileNotFoundError:
    print(f"[medicine_service] WARNING: {MEDICINE_FILE} not found. "
          f"MedicineService.get_medicine will report everything as not found.")
    medicine_df = pd.DataFrame(columns=["medicine"])


class MedicineService:

    @staticmethod
    def get_medicine(name: str):

        result = medicine_df[
            medicine_df["medicine"].str.lower() == name.lower()
        ]

        if result.empty:
            return {
                "found": False,
                "message": "Medicine not found in database."
            }

        medicine = result.iloc[0].to_dict()

        medicine["found"] = True

        return medicine
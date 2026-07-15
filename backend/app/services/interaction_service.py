import pandas as pd
from pathlib import Path

# app/services/interaction_service.py -> parents[2] is the "backend" folder
BASE_DIR = Path(__file__).resolve().parents[2]

INTERACTION_FILE = (
    BASE_DIR /
    "datasets" /
    "interactions" /
    "interactions.csv"
)

try:
    interaction_df = pd.read_csv(INTERACTION_FILE)
except FileNotFoundError:
    # Never let a missing/misplaced data file crash the whole backend at
    # import time - this import chain runs on every server start
    # (main.py -> ai.py -> agent_manager -> safety_agent -> here).
    # Fail soft: interaction checks just return "no match" until the
    # file is restored, instead of the entire API refusing to boot.
    print(f"[interaction_service] WARNING: {INTERACTION_FILE} not found. "
          f"Drug interaction checks are disabled until this file exists.")
    interaction_df = pd.DataFrame(columns=["medicine_a", "medicine_b", "type", "severity", "message"])


class InteractionService:

    @staticmethod
    def check_interaction(medicine1, medicine2):

        result = interaction_df[
            (
                (interaction_df["medicine_a"].str.lower() == medicine1.lower()) &
                (interaction_df["medicine_b"].str.lower() == medicine2.lower())
            ) |
            (
                (interaction_df["medicine_a"].str.lower() == medicine2.lower()) &
                (interaction_df["medicine_b"].str.lower() == medicine1.lower())
            )
        ]

        if result.empty:
            return None

        return result.iloc[0].to_dict()
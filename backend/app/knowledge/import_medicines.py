import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "medicines.db"

CSV_PATH = Path(__file__).resolve().parents[1] / "database" / "medicines.csv"


def import_csv():

    if not CSV_PATH.exists():
        print("CSV file not found:", CSV_PATH)
        return

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_csv(CSV_PATH)

    print("Rows Found:", len(df))

    for _, row in df.iterrows():

        conn.execute(
            """
            INSERT OR REPLACE INTO medicines(

                name,
                generic_name,
                brand_name,
                purpose,
                how_to_take,
                food_instruction,
                common_side_effects,
                warnings,
                contraindications,
                pregnancy,
                breastfeeding,
                dosage,
                frequency,
                duration,
                storage,
                when_to_call_doctor,
                drug_class,
                active_ingredient,
                source,
                verified,
                confidence

            )

            VALUES(

                ?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?

            )
            """,

            (

                row.get("name",""),
                row.get("generic_name",""),
                row.get("brand_name",""),
                row.get("purpose",""),
                row.get("how_to_take",""),
                row.get("food_instruction",""),
                row.get("common_side_effects","[]"),
                row.get("warnings","[]"),
                row.get("contraindications","[]"),
                row.get("pregnancy","UNKNOWN"),
                row.get("breastfeeding","UNKNOWN"),
                row.get("dosage",""),
                row.get("frequency",""),
                row.get("duration",""),
                row.get("storage",""),
                row.get("when_to_call_doctor",""),
                row.get("drug_class",""),
                row.get("active_ingredient",""),
                row.get("source","CSV"),
                1,
                "high"

            )

        )

    conn.commit()

    conn.close()

    print("Medicines Imported Successfully")


if __name__ == "__main__":
    import_csv()
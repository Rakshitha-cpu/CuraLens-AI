import requests

BASE_URL = "https://api.fda.gov/drug/label.json"


def first(data, key):
    """
    Safely extract the first value from an OpenFDA field.
    """

    value = data.get(key)

    if not value:
        return ""

    if isinstance(value, list):
        return value[0]

    return value


def search_openfda(medicine_name: str):

    try:

        url = (
            BASE_URL
            + "?search=openfda.brand_name:"
            + f'"{medicine_name}"'
            + "&limit=1"
        )

        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            return None

        results = response.json().get("results", [])

        if not results:
            return None

        drug = results[0]

        openfda = drug.get("openfda", {})

        return {
            "name": medicine_name,
            "generic_name": first(openfda, "generic_name"),
            "brand_name": first(openfda, "brand_name"),
            "category": "Allopathy",
            "purpose": first(drug, "indications_and_usage"),
            "how_to_take": first(drug, "dosage_and_administration"),
            "food_instruction": "",
            "common_side_effects": first(drug, "adverse_reactions"),
            "warnings": first(drug, "warnings"),
            "storage": first(drug, "storage_and_handling"),
            "prescription_required": "Yes",
            "source": "OpenFDA",
            "verified": True
        }

    except Exception as e:

        print("OpenFDA Error:", e)

        return None


if __name__ == "__main__":

    medicine = input("Medicine: ")

    result = search_openfda(medicine)

    print(result)
import requests
import pandas as pd

URL = "https://api.fda.gov/drug/label.json?limit=100"

response = requests.get(URL)

if response.status_code != 200:
    print("Failed to fetch data")
    exit()

results = response.json()["results"]

medicines = []

for drug in results:

    medicines.append({
        "name": drug.get("openfda", {}).get("brand_name", ["UNKNOWN"])[0],
        "generic_name": drug.get("openfda", {}).get("generic_name", ["UNKNOWN"])[0],
        "manufacturer": drug.get("openfda", {}).get("manufacturer_name", ["UNKNOWN"])[0],
        "purpose": " ".join(drug.get("purpose", ["UNKNOWN"])),
        "warnings": " ".join(drug.get("warnings", ["UNKNOWN"])),
        "route": ",".join(drug.get("openfda", {}).get("route", [])),
        "dosage_form": ",".join(drug.get("openfda", {}).get("dosage_form", [])),
    })

df = pd.DataFrame(medicines)

df.to_csv("data/medicines.csv", index=False)

print("Dataset created successfully.")
print(df.head())
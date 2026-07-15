import requests
import os

url = "https://download.open.fda.gov/drug/label/drug-label-0001-of-0011.json.zip"

os.makedirs("../datasets/openfda", exist_ok=True)

output = "../datasets/openfda/drug-label.zip"

print("Downloading OpenFDA...")

r = requests.get(url, stream=True)

with open(output, "wb") as f:
    for chunk in r.iter_content(8192):
        f.write(chunk)

print("Downloaded:", output)

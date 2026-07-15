import requests
import os

url = "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json"

os.makedirs("../datasets/dailymed", exist_ok=True)

data = requests.get(url).json()

with open("../datasets/dailymed/spls.json","w",encoding="utf8") as f:
    import json
    json.dump(data,f,indent=2)

print("Downloaded DailyMed list")
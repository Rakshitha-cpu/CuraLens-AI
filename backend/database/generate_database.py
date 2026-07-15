import pandas as pd

medicines = [

{
"name":"Paracetamol",
"generic_name":"Paracetamol",
"brand_name":"Crocin",
"category":"Allopathy",
"purpose":"Fever and pain relief",
"how_to_take":"Take as directed by doctor",
"food_instruction":"With or without food",
"common_side_effects":"Nausea,Rash",
"warnings":"Avoid overdose",
"storage":"Room temperature",
"prescription_required":"No"
},

{
"name":"Dolo 650",
"generic_name":"Paracetamol",
"brand_name":"Dolo 650",
"category":"Allopathy",
"purpose":"Fever and pain",
"how_to_take":"Take as prescribed",
"food_instruction":"With or without food",
"common_side_effects":"Nausea",
"warnings":"Liver disease",
"storage":"Room temperature",
"prescription_required":"No"
},

{
"name":"Albendazole",
"generic_name":"Albendazole",
"brand_name":"Zentel",
"category":"Allopathy",
"purpose":"Deworming",
"how_to_take":"Usually single dose",
"food_instruction":"After food",
"common_side_effects":"Headache",
"warnings":"Pregnancy caution",
"storage":"Room temperature",
"prescription_required":"Yes"
},

{
"name":"Raja Pravartani Vati",
"generic_name":"Herbal Formula",
"brand_name":"Baidyanath",
"category":"Ayurveda",
"purpose":"Menstrual disorders",
"how_to_take":"As directed",
"food_instruction":"After meals",
"common_side_effects":"Mild stomach upset",
"warnings":"Avoid during pregnancy",
"storage":"Cool dry place",
"prescription_required":"No"
},

{
"name":"Ashwagandha",
"generic_name":"Withania somnifera",
"brand_name":"Himalaya",
"category":"Ayurveda",
"purpose":"Stress and immunity",
"how_to_take":"1 tablet twice daily",
"food_instruction":"After meals",
"common_side_effects":"Sleepiness",
"warnings":"Pregnancy caution",
"storage":"Cool dry place",
"prescription_required":"No"
},

{
"name":"Amoxicillin",
"generic_name":"Amoxicillin",
"brand_name":"Mox",
"category":"Allopathy",
"purpose":"Bacterial infection",
"how_to_take":"As prescribed",
"food_instruction":"With or without food",
"common_side_effects":"Diarrhea",
"warnings":"Penicillin allergy",
"storage":"Room temperature",
"prescription_required":"Yes"
},

{
"name":"Metformin",
"generic_name":"Metformin",
"brand_name":"Glycomet",
"category":"Allopathy",
"purpose":"Type 2 Diabetes",
"how_to_take":"Twice daily",
"food_instruction":"After food",
"common_side_effects":"Nausea",
"warnings":"Kidney disease",
"storage":"Room temperature",
"prescription_required":"Yes"
},

{
"name":"Telmisartan",
"generic_name":"Telmisartan",
"brand_name":"Telma",
"category":"Allopathy",
"purpose":"Hypertension",
"how_to_take":"Once daily",
"food_instruction":"With or without food",
"common_side_effects":"Dizziness",
"warnings":"Pregnancy",
"storage":"Room temperature",
"prescription_required":"Yes"
}

]

df = pd.DataFrame(medicines)

df.to_csv("medicines.csv",index=False)

print("Database created successfully")
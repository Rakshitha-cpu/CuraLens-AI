from app.services.medicine_service import MedicineService

medicine = MedicineService.get_medicine("ORS")

print(medicine)
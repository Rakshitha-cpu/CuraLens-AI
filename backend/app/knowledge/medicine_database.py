from app.knowledge.cache import get_cached_medicine

def verify_medicine(name: str):
    medicine = get_cached_medicine(name)

    if medicine:
        return medicine

    return None
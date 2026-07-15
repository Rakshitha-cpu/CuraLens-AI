from dataclasses import dataclass


@dataclass
class Medicine:

    name: str

    generic_name: str = ""

    brand_name: str = ""

    category: str = ""

    purpose: str = ""

    how_to_take: str = ""

    food_instruction: str = ""

    common_side_effects: str = ""

    warnings: str = ""

    storage: str = ""

    prescription_required: str = ""

    source: str = ""

    verified: bool = False
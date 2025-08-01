import json
import os
from bowl_scale import BowlScale
from fastapi import HTTPException
from typing import Dict
from scale import Scale


def load_scales(path: str = "./scale_profiles") -> Dict[str, Scale]:
    """
    load_scales Load scales from the given path.

    Args:
        path (str, optional): The path to the scale profiles. Defaults to "./scale_profiles".

    Raises:
        NotImplementedError: If the scale class is not implemented.

    Returns:
        Dict[str, Scale]: A dictionary of scales.
    """
    scales = {}
    for identifier in os.listdir(path):
        scale_profile = json.load(open(os.path.join(path, identifier)))
        scale_class = scale_profile["class"]

        if scale_class == "BowlScale":
            scales[identifier] = BowlScale(**scale_profile)
        else:
            raise NotImplementedError(f"Scale class {scale_class} not implemented.")
    return scales


def check_scale_exists(scale_id: str, scales: Dict[str, Scale]):
    """
    check_scale_exists Check if a scale with the given ID exists.

    Args:
        scale_id (str): The ID of the scale to check.
        scales (Dict[str, Scale]): The dictionary of scales.

    Raises:
        HTTPException: If the scale with the given ID does not exist.
    """
    if scale_id not in scales:
        raise HTTPException(
            status_code=404, detail=f"Scale with ID {scale_id} not found."
        )


def unit_converter(kg: float, unit: str) -> float:
    """
    _unit_converter Convert the value to the specified unit from kilograms (kg)

    Args:
        kg (float): The value to convert from kg
        unit (str): The unit to convert to

    Returns:
        float: The converted value
    """
    if unit == "kg":
        return kg
    elif unit == "g":
        return kg * 1000
    elif unit == "lb":
        return kg * 2.20462
    elif unit == "oz":
        return kg * 35.274
    else:
        raise ValueError("Unit not supported")


def unit_converer(value: float, to_unit: str, from_unit: str = "kg") -> float:
    """
    unit_converter Convert the value from one unit to another.

    Args:
        value (float): The value to convert.
        to_unit (str): The unit to convert to.
        from_unit (str, optional): The unit to convert from. Defaults to "kg".

    Raises:
        ValueError: If the conversion is not supported.

    Returns:
        float: The converted value.
    """

    conversion_rates = {
        "g": {"g": 1, "kg": 0.001, "l": 0.001, "ml": 1},
        "kg": {"g": 1000, "kg": 1, "l": 1, "ml": 1000},
        "l": {"g": 1000, "kg": 1, "l": 1, "ml": 1000},
        "ml": {"g": 1, "kg": 0.001, "l": 0.001, "ml": 1},
    }

    if from_unit not in conversion_rates or to_unit not in conversion_rates[from_unit]:
        raise ValueError(
            "Conversion from {} to {} not supported".format(from_unit, to_unit)
        )

    return value * conversion_rates[from_unit][to_unit]

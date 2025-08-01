def unit_converter(value: float, to_unit: str, from_unit: str = "kg") -> float:
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

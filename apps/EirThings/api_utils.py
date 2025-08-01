import json
import os
from bowl_scale import BowlScale
from scale_vault import ScaleVault
from fastapi import HTTPException
from typing import Dict
from scale import Scale


def load_scales(
    path: str = "./scale_profiles", vault_root: str = "./data"
) -> Dict[str, Scale]:
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
    vault = ScaleVault(vault_root)

    for profile_path in os.listdir(path):
        scale_profile = json.load(open(os.path.join(path, profile_path)))
        scale_class = scale_profile["class"]
        identifier = scale_profile["properties"]["identifier"]

        if scale_class == "BowlScale":
            scales[identifier] = BowlScale(vault=vault, **scale_profile["properties"])
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

import json
import os
import time
from typing import List

TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"


class ScaleVault:
    def __init__(self, root: str = "./data"):
        self.root = root

    def store_data(
        self,
        identifier: str,
        category: str,
        type: str,
        data: dict,
        timestamp: float = time.time(),
    ) -> bool:
        """
        _store_data Store data in the vault

        Args:
            category (str): The category of the data (calibration, measurement, etc.)
            type (str): The type of data (offset, weight, etc.)
            data (dict): The actual data

        Returns:
            bool: True if the data was stored successfully

        """
        # Make sure folder exists
        data_folder = self._vault_path_format(identifier, category, type)
        os.makedirs(data_folder, exist_ok=True)

        # Write file
        file_path = self._file_path_format(data_folder, timestamp)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Data stored at: {file_path}")

        return True

    def load_data(
        self,
        identifier: str,
        category: str,
        type: str,
        timestamp: float = None,
        latest: bool = False,
        includ_path_metadata: bool = False,
    ) -> dict | List[dict]:
        """
        _load_data Load data from the vault

        Args:
            category (str): The category of the data (calibration, measurement, etc.)
            type (str): The type of data (offset, weight, etc.)
            timestamp (float): The timestamp of the data as second since epoch
            includ_path_data (bool, optional): Include the path data in the returned data. Defaults to True
            include_timstamp (bool, optional): Include the timestamp in the returned data. Defaults to True
        Returns:
            dict: The data
        """
        data_folder = self._vault_path_format(identifier, category, type)
        if not os.path.exists(data_folder):
            print(f"No vault data at: {data_folder}")
            return []

        timestamps = [timestamp]
        if timestamp is None:
            timestamps = [
                self._extract_filename_timestamp(file_name)
                for file_name in os.listdir(data_folder)
            ]

        if latest:
            timestamps = [max(timestamps)]

        all_data = []
        for timestamp in timestamps:

            # Load the data
            file_path = self._file_path_format(data_folder, timestamp)
            with open(file_path) as f:
                data = dict(json.load(f))

            # Get the path data
            if includ_path_metadata:
                data.update(self._extract_path_data(file_path))

            all_data.append(data)

        return all_data[0] if latest else all_data

    def _vault_path_format(self, identifier, category: str, type: str) -> str:
        """
        _vault_format Format data to be stored in the vault

        Returns:
            str: The path for the vault
        """
        return os.path.join(
            self.root,
            f"identifier={identifier}",
            f"category={category}",
            f"type={type}",
        )

    def _file_path_format(self, vault_path: str, timestamp: float) -> str:
        """
        _file_path_format Format the file path

        Args:
            vault_path (str): The vault path
            timestamp (float): The timestamp (s)


        Returns:
            str: The formatted file path
        """
        return os.path.join(
            vault_path,
            f"{time.strftime(TIMESTAMP_FORMAT, time.localtime(timestamp))}.json",
        )

    def _extract_path_data(self, path: str) -> dict:
        """
        _extract_path_data Extract data from the path

        Args:
            path (str): The path to extract data from

        Returns:
            dict: The extracted data
        """
        path_parts, tail = os.path.split(path)

        # Extract the time from the filename
        data = {"timestamp": self._extract_filename_timestamp(tail)}

        # Extract the data from the path
        for component in path_parts:
            if "=" in component:
                for key, value in component.split("="):
                    data[key] = value

        return data

    def _extract_filename_timestamp(self, file_name: str) -> float:
        """
        _extract_filename_timestamp Extract the timestamp from the filename"

        Args:
            file_name (str): The filename to extract the timestamp from

        Returns:
            float: The timestamp (s)
        """

        return time.mktime(time.strptime(file_name.split(".")[0], TIMESTAMP_FORMAT))

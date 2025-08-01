from numpy import median
import os
import time

from scale import Scale
from scale_vault import ScaleVault
from scale_utils import unit_converter

if os.getenv("EXEC_MODE") != "TEST":
    from hx711 import HX711
else:
    from dummy_sensor import HX711

    print("Using dummy sensor.")


class BowlScale(Scale, HX711):
    def __init__(
        self,
        identifier: str,
        vault: ScaleVault,
        dout_pin=5,
        pd_sck_pin=6,
        gain=64,
        channel="A",
    ):
        super().__init__(dout_pin, pd_sck_pin, gain, channel)

        print(f"Initializing BowlScale with identifier: {identifier}..")
        self.identifier = identifier
        self.vault = vault
        self.calibration_data = {}
        self._load_calibration_data()

    def status(self) -> bool:
        """
        status Method for checking if the scale is connected.

        Returns:
            bool: True if the scale is connected, False otherwise.
        """

        return self._calibration_status()

    def tare(self) -> bool:
        """
        tare Calculate the offset value of an empty scale

        Returns:
            int: The offset value
        """
        print("Taring scale")

        # Before we start, reset the HX711 (not obligate)
        self.reset()

        # Get measurements
        measurements = self.get_raw_data()
        median_measurement = median(measurements)

        # Store the offset value
        timestamp = time.time()
        self.vault.store_data(
            self.identifier,
            "calibration",
            "offset",
            {"value": median_measurement},
            timestamp,
        )
        self.calibration_data["offset"] = {
            "value": median_measurement,
            "timestamp": timestamp,
        }

        print(f"Calibrated offset: {median_measurement}")

        return True

    def calibrate(self, weight: float, unit: str) -> bool:
        """
        calibrate Method for calibrating the scale to a known weight in the given unit.

        Args:
            weight (float): The known weight in the given unit.
            unit (str): The unit of the known weight.

        Returns:
            bool: True if calibration was successful, False otherwise.
        """
        print(f"Calibrating scale to {weight} [{unit}]")

        if "offset" not in self.calibration_data:
            raise AttributeError(
                "Missing offsett. Call tare() while the scale is empty to calibrate the bowls offset bore calibrating gain."
            )

        self.reset()
        measurements = self.get_raw_data()
        median_measurement = median(measurements)

        # Calculate the scale factor
        gain = weight / (median_measurement - self.calibration_data["offset"]["value"])

        # Store the calibration data
        timestamp = time.time()
        self.vault.store_data(
            self.identifier,
            "calibration",
            "gain",
            {"value": gain, "unit": unit},
            timestamp,
        )
        self.calibration_data["gain"] = {
            "value": gain,
            "unit": unit,
            "timestamp": timestamp,
        }

        print(f"Calibrated gain: {gain} [{unit}]")

        return True

    def read(self, unit: str = "kg", store_vault: bool = False) -> float:
        """
        read Method for reading the weight from the scale.

        Args:
            unit (str): The unit to get the weight in.

        Returns:
            float: The weight in the specified unit.
        """

        if not self._calibration_status():
            raise AttributeError(
                "Scale not calibrated. Calibrate the scale before reading."
            )

        self.reset()
        timestamp = time.time()
        measurements = self.get_raw_data()
        median_measurement = median(measurements)

        if store_vault:
            self.vault.store_data(
                self.identifier,
                "measurement",
                "weight",
                {"value": median_measurement},
                timestamp,
            )

        weight = (
            median_measurement - self.calibration_data["offset"]["value"]
        ) * self.calibration_data["gain"]["value"]

        return unit_converter(weight, self.calibration_data["gain"]["unit"], unit)

    def _calibration_status(self) -> bool:
        """
        _calibration_status Check if the scale is calibrated

        Returns:
            bool: True if the scale is calibrated, False otherwise
        """
        required_calibraiton_data = {"offset", "gain"}
        calibraiton_data_status = set()

        for data_type in required_calibraiton_data:
            if data_type in self.calibration_data:
                print(f"{str.title(data_type)}: {self.calibration_data[data_type]}")
                calibraiton_data_status.add(data_type)

        if calibraiton_data_status == required_calibraiton_data:
            return True
        else:
            missing_data = required_calibraiton_data - calibraiton_data_status
            print(f"Missing calibration data: {missing_data}")
            return False

    def _load_calibration_data(self) -> bool:
        """
        _load_calibration_data Load the calibration data from the vault

        Returns:
            bool: True if the calibration data was loaded successfully, False otherwise
        """

        print(f"Loading latest calibration data for {self.identifier}")

        # Load the offset
        offset_data = self.vault.load_data(
            self.identifier, "calibration", "offset", latest=True
        )
        if offset_data:
            self.calibration_data["offset"] = offset_data

        # Load the gain
        gain_data = self.vault.load_data(
            self.identifier, "calibration", "gain", latest=True
        )
        if gain_data:
            self.calibration_data["gain"] = gain_data

        if self._calibration_status():
            print("Scale calibrated.")
            return True
        else:
            print("Unable to calibrate scale from vault data.")
            return False

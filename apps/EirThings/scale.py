from abc import ABC, abstractmethod, ABCMeta


class Scale(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def status(self) -> bool:
        """
        status Method for checking if the scale is connected.

        Returns:
            bool: True if the scale is connected, False otherwise.
        """
        pass

    @abstractmethod
    def tare(self) -> bool:
        """
        tare Method for setting the scale to zero.

        Returns:
            bool: True if tare was successful, False otherwise.
        """
        pass

    @abstractmethod
    def calibrate(self, wight: float, unit: str) -> bool:
        """
        calibrate Method for calibrating the scale to a known weight in the given unit.

        Args:
            weight (float): The known weight in the given unit.
            unit (str): The unit of the known weight.

        Returns:
            bool: True if calibration was successful, False otherwise.
        """
        pass

    @abstractmethod
    def read(self, unit: str) -> float:
        """
        read Method for reading the weight from the scale.

        Args:
            unit (str): The unit to get the weight in.

        Returns:
            float: The weight in the specified unit.
        """
        pass

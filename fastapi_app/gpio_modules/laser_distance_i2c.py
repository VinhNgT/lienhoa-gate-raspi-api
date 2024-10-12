from time import sleep
from typing import Final

from adafruit_extended_bus import ExtendedI2C as I2C
from adafruit_vl53l0x import VL53L0X


class LaserDistanceI2c:
    MEASUREMENT_TIMING_BUDGET: Final = 200000
    DEFAULT_CALIBRATION_OFFSET: Final = -40

    def __init__(
        self,
        i2c_bus,
        is_continuous=False,
        calibration_offset=DEFAULT_CALIBRATION_OFFSET,
    ):
        self._sensor = VL53L0X(I2C(i2c_bus))
        self._sensor.measurement_timing_budget = self.MEASUREMENT_TIMING_BUDGET
        self.calibration_offset: Final = calibration_offset
        self.is_continuous: Final = is_continuous

        if is_continuous:
            self._sensor.start_continuous()

    def __del__(self):
        if self.is_continuous:
            self._sensor.stop_continuous()

    def get_distance(self) -> int:
        """
        Return the distance in mm
        """
        return max(0, self._sensor.range + self.calibration_offset)


def run_example():
    laser = LaserDistanceI2c(i2c_bus=7, is_continuous=True)

    while True:
        print("Range: {0}mm".format(laser.get_distance()))
        sleep(0.25)


if __name__ == "__main__":
    run_example()

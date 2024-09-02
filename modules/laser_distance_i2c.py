from typing import Final
from adafruit_vl53l0x import VL53L0X
from adafruit_extended_bus import ExtendedI2C as I2C
from time import sleep


class LaserDistanceI2C:
    MEASUREMENT_TIMING_BUDGET: Final = 200000

    def __init__(self, i2c_bus, is_continuous=False, calibration_offset=0):
        self.__sensor = VL53L0X(I2C(i2c_bus))
        self.__sensor.measurement_timing_budget = self.MEASUREMENT_TIMING_BUDGET
        self.calibration_offset: Final = calibration_offset
        self.is_continuous = is_continuous

        if is_continuous:
            self.__sensor.start_continuous()

    def __del__(self):
        if self.is_continuous:
            self.__sensor.stop_continuous()

    def get_distance(self) -> int:
        """
        Return the distance in mm
        """
        return max(0, self.__sensor.range + self.calibration_offset)


def run_example():
    laser = LaserDistanceI2C(i2c_bus=7, is_continuous=True, calibration_offset=-40)

    while True:
        print("Range: {0}mm".format(laser.get_distance()))
        sleep(0.25)


if __name__ == "__main__":
    run_example()

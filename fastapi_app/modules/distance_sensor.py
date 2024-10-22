from fastapi import APIRouter
from pydantic import BaseModel

from fastapi_app.gpio_modules import LaserDistanceI2c


class DistanceSensor:
    def __init__(self):
        self._sensor = LaserDistanceI2c(i2c_bus=7)

    def get_distance(self) -> float:
        return self._sensor.get_distance()


class DistanceSensorResponse(BaseModel):
    distance: float


router = APIRouter(
    prefix="/distance_sensor",
    tags=["distance_sensor (module VL53L0X)"],
)
distance_sensor = DistanceSensor()


@router.get(
    "/",
    summary="Get the distance sensor reading",
    response_model=DistanceSensorResponse,
)
def get_distance():
    return DistanceSensorResponse(distance=distance_sensor.get_distance())

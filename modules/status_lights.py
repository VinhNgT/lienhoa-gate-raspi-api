from enum import Enum
from pydantic import BaseModel
from fastapi import APIRouter, Form
from typing import Annotated
from gpio_modules.leds_i2c import LedsI2c


class StatusLightState(str, Enum):
    NONE = "none"
    CAR_DETTECTED = "car_detected"
    PROCESSING = "processing"
    ALLOW = "allow"
    DENY = "deny"


class StatusLights:
    def __init__(self):
        self.leds = LedsI2c(i2c_bus=8, led_count=4)
        self.set_status(StatusLightState.NONE)

    def set_status(self, state: StatusLightState):
        match state:
            case StatusLightState.NONE:
                self.leds.set_leds_bits(0b0000)

            case StatusLightState.CAR_DETTECTED:
                self.leds.set_leds_bits(0b0001)

            case StatusLightState.PROCESSING:
                self.leds.set_leds_bits(0b0010)

            case StatusLightState.ALLOW:
                self.leds.set_leds_bits(0b0100)

            case StatusLightState.DENY:
                self.leds.set_leds_bits(0b1000)

        self.current_state = state


class StatusLightsStateResponse(BaseModel):
    state: StatusLightState


router = APIRouter(
    prefix="/status_lights_state",
    tags=["status_lights_state"],
)
status_lights = StatusLights()


@router.get(
    "/",
    summary="Get status lights state",
    response_model=StatusLightsStateResponse,
)
def read_status_light():
    """
    Get PCF8574 module status lights state
    """
    return StatusLightsStateResponse(state=status_lights.current_state)


@router.patch(
    "/",
    summary="Set status lights state",
    response_model=StatusLightsStateResponse,
)
def set_status_light(state: Annotated[StatusLightState, Form()]):
    """
    Set PCF8574 module status lights state
    """
    status_lights.set_status(state)
    return StatusLightsStateResponse(state=status_lights.current_state)

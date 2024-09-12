from enum import Enum
from pydantic import BaseModel
from fastapi import APIRouter, Form
from typing import Annotated
from gpio_modules.servo_hw_pwm import ServoHwPwm


class GateState(str, Enum):
    OPEN = "open"
    CLOSE = "close"


class Gate:
    def __init__(self):
        self.servo = ServoHwPwm(pwm_channel=0)
        self.set_status(GateState.CLOSE)

    def set_status(self, state: GateState):
        match state:
            case GateState.CLOSE:
                self.servo.ease_angle(0, ease_seconds=3)

            case GateState.OPEN:
                self.servo.ease_angle(90, ease_seconds=3)

        self.current_state = state


class GateStateResponse(BaseModel):
    state: GateState


router = APIRouter(
    prefix="/gate",
    tags=["gate"],
)
gate = Gate()


@router.get(
    "/",
    summary="Get gate state",
    response_model=GateStateResponse,
)
def read_gate():
    """
    Get the gate current state
    """
    return GateStateResponse(state=gate.current_state)


@router.patch(
    "/",
    summary="Set gate state",
    response_model=GateStateResponse,
)
def set_status_light(state: Annotated[GateState, Form()]):
    """
    Set the gate state
    """
    gate.set_status(state)
    return GateStateResponse(state=gate.current_state)

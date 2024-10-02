from enum import Enum
from pydantic import BaseModel, Field
from fastapi import APIRouter, Form
from typing import Annotated
import atexit
from contextlib import asynccontextmanager

from fastapi_app.gpio_modules import ServoHwPwm
from fastapi_app.utils.request_queue import RequestQueue


class GateState(str, Enum):
    OPEN = "open"
    CLOSE = "close"


class Gate:
    def __init__(self):
        self._servo = ServoHwPwm(pwm_channel=0)

        self.set_status(GateState.CLOSE)
        atexit.register(self._servo.cleanup)

    def set_status(self, state: GateState):
        match state:
            case GateState.CLOSE:
                self._servo.ease_angle(0, ease_seconds=0.5)

            case GateState.OPEN:
                self._servo.ease_angle(90, ease_seconds=0.5)

        self.current_state = state


class GateStateResponse(BaseModel):
    state: GateState = Field(
        description="Current state of the gate",
        examples=["open", "close"],
    )


gate = Gate()
request_queue = RequestQueue(3)


@asynccontextmanager
async def lifespan(app: APIRouter):
    yield
    request_queue.shutdown()


router = APIRouter(
    prefix="/gate",
    tags=["gate (module MG90S)"],
    lifespan=lifespan,
)


@router.get(
    "/",
    summary="Get gate state",
    response_model=GateStateResponse,
)
def read_gate():
    return GateStateResponse(state=gate.current_state)


@router.patch(
    "/",
    summary="Set gate state",
    response_model=GateStateResponse,
)
def set_gate(state: Annotated[GateState, Form()]):
    request_queue.submit(gate.set_status, state)

    return GateStateResponse(state=gate.current_state)

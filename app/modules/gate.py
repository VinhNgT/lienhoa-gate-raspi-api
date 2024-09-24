from enum import Enum
from pydantic import BaseModel, Field
from fastapi import APIRouter, Form, BackgroundTasks
from typing import Annotated
import atexit
import threading

from app.gpio_modules import ServoHwPwm
from app.exceptions import app_exceptions
from app.utils.request_count_tracker import RequestCountTracker


class GateState(str, Enum):
    OPEN = "open"
    CLOSE = "close"


class Gate:
    def __init__(self):
        self._servo = ServoHwPwm(pwm_channel=0)
        self._lock = threading.Semaphore()
        self._requests_count_tracker = RequestCountTracker(3)

        self.set_status(GateState.CLOSE)
        atexit.register(self._servo.cleanup)

    @property
    def is_limited(self):
        return self._requests_count_tracker.is_max_requests_reached()

    def set_status(self, state: GateState):
        if self.is_limited:
            raise app_exceptions.TooManyRequestsException()

        with self._requests_count_tracker:
            with self._lock:
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


router = APIRouter(
    prefix="/gate",
    tags=["gate (module MG90S)"],
)
gate = Gate()


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
def set_gate(state: Annotated[GateState, Form()], background_tasks: BackgroundTasks):
    if gate.is_limited:
        raise app_exceptions.TooManyRequestsException()

    background_tasks.add_task(gate.set_status, state)
    return GateStateResponse(state=gate.current_state)
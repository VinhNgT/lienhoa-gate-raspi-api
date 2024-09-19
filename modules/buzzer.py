from pydantic import BaseModel, Field
from fastapi import APIRouter, Form, BackgroundTasks, Body
from typing import Annotated
from gpio_modules.buzzer_hw_pwm import BuzzerHwPwm
import atexit
import threading
from modules.exceptions import app_exceptions
from modules.utils.request_count_tracker import RequestCountTracker


class Buzzer:
    def __init__(self):
        self._buzzer = BuzzerHwPwm(pwm_channel=1)
        self._lock = threading.Lock()
        self._requests_count_tracker = RequestCountTracker(3)

        atexit.register(self._buzzer.cleanup)

    @property
    def is_limited(self):
        return self._requests_count_tracker.is_max_requests_reached()

    def beep(self, frequency, duration):
        if self.is_limited:
            raise app_exceptions.TooManyRequestsException()

        with self._requests_count_tracker:
            with self._lock:
                self._buzzer.beep(frequency, duration)


class BuzzerFormData(BaseModel):
    frequency: float = Field(
        description="Frequency in Hz",
        examples=[600, 1000],
        ge=0.1,
        le=1000,
    )
    duration: float = Field(
        description="Duration in seconds",
        examples=[0.5, 1.0],
        ge=0.1,
        le=5,
    )


router = APIRouter(
    prefix="/buzzer",
    tags=["buzzer (passive)"],
)
buzzer = Buzzer()


@router.post(
    "/",
    summary="Set buzzer frequency and duration",
    response_model=BuzzerFormData,
)
def set_buzzer(
    data: Annotated[BuzzerFormData, Form()],
    background_tasks: BackgroundTasks,
):
    if buzzer.is_limited:
        raise app_exceptions.TooManyRequestsException()

    background_tasks.add_task(buzzer.beep, data.frequency, data.duration)
    return BuzzerFormData(frequency=data.frequency, duration=data.duration)

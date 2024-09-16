from pydantic import BaseModel
from fastapi import APIRouter, Form, BackgroundTasks
from typing import Annotated
from gpio_modules.buzzer_hw_pwm import BuzzerHwPwm
import atexit
import threading


class Buzzer:
    def __init__(self):
        self._buzzer = BuzzerHwPwm(pwm_channel=1)
        self._lock = threading.Lock()

        atexit.register(self._buzzer.cleanup)

    def beep(self, frequency, duration):
        with self._lock:
            self._buzzer.beep(frequency, duration)


class BuzzerFormData(BaseModel):
    frequency: float
    duration: float


router = APIRouter(
    prefix="/buzzer",
    tags=["buzzer"],
)
buzzer = Buzzer()


@router.post(
    "/",
    summary="Set buzzer frequency and duration",
    response_model=BuzzerFormData,
)
def set_buzzer(
    data: Annotated[BuzzerFormData, Form()], background_tasks: BackgroundTasks
):
    """
    Set buzzer frequency and duration
    """
    background_tasks.add_task(buzzer.beep, data.frequency, data.duration)
    return BuzzerFormData(frequency=data.frequency, duration=data.duration)

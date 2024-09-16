from pydantic import BaseModel
from fastapi import APIRouter, Form
from typing import Annotated
from gpio_modules.buzzer_hw_pwm import BuzzerHwPwm


class Buzzer:
    def __init__(self):
        self._buzzer = BuzzerHwPwm(pwm_channel=1)

    def beep(self, frequency, duration):
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
def set_buzzer(data: Annotated[BuzzerFormData, Form()]):
    """
    Set buzzer frequency and duration
    """
    buzzer.beep(data.frequency, data.duration)
    return BuzzerFormData(frequency=data.frequency, duration=data.duration)

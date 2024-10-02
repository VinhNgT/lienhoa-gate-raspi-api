from pydantic import BaseModel, Field
from fastapi import APIRouter, Form
from typing import Annotated
import atexit
from contextlib import asynccontextmanager

from fastapi_app.gpio_modules import BuzzerHwPwm
from fastapi_app.utils.request_queue import RequestQueue


class Buzzer:
    def __init__(self):
        self._buzzer = BuzzerHwPwm(pwm_channel=1)
        atexit.register(self._buzzer.cleanup)

    def beep(self, frequency, duration):
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


buzzer = Buzzer()
request_queue = RequestQueue(3)


@asynccontextmanager
async def lifespan(app: APIRouter):
    yield
    request_queue.shutdown()


router = APIRouter(
    prefix="/buzzer",
    tags=["buzzer (passive)"],
    lifespan=lifespan,
)


@router.post(
    "/",
    summary="Set buzzer frequency and duration",
    response_model=BuzzerFormData,
)
def set_buzzer(data: Annotated[BuzzerFormData, Form()]):
    request_queue.submit(buzzer.beep, data.frequency, data.duration)

    return BuzzerFormData(frequency=data.frequency, duration=data.duration)

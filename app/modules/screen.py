from pydantic import BaseModel, Field
from fastapi import APIRouter, Form
from typing import Annotated
from gpio_modules.lcd_i2c import LcdI2c
import atexit
import threading


class LcdScreen:
    def __init__(self):
        self._lcd = LcdI2c(i2c_bus=1)
        self._lock = threading.Lock()

        atexit.register(self.cleanup)

    def write_string(self, text: str):
        with self._lock:
            self._lcd.write_string(text)

    def cleanup(self):
        self._lcd.clear()
        self.write_string("LCD connection closed")
        self._lcd.close()


class LcdFormData(BaseModel):
    text: str = Field(
        description="Text to display on the screen",
        examples=["Hello, World!"],
    )


class LcdResponse(BaseModel):
    text: str


router = APIRouter(
    prefix="/screen",
    tags=["screen (module 2004A with PCF8574 I2C backpack)"],
)
screen = LcdScreen()


@router.post(
    "/",
    summary="Set lcd screen text",
    response_model=LcdResponse,
)
def set_lcd_text(data: Annotated[LcdFormData, Form()]):
    screen.write_string(data.text)
    return LcdResponse(text=data.text)

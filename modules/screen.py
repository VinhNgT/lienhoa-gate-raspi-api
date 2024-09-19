from pydantic import BaseModel, Field
from fastapi import APIRouter, Form
from typing import Annotated
from gpio_modules.lcd_i2c import LcdI2c


class LcdScreen:
    def __init__(self):
        self._lcd = LcdI2c(i2c_bus=1)

    def write_string(self, text: str, format_string: bool):
        self._lcd.write_string(text, format_string=format_string)


class LcdFormData(BaseModel):
    text: str = Field(
        description="Text to display on the screen",
        examples=["Hello, World!"],
    )
    format: bool = True


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
    screen.write_string(data.text, data.format)
    return LcdResponse(text=data.text)

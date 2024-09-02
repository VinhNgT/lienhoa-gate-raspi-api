from pydantic import BaseModel

class SetGPIO(BaseModel):
    on: bool


class GpioStatusResponse(BaseModel):
    gpio: int
    on: bool
from fastapi import FastAPI
from domain.general import GpioStatusResponse, SetGPIO
from modules.leds_i2c import LedsI2c


app = FastAPI()
leds = LedsI2c(i2c_bus=8, led_count=4)


@app.get("/read/{gpio}")
def read_gpio(gpio: int):
    return GpioStatusResponse(gpio=gpio, on= leds.get_led(gpio))


@app.patch("/set/{gpio}")
def set_gpio(gpio: int, value: SetGPIO):
    leds.set_led(gpio, value.on)
    return GpioStatusResponse(gpio=gpio, on=value.on)

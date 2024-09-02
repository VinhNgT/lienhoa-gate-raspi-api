from fastapi import FastAPI
from time import sleep
import adafruit_pcf8574
from adafruit_extended_bus import ExtendedI2C as I2C


from domain.general import GpioStatusResponse, SetGPIO

i2c = I2C(8)
pcf = adafruit_pcf8574.PCF8574(i2c, address=0x20)

pcf.get_pin(0).switch_to_output(True)
pcf.get_pin(1).switch_to_output(True)
pcf.get_pin(2).switch_to_output(True)
pcf.get_pin(3).switch_to_output(True)
pcf.get_pin(4).switch_to_output(True)
pcf.get_pin(5).switch_to_output(True)
pcf.get_pin(6).switch_to_output(True)
pcf.get_pin(7).switch_to_output(True)


app = FastAPI()


@app.get("/read/{gpio}")
def read_gpio(gpio: int):
    return GpioStatusResponse(gpio=gpio, on=not pcf.get_pin(gpio).value)


@app.patch("/set/{gpio}")
def set_gpio(gpio: int, value: SetGPIO):
    pcf.get_pin(gpio).value = not value.on
    return GpioStatusResponse(gpio=gpio, on=value.on)

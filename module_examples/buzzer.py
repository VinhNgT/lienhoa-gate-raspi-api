from rpi_hardware_pwm import HardwarePWM
from time import time, sleep
import math

pwm = HardwarePWM(pwm_channel=1, hz=600, chip=0)
pwm.start(0)

for i in range(5):
    pwm.change_duty_cycle(50)
    sleep(0.5)
    pwm.change_duty_cycle(0)
    sleep(0.1)

pwm.stop()

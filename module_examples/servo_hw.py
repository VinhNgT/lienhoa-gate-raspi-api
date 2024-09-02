from rpi_hardware_pwm import HardwarePWM
import time

pwm = HardwarePWM(pwm_channel=1, hz=50, chip=0)
time.sleep(1)
pwm.start(0)


try:
    while True:
        pwm.change_duty_cycle(2.85)
        time.sleep(1)
        pwm.change_duty_cycle(12.55)
        time.sleep(1)


except KeyboardInterrupt:
    pwm.stop()
    print("Servo stopped")

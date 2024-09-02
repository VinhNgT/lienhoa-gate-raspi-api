from rpi_hardware_pwm import HardwarePWM
from time import sleep


class BuzzerHwPwm:
    def __init__(self, pwm_channel):
        self.pwm = HardwarePWM(pwm_channel=pwm_channel, hz=100, chip=0)
        self.pwm.start(0)

    def __del__(self):
        self.pwm.stop()

    def beep(self, frequency, duration):
        self.pwm.change_frequency(frequency)
        self.pwm.change_duty_cycle(50)
        sleep(duration)
        self.pwm.change_duty_cycle(0)


def run_example():
    buzzer = BuzzerHwPwm(pwm_channel=1)

    for i in range(5):
        buzzer.beep(frequency=600, duration=0.5)
        sleep(0.1)


if __name__ == "__main__":
    run_example()

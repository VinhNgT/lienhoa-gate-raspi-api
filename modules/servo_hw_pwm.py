from rpi_hardware_pwm import HardwarePWM
from time import time, sleep
import math
from typing import Final

SERVO_DEFAULT_SLEEP_DURATION = 0.5


class ServoHwPwm:
    SERVO_FREQUENCY: Final = 50
    SERVO_MIN_ANGLE: Final = 0
    SERVO_MAX_ANGLE: Final = 180

    def __init__(self, pwm_channel, min_duty=2.85, max_duty=12.55):
        self.min_duty: Final = min_duty
        self.max_duty: Final = max_duty
        self.angle_duty_ratio: Final = (
            self.max_duty - self.min_duty
        ) / self.SERVO_MAX_ANGLE

        # Initialize PWM
        self.__pwm: Final = HardwarePWM(
            pwm_channel=pwm_channel, hz=self.SERVO_FREQUENCY, chip=0
        )
        self.__pwm.start(min_duty)

        # Variables
        self.current_angle = self.SERVO_MIN_ANGLE
        self.current_duty = self.min_duty

    def __del__(self):
        self.__pwm.change_duty_cycle(self.min_duty)
        sleep(SERVO_DEFAULT_SLEEP_DURATION)
        self.__pwm.stop()

    def __set_duty(self, duty: float):
        # Warn: Setting the duty too high or too low will confused the servo.
        # Fix by unplug and plug the servo in again or the power source.
        #
        # Clamp the duty value so this doesn't happen.
        clampped_duty = max(self.min_duty, min(self.max_duty, duty))

        self.__pwm.change_duty_cycle(clampped_duty)
        self.current_angle = (clampped_duty - self.min_duty) / self.angle_duty_ratio
        self.current_duty = clampped_duty

    def set_angle(self, angle: float):
        self.__set_duty(self.min_duty + self.angle_duty_ratio * angle)

    def ease_angle(self, angle: float, ease_seconds: float):
        if ease_seconds <= 0:
            raise ValueError("ease_time must be greater than 0")

        # Skip if the requested angle is the same as the current angle.
        if angle == self.current_angle:
            return

        # The number of steps to finish the operation.
        # We multiply by 2 to make the movement smoother.
        steps = math.ceil(self.SERVO_FREQUENCY * ease_seconds * 2)

        # The time for each step.
        step_delay = ease_seconds / steps

        # The angle by which the servo needs to move in each step.
        step_size = (angle - self.current_angle) / steps

        # Perform stepping
        for i in range(steps):
            target_angle = round(self.current_angle + step_size, 4)
            print(f"Step {i + 1}/{steps}, moving to {target_angle}")
            self.set_angle(target_angle)

            # After the last step, we don't need to sleep because the operation
            # is finished.
            # if i == steps - 1:
            #     break

            sleep(step_delay)


def run_example_1():
    servo = ServoHwPwm(pwm_channel=0)

    try:
        while True:
            for i in [0, 90, 180, 90]:
                servo.set_angle(i)
                sleep(SERVO_DEFAULT_SLEEP_DURATION)

    except KeyboardInterrupt:
        pass


def run_example_2():
    servo = ServoHwPwm(pwm_channel=0)

    while True:
        input_angle = float(input("Enter angle: "))
        servo.ease_angle(input_angle, ease_seconds=60)


if __name__ == "__main__":
    run_example_1()
    # run_example_2()

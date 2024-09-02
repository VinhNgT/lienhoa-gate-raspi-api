import time
import adafruit_pcf8574
from adafruit_extended_bus import ExtendedI2C as I2C

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


def reverse_bits(byte):
    result = 0
    for i in range(8):
        # Move the result one bit to the left and add the least significant bit
        # of byte to it.
        result = (result << 1) | (byte & 1)

        # Shift the byte one bit to the right. Prepare for the next iteration.
        byte >>= 1

    return result


def set_leds_byte(byte):
    # The PCF8574 pins start from the least significant bit, so we need to reverse
    # the bit pattern.
    reversed = reverse_bits(byte)

    # The LEDs use 'active low' logic, so we need to flip the bits.
    flipped = ~reversed & 0xFF

    pcf.write_gpio(flipped)


# Initial bit pattern
#
# To make it easier to see the pattern, we assume the most
# significant bit is the left most LED.
bit_pattern = 0b10000000


while True:
    set_leds_byte(bit_pattern)
    time.sleep(0.25)

    # Rotate the bit pattern to the right
    bit_pattern = ((bit_pattern >> 1) | (bit_pattern << 7)) & 0xFF
    print(bin(bit_pattern))

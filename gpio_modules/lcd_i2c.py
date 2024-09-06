from RPLCD.i2c import CharLCD


class LcdI2c:
    def __init__(self, i2c_bus, i2c_addr=0x27):
        self.__lcd = CharLCD(
            i2c_expander="PCF8574",
            address=i2c_addr,
            port=i2c_bus,
            cols=20,
            rows=4,
        )

    def __del__(self):
        self.__lcd.clear()
        self.write_string("LCD connection closed")
        self.__lcd.close()

    def __format_string(self, input_string: str, max_length=20) -> str:
        words = input_string.split()
        lines = []

        for word in words:
            if len(word) >= max_length or len(lines) == 0:
                lines.append(word)
                continue

            if (len(lines[-1]) + len(" ") + len(word)) < max_length:
                lines[-1] += f" {word}"
                continue

            lines.append(word)

        return "\r\n".join(lines)

    def clear(self):
        self.__lcd.clear()

    def write_string(self, text: str, clear=True, format_string=True):
        if clear:
            self.clear()

        self.__lcd.write_string(self.__format_string(text) if format_string else text)


def run_example():
    lcd = LcdI2c(i2c_bus=1)
    lcd.write_string("Hello World!")
    while True:
        input_str = input("Enter string to print to the LCD: ")
        lcd.clear()
        lcd.write_string(input_str)


if __name__ == "__main__":
    run_example()

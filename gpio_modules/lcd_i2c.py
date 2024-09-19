from RPLCD.i2c import CharLCD
from itertools import chain
from typing import Final


class LcdI2c:
    MAX_LINE_LENGTH: Final = 20
    MAX_LINE_COUNT: Final = 4

    def __init__(self, i2c_bus, i2c_addr=0x27):
        self._lcd = CharLCD(
            i2c_expander="PCF8574",
            address=i2c_addr,
            port=i2c_bus,
            cols=20,
            rows=4,
        )

    # def __del__(self):
    #     self._lcd.clear()
    #     self.write_string("LCD connection closed")
    #     self._lcd.close()

    def _auto_newline(
        self, input_string: str, max_line_length=MAX_LINE_LENGTH
    ) -> list[str]:
        words = input_string.split()
        lines = []

        for word in words:
            if len(word) >= max_line_length or len(lines) == 0:
                lines.append(word)
                continue

            if (len(lines[-1]) + len(" ") + len(word)) <= max_line_length:
                lines[-1] += f" {word}"
                continue

            lines.append(word)

        return lines

    def clear(self):
        self._lcd.clear()

    def write_string(self, text: str, clear=True, format_string=True):
        lines = text.strip().split("\n")
        lines = list(
            chain.from_iterable(
                [self._auto_newline(line) if line != "" else [""] for line in lines]
            )
        )

        if clear:
            self.clear()

        print("Sending text to LCD:")
        for i, line in enumerate(lines):
            print(line)

            if i >= self.MAX_LINE_COUNT:
                raise ValueError(
                    f"Number of lines is greater than {self.MAX_LINE_COUNT}: {lines}"
                )

            if len(line) > self.MAX_LINE_LENGTH:
                raise ValueError(
                    f"Line length is greater than {self.MAX_LINE_LENGTH} characters: {line}"
                )

            self._lcd.write_string(line)
            self._lcd.crlf()


def run_example():
    def get_multiline_input() -> str:
        print("Enter/Paste your content. Type #d to finish.")
        lines = []

        while True:
            line = input()

            if line != "#d":
                lines.append(line)
            else:
                break

        text = "\n".join(lines)
        return text

    lcd = LcdI2c(i2c_bus=1)
    lcd.write_string("Hello World!")

    while True:
        input_str = get_multiline_input()

        lcd.clear()
        lcd.write_string(input_str)


def run_example_print():
    lcd = LcdI2c(i2c_bus=1)
    lcd.write_string(("8" * 20 + "\n") * 4)


if __name__ == "__main__":
    # run_example()
    run_example_print()

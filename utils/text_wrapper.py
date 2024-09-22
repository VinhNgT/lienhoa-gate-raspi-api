from typing import Final
import re
from more_itertools import batched


class StringObject:
    def __init__(self, content: str):
        self._content = content

    def __len__(self) -> int:
        return len(self._content)

    def __str__(self) -> str:
        return self._content


class Word(StringObject):
    def __init__(self, content: str):
        super().__init__(content)


class Spaces(StringObject):
    def __init__(self, content: str):
        super().__init__(content)


class TextWrapper :
    def __init__(self, max_line_length: int):
        self.max_line_length: Final = max_line_length

    def _convert_to_str_objs(self, text: str) -> list[StringObject]:
        split: list[str] = re.findall(r"\S+|\s+", text)
        return [Spaces(item) if item.isspace() else Word(item) for item in split]

    def _get_remaining_space(self, line: str) -> int:
        return self.max_line_length - len(line)

    def wrap(self, text: str) -> list[str]:
        if len(text) == 0:
            return []

        str_objs: list[StringObject] = self._convert_to_str_objs(text)
        lines: list[str] = [""]

        for obj in str_objs:
            if self._get_remaining_space(lines[-1]) >= len(obj):
                lines[-1] += str(obj)
                continue

            match obj:
                case Spaces():
                    space_to_newline_num = (len(lines[-1]) + len(obj)) // (
                        self.max_line_length + 1
                    )
                    compound_line = lines[-1] + str(obj)[:-space_to_newline_num]
                    lines_to_be_added = [
                        "".join(str_tuple)
                        for str_tuple in batched(compound_line, self.max_line_length)
                    ]

                    lines.pop()
                    lines.extend(lines_to_be_added)

                case Word():
                    lines_to_be_added = [
                        "".join(str_tuple)
                        for str_tuple in batched(str(obj), self.max_line_length)
                    ]

                    if len(lines[-1]) == 0:
                        lines.pop()

                    lines.extend(lines_to_be_added)

        return [line.rstrip() for line in lines]


def run_example():
    formatter = TextWrapper (20)
    text = "Hello, World!        888888"

    result = formatter.wrap(text)
    for line in result:
        print(line)


if __name__ == "__main__":
    run_example()

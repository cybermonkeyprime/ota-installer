from dataclasses import dataclass, field
from enum import Enum
from typing import Self

import src.display.variables.functions as functions


@dataclass
class EnumBuilder(object):
    title: str = field(init=False)
    value: str = field(init=False)

    def set_title(self, title: str) -> Self:
        self.title = str(title)
        return self

    def set_value(self, value: str) -> Self:
        self.value = str(value)
        return self

    def set_data_enum(self) -> Self:
        self.data_enum = Enum(
            "DataEnum",
            {
                "TITLE": str(self.title),
                "VALUE": str(self.value),
            },
        )
        return self

    def show_output(self) -> None:
        functions.parse_output(self.data_enum)


def main():
    pass


if __name__ == "__main__":
    main()

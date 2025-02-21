from dataclasses import dataclass
from build.styles.palette import Colors


@dataclass
class Colorize:
    style = ""
    value = ""

    def __call__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.style}{self.value}{Colors.reset}"

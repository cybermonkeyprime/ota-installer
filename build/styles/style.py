from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from pyfiglet import figlet_format

from build.styles import Colors, Indentation


@dataclass
class Decorators:
    @dataclass
    class Indent:
        """Decorator to indent text."""
        interval: int = 0
        char = " "

        def __call__(self, function):
            def inner(*args, **kwargs):
                result = function(*args, **kwargs)
                return f"{self.indent()}{result}"

            return inner

        def indent(self):
            return f"{Indentation(char=self.char, interval=self.interval)}"

    @dataclass
    class Colorize:
        """Decorator to colorize text."""
        style: str = ""

        def __call__(self, function):
            @wraps(function)
            def inner(*args, **kwargs):
                result = function(*args, **kwargs)
                return f"{self._style()}{result}{Colors.default}"

            return inner

        def _style(self):
            if self.style in Colors.__annotations__.keys():
                return eval(f"Colors.{self.style}")
            else:
                return "[blue]"

    @dataclass
    class MultiplyString:
        interval: str = ""

        def __call__(self, function):
            @wraps(function)
            def inner(*args, **kwargs):
                result = function(*args, **kwargs)
                return f"{result * self.interval}"

            return inner

    @dataclass
    class Figletize:
        """Decorator to apply figlet formatting to text."""
        font: str = "slant"

        def __call__(self, function):
            @wraps(function)
            def inner(*args, **kwargs):
                result = function(*args, **kwargs)
                return f"{figlet_format(result, font=self.font)}"

            return inner

    @dataclass
    class Print:
        """Decorator to print the result of a function."""
        begin: str = ""
        color: bool = False
        end: str = "\n"

        def __call__(self, function):
            @wraps(function)
            def inner(*args, **kwargs):
                result = function(*args, **kwargs)
                print(f"{self.begin}{result}", end=self.end)
                return result

            return inner


    @dataclass
    class PrintColorize:
        """Decorator to print the result of a function."""
        begin: str = ""
        end: str = ""
        style: str = "variable"

        def __call__(self, function: Callable) -> Any:
            @Decorators.Print(color=False)
            @Decorators.Colorize(style=self.style)
            @wraps(function)
            def inner(*args: Any, **kwargs: Any) -> Any:
                result = function(*args, **kwargs)
                return f"{result}"

            return inner

    @dataclass
    class PrintColorizeIndent:
        indent: int = 0
        begin: str = ""
        end: str = ""
        style: str = "variable"

        def __call__(self, function: Callable) -> Any:
            @Decorators.Print(color=False)
            @Decorators.Colorize(style=self.style)
            @Decorators.Indent(interval=self.indent)
            @wraps(function)
            def inner(*args: Any, **kwargs: Any) -> Any:
                result = function(*args, **kwargs)
                return f"{result}"

            return inner

    @dataclass
    class ColorizedFiglet:
        """Decorator to apply color and figlet formatting to text."""
        style: str = "info"
        font: str = "slant"

        def __call__(self, function):
            @Decorators.Colorize(style=self.style)
            @Decorators.Figletize(font=self.font)
            @wraps(function)
            def inner(*args, **kwargs):
                result = function(*args, **kwargs)
                return result

            return inner

    @dataclass
    class PrintColorizedFiglet:
        """Decorator to print colorized and figlet formatted text."""
        color: bool = True
        end: str = "\n"
        style: str = "info"
        font: str = "slant"

        def __call__(self, function):
            @Decorators.Print(color=False, end=self.end)
            @Decorators.Colorize(style=self.style)
            @Decorators.Figletize(font=self.font)
            @wraps(function)
            def inner(*args, **kwargs):
                result = function(*args, **kwargs)
                return result

            return inner

if __name__ == '__main__':
    # Example usage of the decorators

    @Decorators.PrintColorizedFiglet(style="info", font="slant")
    def display_message(message: str) -> str:
        return message

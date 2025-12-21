# src/ota_installer/decorators/styled_indent_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from ..types.decorators import GenericDecorator

type R = str


@dataclass
class StylizedIndentPrinter(GenericDecorator):
    style: str = "variable"
    indent: int = 0
    begin: str = ""
    end: str = ""
    use_output: bool = False

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        from . import Colorizer, IndentWrapper
        from .output_printer import OutputPrinter

        decorated = IndentWrapper(interval=self.indent)(function)  # type: ignore[reportArgumentType]
        decorated = Colorizer(style=self.style)(decorated)

        if self.use_output:
            decorated = OutputPrinter(suffix=self.end)(decorated)

        wrapped_fn = wraps(function)(decorated)
        return cast(Callable[P, R], wrapped_fn)

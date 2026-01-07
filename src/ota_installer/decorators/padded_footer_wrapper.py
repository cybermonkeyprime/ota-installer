# src/ota_installer/decorators/padded_footer_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import GenericDecorator


@dataclass
class PaddedFooterWrapper(GenericDecorator):
    padding: str = field(default="")

    from . import Colorizer
    from .indent_wrapper import IndentWrapper
    from .output_printer import OutputPrinter

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            self.padding_output()
            return result

        return cast(Callable[P, R], wrapper)

    @OutputPrinter(use_color=True)
    @Colorizer(style="variable")
    @IndentWrapper(interval=1)  # type: ignore[return-value]
    def padding_output(self) -> object:
        return f"{self.padding}"

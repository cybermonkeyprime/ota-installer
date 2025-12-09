# src/decorators/double_padded_footer_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import cast

# from src.logger import logger
from src.types.decorators import GenericDecorator


@dataclass
class DoublePaddedFooterWrapper(GenericDecorator):
    beginning: str = field(default="")
    message: str = field(default="Finished!")
    ending: str = field(default="")

    from . import Colorizer
    from .indent_wrapper import IndentWrapper
    from .output_printer import OutputPrinter

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            self.string_output(self.beginning)
            # logger.info(self.message)
            self.string_output(self.message)
            self.string_output(self.ending)
            return result

        return cast(Callable[P, R], wrapper)

    @OutputPrinter(use_color=False)
    @Colorizer(style="variable")
    @IndentWrapper(interval=1)
    def string_output(self, message: str) -> str:
        return f"{message}"


if __name__ == "__main__":
    pass

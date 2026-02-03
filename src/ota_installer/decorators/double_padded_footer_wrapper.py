# src/ota_installer/decorators/double_padded_footer_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps

from dependency_injector import containers, providers

from ..log_setup import logger
from .protocols.decorator_protocols import GenericDecorator


@dataclass
class DoublePaddedFooterWrapper(GenericDecorator):
    """
    Decorator that adds a double padded footer to the output of a function.
    """

    beginning: str = field(default="")
    message: str = field(default="Finished!")
    ending: str = field(default="")

    class Container(containers.DeclarativeContainer):
        from . import Colorizer
        from .indent_wrapper import IndentWrapper
        from .output_printer import OutputPrinter

        colorizer = providers.Factory(Colorizer, style="variable")
        indent_wrapper = providers.Factory(IndentWrapper, interval=1)
        output_printer = providers.Factory(OutputPrinter, use_color=False)

    def __call__(self, function: Callable) -> Callable:
        """Wraps the function to add a double padded footer."""

        @wraps(function)
        def wrapper(*args, **kwargs) -> object:
            result = function(*args, **kwargs)
            self._output_footer(self.beginning)
            logger.debug(self.message)
            self._output_footer(self.message)
            self._output_footer(self.ending)
            return result

        return wrapper

    @Container.output_printer()
    @Container.colorizer()
    @Container.indent_wrapper()
    def _output_footer(self, message: str) -> str:
        """Outputs the footer messages."""
        return f"{message}"


if __name__ == "__main__":
    pass

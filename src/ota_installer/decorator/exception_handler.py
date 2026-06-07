# src/ota_installer/decorators/exception_handler.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from .protocol.decorator_protocols import GenericDecorator


@dataclass
class ExceptionHandler(GenericDecorator):
    """Decorator to handle exceptions in a function and log them."""

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to catch and log exceptions."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> object | None:
            """
            Wrapper function that executes the original function and logs
            exceptions.
            """
            from ..log_setup import logger

            result = None
            if func:
                try:
                    result = func(*args, **kwargs)
                except Exception as err:
                    logger.exception(
                        f"{type(err).__name__} occured in {func.__name__}"
                    )
            return result

        return wrapper

# src/ota_installer/decorators/exception_handler.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from .protocols.decorator_protocols import GenericDecorator


@dataclass
class ExceptionHandler(GenericDecorator):
    """Decorator to handle exceptions in a function and log them."""

    def __call__(self, function: Callable) -> Callable:
        """Wraps the function to catch and log exceptions."""

        @wraps(function)
        def wrapper(*args, **kwargs) -> object | None:
            """
            Wrapper function that executes the original function and logs
            exceptions.
            """
            from ..log_setup import logger

            try:
                return function(*args, **kwargs)
            except Exception as err:
                logger.exception(
                    f"{type(err).__name__} occured in {function.__name__}"
                )
            return None

        return wrapper


# Signed off by Brian Sanford on 20260213

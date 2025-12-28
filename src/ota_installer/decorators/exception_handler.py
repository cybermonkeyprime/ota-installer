# src/ota_installer/decorators/exception_handler.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from ..protocols.decorator_protocols import GenericDecorator


@dataclass
class ExceptionHandler(GenericDecorator):
    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            from ..log_setup import logger

            try:
                return function(*args, **kwargs)
            except Exception as err:
                logger.exception(
                    f"{type(err).__name__} occured in {function.__name__}"
                )
            return None

        return cast(Callable[P, R], wrapper)

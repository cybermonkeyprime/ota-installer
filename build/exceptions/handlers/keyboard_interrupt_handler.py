from dataclasses import dataclass

from .exception_handler_factory import exception_handler_factory
from .base_exception_handler import BaseExceptionHandler


@exception_handler_factory(KeyboardInterrupt)
@dataclass
class KeyboardInterruptHandler(BaseExceptionHandler):
    default_message: str = "Keyboard interrupt detected, quitting!"

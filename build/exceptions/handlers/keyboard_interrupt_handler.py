from dataclasses import dataclass

from build.exceptions.handlers import exception_handler_factory
from build.exceptions.handlers import BaseExceptionHandler


@exception_handler_factory(KeyboardInterrupt)
@dataclass
class KeyboardInterruptHandler(BaseExceptionHandler):
    default_message: str = "Keyboard interrupt detected, quitting!"

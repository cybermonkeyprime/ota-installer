# src/ota_installer/exceptions/handlers/keyboard_interrupt_handler.py
from dataclasses import dataclass

from .base_exception_handler import BaseExceptionHandler
from .exception_handler_factory import exception_handler_factory


@exception_handler_factory(KeyboardInterrupt)
@dataclass
class KeyboardInterruptHandler(BaseExceptionHandler):
    default_message: str = "Keyboard interrupt detected, quitting!"

# src/ota_installer/exceptions/handlers/keyboard_interrupt_info.py
from dataclasses import dataclass

from .base_exception_info import BaseExceptionHandler
from .exception_factory_info import exception_handler_factory


@exception_handler_factory(KeyboardInterrupt)
@dataclass
class KeyboardInterruptHandler(BaseExceptionHandler):
    """Handles KeyboardInterrupt exceptions."""

    default_message: str = "Keyboard interrupt detected, quitting!"


# Signed off by Brian Sanford on 20260611

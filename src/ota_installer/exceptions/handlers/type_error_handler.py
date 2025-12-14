# src/ota_installer/exceptions/handlers/type_error_handler.py
from dataclasses import dataclass

from .base_exception_handler import BaseExceptionHandler
from .exception_handler_factory import exception_handler_factory


@exception_handler_factory(TypeError)
@dataclass
class TypeErrorHandler(BaseExceptionHandler):
    default_message: str = "Type error occurred, quitting!"

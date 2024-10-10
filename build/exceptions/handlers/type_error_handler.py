from dataclasses import dataclass

from .exception_handler_factory import exception_handler_factory
from .base_exception_handler import BaseExceptionHandler


@exception_handler_factory(TypeError)
@dataclass
class TypeErrorHandler(BaseExceptionHandler):
    default_message: str = "Type error occurred, quitting!"

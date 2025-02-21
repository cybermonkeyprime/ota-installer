from dataclasses import dataclass

from build.exceptions.handlers import exception_handler_factory
from build.exceptions.handlers import BaseExceptionHandler


@exception_handler_factory(TypeError)
@dataclass
class TypeErrorHandler(BaseExceptionHandler):
    default_message: str = "Type error occurred, quitting!"

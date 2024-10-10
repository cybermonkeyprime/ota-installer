from dataclasses import dataclass

from .exception_handler_factory import exception_handler_factory
from .base_exception_handler import BaseExceptionHandler


@exception_handler_factory(FileNotFoundError)
@dataclass
class FileNotFoundExceptionHandler(BaseExceptionHandler):
    default_message: str = "File not found, quitting!"

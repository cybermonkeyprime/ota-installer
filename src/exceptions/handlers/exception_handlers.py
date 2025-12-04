# src/exceptions/handlers/exception_handlers.py
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar

from src.decorators import Colorizer, IndentWrapper, OutputPrinter

T = TypeVar("T")


@dataclass
class BaseExceptionHandler(object):
    func: Callable
    exception_type: type[BaseException] = field(default=BaseException)
    default_message: str = field(default="An error occurred")
    custom_messages: dict[type[BaseException], str] = field(
        default_factory=dict
    )

    def handle(self, *args: T, **kwargs: T) -> T | None:
        try:
            return self.func(*args, **kwargs)
        except self.exception_type as err:
            self.print_exception_message(err)
            return None

    @OutputPrinter(use_color=True, prefix="\n\n", suffix="\n\n")
    def print_exception_message(self, error: BaseException) -> None:
        formatted_message = self.format_message(error)
        return formatted_message

    @IndentWrapper(interval=1)
    @Colorizer(style="variable")
    def format_message(self, error: BaseException) -> str:
        error_message = self.custom_messages.get(
            type(error), self.default_message
        )
        return f"{error_message}"

    def __call__(self, *args: T, **kwargs: T) -> T | None:
        return self.handle(*args, **kwargs)


def exception_handler_factory(*exception_types: type[BaseException]):
    def decorator(
        cls: type[BaseExceptionHandler],
    ) -> type[BaseExceptionHandler]:
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.exception_type = (
                exception_types
                if len(exception_types) > 1
                else exception_types[0]
            )
            self.custom_messages.update(
                {ex: self.default_message for ex in exception_types}
            )

        cls.__init__ = __init__
        return cls

    return decorator


@exception_handler_factory(TypeError)
@dataclass
class TypeErrorHandler(BaseExceptionHandler):
    default_message: str = "Type error occurred, quitting!"


@exception_handler_factory(KeyboardInterrupt)
@dataclass
class KeyboardInterruptHandler(BaseExceptionHandler):
    default_message: str = "Keyboard interrupt detected, quitting!"


@exception_handler_factory(FileNotFoundError)
@dataclass
class FileNotFoundExceptionHandler(BaseExceptionHandler):
    default_message: str = "File not found, quitting!"

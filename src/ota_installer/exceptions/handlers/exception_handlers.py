# src/ota_installer/exceptions/handlers/exception_handlers.py
from dataclasses import dataclass

from .base_exception_handler import BaseExceptionHandler


def exception_handler_factory(*exception_types: type[BaseException]):
    def decorator(
        cls: type[BaseExceptionHandler],
    ) -> type[BaseExceptionHandler]:
        original_init = cls.__init__

        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.exception_type = (
                exception_types if len(exception_types) > 1 else ""
            )
            self.custom_messages.update(
                {ex: self.default_message for ex in exception_types}
            )

        cls.__init__ = __init__
        return cls

    return decorator


@exception_handler_factory(KeyboardInterrupt)
@dataclass
class KeyboardInterruptHandler(BaseExceptionHandler):
    default_message: str = "Keyboard interrupt detected, quitting!"

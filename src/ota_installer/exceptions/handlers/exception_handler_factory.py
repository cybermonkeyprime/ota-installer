# src/ota_installer/exceptions/handlers/exception_handler_factory.py
from collections.abc import Callable

from .base_exception_handler import BaseExceptionHandler


def exception_handler_factory(
    *exception_types: type[BaseException],
) -> Callable[...]:
    def decorator(
        handler_class: type[BaseExceptionHandler],
    ) -> type[BaseExceptionHandler]:
        """
        Factory to create exception handlers for specified exception types.
        """
        original_init = handler_class.__init__

        def __init__(self: BaseExceptionHandler, *args, **kwargs) -> None:
            """
            Initialize the exception handler with specified exception types.
            """
            original_init(self, *args, **kwargs)

            self.exception_types = exception_types
            self.custom_messages = {
                ex: self.default_message for ex in exception_types
            }

            handler_class.__init__ = __init__

        return handler_class

    return decorator


def main():
    """Main entry point of the application."""
    pass


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260129

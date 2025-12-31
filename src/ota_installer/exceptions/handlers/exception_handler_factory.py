# src/ota_installer/exceptions/handlers/exception_handler_factory.py
from collections.abc import Callable
from dataclasses import dataclass, field

from .base_exception_handler import BaseExceptionHandler


def exception_handler_factory(
    *exception_types: type[BaseException],
) -> Callable[...]:
    def decorator(
        handler_class: type[BaseExceptionHandler],
    ) -> type[BaseExceptionHandler]:
        original_init = handler_class.__init__

        def __init__[**P](
            self: BaseExceptionHandler, *args: P.args, **kwargs: P.kwargs
        ) -> None:
            original_init(self, *args, **kwargs)
            self.exception_types = exception_types
            self.custom_messages = {
                ex: self.default_message for ex in exception_types
            }

            handler_class.__init__ = __init__

        return handler_class

    return decorator


@dataclass
class ExceptionHandler(object):
    default_message: str = "An error occurred"
    custom_messages: dict[type[BaseException], str] = field(
        default_factory=dict
    )


if __name__ == "__main__":

    @exception_handler_factory(ValueError, KeyError)
    class CustomExceptionHandler(BaseExceptionHandler):
        pass

    handler = CustomExceptionHandler()
    print(handler.custom_messages)

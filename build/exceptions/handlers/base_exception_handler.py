from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Type

from build.decorators import Indent, Colorizer, Printer


@dataclass
class BaseExceptionHandler(object):
    function: Callable
    exception_type: Type[BaseException] = field(default=BaseException)
    default_message: str = field(default="An error occurred")
    custom_messages: Dict[Type[BaseException], str] = field(default_factory=dict)

    def handle(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return self.function(*args, **kwargs)
        except self.exception_type as err:
            self.print_exception_message(err)
            return None

    @Printer(use_color=True, prefix="\n\n", suffix="\n\n")
    def print_exception_message(self, error: BaseException) -> None:
        formatted_message = self.format_message(error)
        return formatted_message

    @Indent(interval=1)
    @Colorizer(style="variable")
    def format_message(self, error: BaseException) -> str:
        error_message = self.custom_messages.get(type(error), self.default_message)
        return f"{error_message}"

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.handle(*args, **kwargs)


if __name__ == "__main__":
    pass

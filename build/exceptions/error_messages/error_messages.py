from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any
from build.styles.palette import Colors


class ErrorMessageTemplate(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


@dataclass
class CustomMessage(ErrorMessageTemplate):
    error: BaseException = field(default_factory=BaseException)

    def __str__(self) -> str:
        return f"Uh oh something broke!: {self.error}"


@dataclass
class ErrorMessage(ErrorMessageTemplate):
    error: BaseException = field(default_factory=BaseException)

    def __str__(self) -> str:
        return f"An error occurred: {self.error}"


@dataclass
class MessageWithTitleAndValue(ErrorMessageTemplate):
    title: str = field(default="")
    value: Any = field(default=None)
    error: BaseException = field(default_factory=BaseException)

    def __str__(self) -> str:
        return f'{Colors.error}Error processing {self.title.title()} "{self.value}": {self.error}'


@dataclass
class ActionMessage(ErrorMessageTemplate):
    action: str = field(default="doing something")
    title: str = field(default="")
    value: Any = field(default=None)
    error: BaseException = field(default_factory=BaseException)

    def set_value(self):
        if self.value is None:
            self.value = ""
        return self.value

    def __str__(self) -> str:
        return f"Error {self.action} {self.title}: {self.set_value()}"

from abc import ABC, abstractmethod
from subprocess import run

from build import decorators


class TaskFactoryTemplate(ABC):
    comment_string: str = ""

    @property
    @abstractmethod
    def index(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def title(self) -> str:
        raise NotImplementedError()

    @property
    @abstractmethod
    def command_string(self) -> str:
        raise NotImplementedError()

    @decorators.DoublePaddedFooterWrapper(message="Completed")
    def perform_task(self) -> None:
        self.index_and_title()
        self.return_command_string()
        self.execute_command_string()
        if self.comment_string:
            self.after_comment()

    @decorators.ColorizedIndentPrinter(indent=1, end=":", style="warning")
    def index_and_title(self) -> str:
        return f"{self.index}. {self.title}: "

    @decorators.FooterWrapper()
    @decorators.ColorizedIndentPrinter(indent=3, end="", style="default")
    def return_command_string(self) -> str:
        return self.command_string

    @decorators.ConfirmationPrompt(comment="execute the command", indent=2, char=" ")
    @decorators.ContinueOnKeyPress(indent=2, char=" ")
    @decorators.Encapsulate()
    def execute_command_string(self) -> None:
        run([self.command_string], shell=True)

    @decorators.ColorizedIndentPrinter(indent=2, begin="", end="", style="warning")
    def after_comment(self) -> str:
        return f"{self.comment_string}"

from dataclasses import field
from abc import ABC, abstractmethod
from subprocess import run
from typing import Optional

from build import decorators


class TaskFactoryTemplate(ABC):
    """
    An abstract base class representing a generic task.

    Attributes:
        comment: An optional comment string to be printed after the task.
    """
    comment: Optional[str] = field(default=None)

    @property
    @abstractmethod
    def index(self) -> int:
        """Returns the index of the task."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def title(self) -> str:
        """Returns the title of the task."""
        raise NotImplementedError()

    @property
    @abstractmethod
    def command_string(self) -> str:
        """Returns the command string to be executed."""
        raise NotImplementedError()

    @decorators.DoublePaddedFooterWrapper(message="Completed")
    def perform_task(self) -> None:
        """Performs the task by executing the associated command."""
        self.index_and_title()
        self.return_command_string()
        self.execute_command_string()
        if self.comment:
            self.after_comment()

    @decorators.ColorizedIndentPrinter(indent=1, end=":", style="warning")
    def index_and_title(self) -> str:
        """Returns the index and title of the task."""
        return f"{self.index}. {self.title}: "

    @decorators.FooterWrapper()
    @decorators.ColorizedIndentPrinter(indent=3, end="", style="default")
    def return_command_string(self) -> str:
        """Returns the command string of the task."""
        return self.command_string

    @decorators.ConfirmationPrompt(comment="execute the command", indent=2, char=" ")
    @decorators.ContinueOnKeyPress(indent=2, char=" ")
    @decorators.Encapsulate()
    def execute_command_string(self) -> None:
        """Executes the command string of the task."""
        try:
            run([self.command_string], shell=True)
        except Exception as e:
            print(f"An error occurred while executing the command: {e}")


    @decorators.ColorizedIndentPrinter(indent=2, begin="", end="", style="warning")
    def after_comment(self) -> str:
        """Returns the comment associated with the task."""
        return f"{self.comment}"

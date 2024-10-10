from abc import abstractmethod
from subprocess import run

from build import decorators

from re import sub


class TaskFactoryTemplate:
    _index: int = 0
    _title: str = ""
    _command_string: str = ""
    _comment: str = ""

    @abstractmethod
    def __post_init__(self) -> None:
        raise NotImplementedError()

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, integer: int) -> None:
        self._index = integer

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, name: str) -> None:
        self._title = name

    @property
    def command_string(self) -> str:
        return self._command_string

    @command_string.setter
    def command_string(self, name: str) -> None:
        self._command_string = name

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, name: str) -> None:
        self._comment = name

    @decorators.DoublePaddedFooterWrapper(message="Finished")
    def perform_task(self) -> None:
        self.index_and_title()
        self.return_command_string()
        self.execute_command_string()
        if self.comment:
            self.after_comment()

    @decorators.ColorizedIndentPrinter(indent=1, end=":", style="task")
    def index_and_title(self) -> str:
        return f"{self.index}. {self.title}:"

    @decorators.FooterWrapper()
    @decorators.ColorizedIndentPrinter(indent=3, end="", style="non_error")
    def return_command_string(self) -> str:
        return self.command_string

    @decorators.ConfirmationPrompt(comment="execute the command", indent=2, char=" ")
    @decorators.ContinueOnKeyPress(indent=1, char=" ")
    @decorators.Encapsulate()
    def execute_command_string(self) -> None:
        run([self.command_string], shell=True, check=False)

    @decorators.ColorizedIndentPrinter(indent=2, begin="", end="", style="task")
    def after_comment(self) -> str:
        return f"{self.comment}"

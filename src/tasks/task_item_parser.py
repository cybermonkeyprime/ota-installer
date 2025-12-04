# src/tasks/task_item_parser.py
from dataclasses import dataclass

from src import decorators


@dataclass
class TaskItemParser(object):
    value: str

    @decorators.ColorizedIndentPrinter(
        indent=2, begin="", end="", style="task"
    )
    def show_aspect(self) -> str:
        return f"{self.value}"

    @decorators.ColorizedIndentPrinter(indent=1, end=":", style="task")
    def show_header(self) -> str:
        return f"{self.value}"

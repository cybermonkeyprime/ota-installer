# src/tasks/task_operation_processor.py
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Self

from dispatchers import DispatcherInterface
from src import decorators

from . import (
    CommandStringConstants,
    DescriptionConstants,
    ExecutorConstants,
    ReminderConstants,
    TaskOperationExecutor,
    TaskOpsConstants,
    TaskOpsItemTypeConstants,
)


@dataclass
class TaskOperationProcessor(object):
    index: int = field(init=False)
    title: str = field(init=False)
    description: str = field(init=False)
    comment: str = field(init=False)
    reminder: str = field(init=False)
    command_string: str = field(init=False)

    def set_item(self, field_name: str, value: object) -> Self:
        try:
            enum_member = TaskOpsItemTypeConstants[field_name.upper()]
        except KeyError:
            raise AttributeError(
                f"'{field_name}' is not a valid task field."
            ) from None

        expected_type = enum_member.value
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Expected value of type "
                f"{expected_type.__name__} for '{field_name}', "
                f"but got {type(value).__name__} instead."
            )

        setattr(self, field_name.lower(), value)
        return self

    def get_item(self, field_name: str) -> object:
        try:
            TaskOpsItemTypeConstants[field_name.upper()]
        except KeyError:
            raise AttributeError(
                f"'{field_name}' is not a valid task field."
            ) from None

        return getattr(self, field_name.lower(), None)

    def show_index_and_title(self) -> str:
        return TaskAspectParser(f"{self.index}. {self.title}:").show_header()

    @decorators.FooterWrapper()
    @decorators.ColorizedIndentPrinter(indent=3, end="", style="warning")
    def show_description(self) -> str:
        return self.description

    @decorators.FooterWrapper()
    @decorators.ColorizedIndentPrinter(
        indent=CommandStringConstants.INDENT.value,
        end="",
        style=CommandStringConstants.STYLE.value,
    )
    def show_command_string(self) -> str:
        return self.command_string

    def show_comment(self) -> str:
        return TaskAspectParser(self.comment).show_aspect()

    def show_reminder(self) -> str:
        return TaskAspectParser(self.reminder).show_aspect()

    def execute_command_string(self) -> None:
        TaskOperationExecutor(self.command_string).execute()
        if getattr(self, "reminder", None):
            self.show_reminder()

    def execute_and_return_output(self, output_name) -> str:
        return TaskOperationExecutor(
            self.command_string
        ).execute_and_return_output(output_name)

    @decorators.MultiplyString(
        interval=(
            TaskOpsConstants.SPACING.value * TaskOpsConstants.INTERVAL.value
        )
    )
    def get_indentation(self) -> str:
        return " "

    def run_with_output(self) -> None:
        self.show_index_and_title()

        if getattr(self, "description", None):
            self.show_description()

        self.show_command_string()

        self.execute_command_string()


def image_handler(key: str) -> Path:
    try:
        dispatcher = DispatcherInterface("image")
        retriever = dispatcher.get_dispatcher()
        # return retriever.get_key(key)
        return Path.home() / "images" / f"{retriever.get_key(key)}.img"
    except KeyError as e:
        raise ValueError(f"Invalid key for image handler: {key}") from e


@dataclass
class TaskAspectParser(object):
    value: str

    @decorators.ColorizedIndentPrinter(
        indent=2, begin="", end="", style="task"
    )
    def show_aspect(self) -> str:
        return f"{self.value}"

    @decorators.ColorizedIndentPrinter(indent=1, end=":", style="task")
    def show_header(self) -> str:
        return f"{self.value}:"


def main():
    pass


if __name__ == "__main__":
    main()

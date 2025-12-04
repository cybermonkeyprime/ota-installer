# src/tasks/task_operation_processor.py
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from dispatchers import DispatcherInterface
from src import decorators

from .task_item_parser import TaskItemParser
from .task_operation_constants import (
    CommandStringConstants,
    DescriptionConstants,
    TaskOpsConstants,
    TaskOpsItemTypeConstants,
)
from .task_operation_executor import (
    TaskOperationExecutor,
)


@dataclass
class TaskOperationProcessor(object):
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
        return TaskItemParser(
            f"{self.get_item('index')}. {self.get_item('title')}:"
        ).show_header()

    @decorators.FooterWrapper()
    @decorators.ColorizedIndentPrinter(
        indent=DescriptionConstants.INDENT.value,
        end="",
        style=DescriptionConstants.STYLE.value,
    )
    def show_description(self) -> str:
        item = str(self.get_item("description"))
        return item

    @decorators.FooterWrapper()
    @decorators.ColorizedIndentPrinter(
        indent=CommandStringConstants.INDENT.value,
        end="",
        style=CommandStringConstants.STYLE.value,
    )
    def show_command_string(self) -> str:
        item = self.get_item("command_string")
        return str(item)

    def show_comment(self) -> str:
        item = str(self.get_item("comment"))
        return TaskItemParser(item).show_aspect()

    def show_reminder(self) -> str:
        item = str(self.get_item("reminder"))
        padded = f"👉 REMINDER: {item}"
        return TaskItemParser(padded).show_aspect()

    def execute_command_string(self) -> None:
        item = self.get_item("command_string")
        TaskOperationExecutor(str(item)).execute()
        if self.get_item("reminder"):
            self.show_reminder()

    def execute_and_return_output(self, output_name) -> str:
        item = str(self.get_item("command_string"))
        return TaskOperationExecutor(item).execute_and_return_output(
            output_name
        )

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
        return Path.home() / "images" / f"{retriever.get_key(key)}.img"
    except KeyError as e:
        raise ValueError(f"Invalid key for image handler: {key}") from e


def main():
    pass


if __name__ == "__main__":
    main()

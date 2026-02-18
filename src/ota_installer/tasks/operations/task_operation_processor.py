# src/ota_installer/tasks/operations/task_operation_processor.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from loguru import logger

from ... import decorators
from ...dispatchers.factories.plugin_dispatcher_adapter import (
    PluginDispatcherAdapter,
)
from .constants.constants import (
    CommandStringConstants,
    TaskOpsConstants,
)
from .constants.task_ops_item_types import TaskOpsItemTypes
from .task_item_parser import TaskItemParser
from .task_operation_executor import TaskOperationExecutor


@dataclass
class TaskOperationProcessor(object):
    index: int = field(init=False)
    title: str = field(init=False)
    description: str = field(init=False)
    comment: str = field(init=False)
    reminder: str = field(init=False)
    command_string: str = field(init=False)

    def set_item(self, field_name: str, value: object) -> Self:
        """Sets the value of a task field."""
        expected_type = TaskOpsItemTypes.get_validated_type(field_name)
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Expected value of type {expected_type.__name__} for "
                f"'{field_name}', but got {type(value).__name__} instead."
            )
        setattr(self, field_name.lower(), value)
        return self

    def get_item(self, field_name: str) -> object:
        """Retrieves the value of a task field."""
        TaskOpsItemTypes.get_validated_type(field_name)
        return getattr(self, field_name.lower(), None)

    def show_index_and_title(self) -> str:
        """Displays the index and title of the task."""
        return TaskItemParser(f"{self.index}. {self.title}:").show_header()

    @decorators.FooterWrapper()
    @decorators.ColorizedIndentPrinter(indent=3, end="", style="warning")
    def show_description(self) -> str:
        """Displays the description of the task."""
        return self.description

    @decorators.FooterWrapper()
    @decorators.ColorizedIndentPrinter(
        indent=CommandStringConstants.INDENT.value,
        end="",
        style=CommandStringConstants.STYLE.value,
    )
    def show_command_string(self) -> str:
        """Displays the command string of the task."""
        return self.command_string

    def show_comment(self) -> str:
        """Displays the comment of the task."""
        return TaskItemParser(self.comment).show_aspect()

    def show_reminder(self) -> str:
        """Displays the reminder of the task."""
        return TaskItemParser(self.reminder).show_aspect()

    def execute_command_string(self) -> None:
        """Executes the command string associated with the task."""
        TaskOperationExecutor(self.command_string).execute()
        if getattr(self, "reminder", None):
            self.show_reminder()

    def execute_and_return_output(self, output_name) -> str:
        """Executes the command string and returns the output."""
        return (
            TaskOperationExecutor(
                self.command_string
            ).execute_and_return_output(output_name)
            or "No output"
        )

    @decorators.MultiplyString(
        interval=(
            TaskOpsConstants.SPACING.value * TaskOpsConstants.INTERVAL.value
        )
    )
    def run_with_output(self) -> None:
        """Runs the task and displays its output."""
        self.show_index_and_title()
        if getattr(self, "description", None):
            self.show_description()
        self.show_command_string()
        self.execute_command_string()


def image_handler(key: str) -> Path:
    """Handles image retrieval based on a key."""
    logger.debug(f"image_handler(): {key=}")
    try:
        dispatcher = PluginDispatcherAdapter("image")
        logger.debug(f"image_handler(): {dispatcher=}")
        retriever = dispatcher.load()
        logger.debug(f"image_handler(): {retriever=}")
        return Path.home() / "images" / f"{retriever.get_key(key)}.img"  # type: ignore[return-value]
    except KeyError as e:
        raise ValueError(f"Invalid key for image handler: {key}") from e


def main():
    """Main entry point of the application."""
    pass


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260213

# src/ota_installer/task/task_pipeline.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ..task_group.task_group_director import TaskGroupDirector
from .task_directors import DispatcherDirector, TaskDirector
from .task_manager import TaskManager


@dataclass(frozen=True, slots=True)
class CLIArguments:
    """Represents command-line arguments for the application."""

    path: Path
    task_group: str | None = None
    list: bool = False
    version: bool = False


@dataclass(slots=True)
class TaskPipeline:
    arguments: CLIArguments
    task_manager: TaskManager = field(default_factory=lambda: TaskManager())

    dispatcher_director: DispatcherDirector = field(
        default_factory=DispatcherDirector
    )
    task_director: TaskDirector = field(init=False)
    task_group_director: TaskGroupDirector = field(init=False)

    path: Path = field(init=False)

    def __post_init__(self) -> None:
        self.task_director = TaskDirector(
            task_manager=self.task_manager,
            dispatcher=self.dispatcher_director,
        )

        self.task_group_director = TaskGroupDirector(
            task_director=self.task_director,
            dispatcher=self.dispatcher_director,
            task_group=self.arguments.task_group,
        )

    def set_path(self) -> Self:
        """Sets the path from CLI arguments."""
        self.path = self.arguments.path
        return self

    def initialize_task_manager(self) -> Self:
        """Initializes the task manager with the specified path."""
        (
            self.task_manager.set_file_name(self.path)
            .set_variable()
            .log_and_process_variables()
        )
        return self

    def execute(self) -> None:
        self.task_group_director.execute()


def main() -> None:
    """Main entry point for the task executor."""
    pass


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260831

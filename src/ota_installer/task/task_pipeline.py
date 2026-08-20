from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ..log_setup import logger
from ..task.task_group_info import TaskGroupName
from .task_manager import TaskManager


@dataclass(frozen=True, slots=True)
class CLIArguments:
    """Represents command-line arguments for the application."""

    path: Path
    task_group: str | None = None
    list: bool = False
    version = False


@dataclass(slots=True)
class DispatcherDirector:
    dispatcher: object = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the task dispatcher."""

        from ..dispatcher.dispatcher_info import DispatcherType
        from ..plugin.handler.dispatcher_plugin_handler import (
            PluginDispatcherAdapter,
        )

        self.dispatcher: object = PluginDispatcherAdapter(
            DispatcherType.TASK_GROUP.value, TaskGroupName.fetch_mapping()
        ).load()

    def get_instance(self, key: str):
        """Retrieves the dispatcher instance for a given key."""
        logger.debug(f"Retrieving dispatcher instance for key: {key}")
        return self.dispatcher.get_instance(key)

    def contains(self, key: str):
        """Checks if the task group is in the dispatcher collection."""
        return key in self.dispatcher.collection


@dataclass(frozen=True, slots=True)
class TaskGroupDirector:
    task_director: TaskDirector
    dispatcher: DispatcherDirector
    task_group: str | None = None

    @property
    def valid_group(self) -> bool:
        """Validates task group rules."""
        return bool(self.task_group) and self.dispatcher.contains(
            self.task_group
        )

    def execute(self) -> None:
        """Executes tasks based on the task group rules."""
        if self.valid_group:
            self.execute_single()
        else:
            self.execute_all()

    def execute_single(self) -> None:
        """Executes a single task if a task group is defined."""

        if not self.task_group:
            raise AttributeError(f"{self.task_group!r} does not exist!")

        logger.debug(
            f"Executing single task for task group: {self.task_group}"
        )
        self.task_director.execute(self.task_group)

    def execute_all(self) -> None:
        """Executes all tasks defined in the task group keys."""
        for task_group_key in TaskGroupName.get_task_group_members():
            self.task_director.execute(task_group_key)


@dataclass(frozen=True, slots=True)
class TaskDirector:
    task_manager: TaskManager
    dispatcher: DispatcherDirector

    def execute(self, task_group_key: str) -> None:
        from .task_manager import Pipeline

        """Iterates over tasks in the specified task group."""
        logger.debug(f"Executing task iteration for: {task_group_key}")
        stages = self.dispatcher.get_instance(key=task_group_key)
        pipeline = Pipeline(stages=stages)
        self.task_manager.execute_iteration(pipeline=pipeline)


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

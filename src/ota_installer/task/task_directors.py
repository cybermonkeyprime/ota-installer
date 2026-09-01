# src/ota_installer/task/task_directors.py
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import cast

from ..log_setup import logger
from ..task_group.task_group_dispatcher import TaskGroupTypeDispatcher
from ..task_group.task_group_names import TaskGroupName
from .task_manager import TaskManager


@dataclass(slots=True)
class DispatcherDirector:
    dispatcher: TaskGroupTypeDispatcher = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the task dispatcher."""

        from ..dispatcher.dispatcher_type import DispatcherType
        from ..plugin.plugin_dispatcher_adapter import (
            PluginDispatcherAdapter,
        )

        self.dispatcher = cast(
            TaskGroupTypeDispatcher,
            PluginDispatcherAdapter(
                DispatcherType.TASK_GROUP.value, TaskGroupName.fetch_mapping()
            ).load(),
        )
        logger.debug(f"dispatcher type: {type(self.dispatcher)!r}")

    def get_instance(self, key: str) -> Callable:
        """Retrieves the dispatcher instance for a given key."""
        logger.debug(f"Retrieving dispatcher instance for key: {key}")
        return self.dispatcher.get_instance(key)

    def contains(self, key: str):
        """Checks if the task group is in the dispatcher collection."""
        return key in self.dispatcher.collection


@dataclass(frozen=True, slots=True)
class TaskDirector:
    task_manager: TaskManager
    dispatcher: DispatcherDirector

    def execute(self, task_group_key: str) -> None:
        from .task_manager import Pipeline

        """Iterates over tasks in the specified task group."""
        logger.debug(f"Executing task iteration for: {task_group_key}")
        stages = cast(
            tuple[str, ...] | None,
            self.dispatcher.get_instance(key=task_group_key),
        )
        pipeline = Pipeline(stages=stages)
        self.task_manager.execute_iteration(pipeline=pipeline)


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


# Signed off by Brian Sanford on 20260820

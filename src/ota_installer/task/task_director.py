# src/ota_installer/task/task_directors.py
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import cast

from ..log_setup import logger
from .task_group.task_group_dispatcher import TaskGroupTypeDispatcher
from .task_group.task_group_renderer import TASK_GROUPS
from .task_manager import TaskManager


@dataclass(slots=True)
class TaskInvocation:
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
                DispatcherType.TASK_GROUP.value, TASK_GROUPS
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
    dispatcher: TaskInvocation

    def execute(self, task_group_key: str) -> None:
        """Iterates over tasks in the specified task group."""
        from .task_manager import Pipeline

        logger.debug(f"Executing task iteration for: {task_group_key}")
        stages = cast(
            tuple[str, ...] | None,
            self.dispatcher.get_instance(key=task_group_key),
        )
        pipeline = Pipeline(stages=stages)
        self.task_manager.execute_iteration(pipeline=pipeline)


# Signed off by Brian Sanford on 20260820

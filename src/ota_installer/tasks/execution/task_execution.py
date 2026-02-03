from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ...dispatchers.constants.dispatcher_constants import DispatcherConstants
from ...dispatchers.factories.plugin_dispatcher_adapter import (
    PluginDispatcherAdapter,
)
from ...dispatchers.templates.dispatcher_template import (
    CollectionValues,
    DispatcherTemplate,
)
from ...log_setup import logger
from ...task_groups.constants.task_group_names import TaskGroupNames
from ..definitions.task_definitions import TaskDefinitions
from ..managers.task_manager import TaskManager
from .cli_arguments import CLIArguments


@dataclass
class TaskExecutor(object):
    arguments: CLIArguments
    task_manager: TaskManager = field(default_factory=lambda: TaskManager())
    dispatcher: DispatcherTemplate = field(init=False)
    task_group: str | None = field(init=False)
    task_definitions: TaskDefinitions = field(
        default_factory=lambda: TaskDefinitions()
    )
    path: Path = field(init=False)

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

    def assign_task_group(self) -> Self:
        """Assigns the task group from CLI arguments."""
        if hasattr(self.arguments, "task_group"):
            self.task_group = self.arguments.task_group
        else:
            logger.error("Arguments must have 'task_group' attribute")
        return self

    def initialize_task_dispatcher(self) -> Self:
        """Initializes the task dispatcher."""
        self.dispatcher = PluginDispatcherAdapter(
            DispatcherConstants.TASK_GROUP.value, self.task_definitions
        ).load()
        return self

    def task_group_in_dispatcher_collection(self):
        """Checks if the task group is in the dispatcher collection."""
        return self.task_group in self.dispatcher.collection

    @property
    def task_group_rules(self) -> bool:
        """Validates task group rules."""
        return all(
            [self.task_group, self.task_group_in_dispatcher_collection()]
        )

    @property
    def task_group_keys(self) -> tuple:
        """Returns the keys of the task groups."""
        return tuple(enum.value for enum in TaskGroupNames)

    def execute_task_based_on_group(self) -> None:
        """Executes tasks based on the task group rules."""
        if not self.task_group_rules:
            self.execute_all_tasks()
        else:
            self.execute_single_task()

    def get_dispatcher_instance(self, key: str) -> CollectionValues | None:
        """Retrieves the dispatcher instance for a given key."""
        logger.debug(f"Retrieving dispatcher instance for key: {key}")
        return self.dispatcher.get_instance(key)

    def execute_task(self, task_group_key: str) -> None:
        """Executes a specific task based on the task group key."""
        try:
            self.task_iteration(task_group_key)
        except AttributeError as e:
            logger.error(f"Processing {task_group_key} failed: {e}")

    def task_iteration(self, task_group_key: str) -> None:
        """Iterates over tasks in the specified task group."""
        logger.debug(f"Executing task iteration for: {task_group_key}")
        dispatcher_instance = self.get_dispatcher_instance(task_group_key)
        self.task_manager.execute_iteration(task_group=dispatcher_instance)

    def execute_single_task(self) -> None:
        """Executes a single task if a task group is defined."""
        if self.task_group:
            logger.debug(
                f"Executing single task for task group: {self.task_group}"
            )
            self.execute_task(self.task_group)

    def execute_all_tasks(self) -> None:
        """Executes all tasks defined in the task group keys."""
        for task_group_key in self.task_group_keys:
            self.execute_task(task_group_key)


def main() -> None:
    """Main entry point for the task executor."""
    pass


if __name__ == "__main__":
    main()

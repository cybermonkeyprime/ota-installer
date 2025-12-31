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
from ..definitions import TaskDefinitions
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

    def task_group_in_dispatcher_collection(self):
        return self.task_group in self.dispatcher.collection

    @property
    def task_group_rules(self) -> bool:
        return all(
            [self.task_group, self.task_group_in_dispatcher_collection()]
        )

    @property
    def task_group_keys(self) -> tuple:
        return tuple(enum.value for enum in TaskGroupNames)

    def execute_task_based_on_group(self) -> None:
        if not self.task_group_rules:
            self.execute_all_tasks()
        else:
            self.execute_single_task()

    def set_path(self) -> Self:
        self.path = self.arguments.path
        return self

    def initialize_task_manager(self) -> Self:
        (self.task_manager.set_file_name(self.path).set_variable().list_vars())
        return self

    def assign_task_group(self) -> Self:
        try:
            if hasattr(self.arguments, "task_group"):
                self.task_group = self.arguments.task_group
            else:
                raise AttributeError(
                    "Arguments must have 'task_group' attribute"
                )
        except Exception as e:
            logger.error(f"Arguments not processed: {type(e).__name__} {e}")
        return self

    def initialize_task_dispatcher(self) -> Self:
        dispatcher = PluginDispatcherAdapter(
            DispatcherConstants.TASK_GROUP.value, self.task_definitions
        )
        self.dispatcher = dispatcher.load()
        return self

    def get_dispatcher_instance(self, key: str) -> CollectionValues | None:
        logger.debug(f"{key=}")
        return self.dispatcher.get_instance(key)

    def execute_task(self, task_group_key: str) -> None:
        try:
            self.task_iteration(task_group_key)
        except AttributeError as e:
            logger.error(
                f"[{type(e).__name__}] Processing {task_group_key} failed: {e}"
            )

    def task_iteration(self, task_group_key: str) -> None:
        logger.debug(f"{task_group_key=}")
        dispatcher_instance = self.get_dispatcher_instance(task_group_key)
        self.task_manager.execute_iteration(task_group=dispatcher_instance)

    def execute_single_task(self) -> None:
        if self.task_group:
            logger.debug(f"{self.task_group=}")
            self.execute_task(self.task_group)

    def execute_all_tasks(self) -> None:
        {
            self.execute_task(task_group_key)
            for task_group_key in self.task_group_keys
        }


def main() -> None:
    pass


if __name__ == "__main__":
    main()

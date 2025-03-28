from argparse import Namespace
from dataclasses import dataclass, field
from typing import Any

from build.decorators import FooterWrapper
from build.dispatchers import DispatcherTemplate, MainDispatcher
from build.exceptions.handlers import KeyboardInterruptHandler
from build.styles.palette import Colors
from build.tasks.definitions import TaskDefinitions
from build.tasks.managers import TaskManager


@dataclass
class TaskHashes(object):
    task_items: tuple = field(
        default_factory=lambda: ("preparation", "migration", "application")
    )


@KeyboardInterruptHandler
@FooterWrapper(message="Completed Successfully!\n")
@dataclass
class Executor:
    arguments: Namespace = field(default_factory=Namespace)
    task_manager: TaskManager = field(default_factory=TaskManager)
    task_definitions: TaskDefinitions = field(default_factory=TaskDefinitions)

    @property
    def path(self) -> str:
        try:
            self.arguments
        except Exception as e:
            print(f"{e} Arguments must have 'path' attribute")
        assert hasattr(self.arguments, "path"), "Arguments must have 'path' attribute"
        return self.arguments.path

    @property
    def dispatcher(self) -> DispatcherTemplate:
        dispatcher = MainDispatcher("task_group", self.task_definitions)
        return dispatcher.receiver()

    @property
    def task_group(self) -> str | None:
        try:
            if hasattr(self.arguments, "task_group"):
                return self.arguments.task_group
            else:
                raise AttributeError("Arguments must have 'task_group' attribute")
        except Exception as e:
            print(CustomException("arguments", e))

    def __post_init__(self) -> None:
        self.task_manager.initiate_task(self.path)
        self.execute_task_based_on_group()

    def initialize(self) -> None:
        self.task_manager.initiate_task(self.path)
        self.execute_task_based_on_group()

    def execute_task_based_on_group(self) -> None:
        if self.task_group and self.task_group in self.dispatcher.collection:
            self.execute_single_task()
        else:
            self.execute_all_tasks()

    def initialize_task_manager(self) -> None:
        self.task_manager.initiate_task(self.path)

    def get_dispatcher_instance(self, key: str) -> Any:
        return self.dispatcher.get_instance(key)

    def execute_task(self, task_group_key: str) -> None:
        try:
            dispatcher_instance = self.get_dispatcher_instance(task_group_key)
            execution_function = self.task_manager.iteration.execute_iteration
            execution_function(task_group=dispatcher_instance)
        except Exception as e:
            print(CustomException(task_group_key, e))

    #            print(f"{Colors.error}Error processing {task_group_key}: {e}")

    def execute_single_task(self) -> None:
        if self.task_group:
            self.execute_task(self.task_group)

    def execute_all_tasks(self) -> None:
        hashes = TaskHashes()
        for task_group_key in hashes.task_items:
            self.execute_task(task_group_key)


@dataclass
class Execution(object):
    task_group: str

    @property
    def task_manager(self):
        return TaskManager()

    def task_based_on_group(self) -> None:
        if self.task_group in self.dispatcher.collection:
            self.single_task()
        else:
            self.all_tasks()

    def single_task(self) -> None:
        if self.task_group:
            self.task(self.task_group)

    def all_tasks(self) -> None:
        hashes = TaskHashes()
        for task_group_key in hashes.task_items:
            self.task(task_group_key)

    def task(self, task_group_key: str) -> None:
        try:
            dispatcher_instance = self.get_dispatcher_instance(task_group_key)
            execution_function = self.task_manager.iteration.execute_iteration
            execution_function(task_group=dispatcher_instance)
        except Exception as e:
            print(CustomException(task_group_key, e))

    pass


@dataclass
class CustomException(Exception):
    operation: str
    error: Exception

    def __str__(self) -> str:
        return f"{Colors.error}Error processing {self.operation}: {self.error}"


if __name__ == "__main__":
    pass

from argparse import Namespace
from dataclasses import dataclass, field
from typing import Any

from build.decorators import FooterWrapper
from build.dispatchers import DispatcherTemplate, MainDispatcher
from build.exceptions.handlers import KeyboardInterruptHandler
from build.styles.palette import Colors
from build.tasks.definitions import TaskDefinitions
from build.tasks.managers import TaskManager


@KeyboardInterruptHandler
@FooterWrapper(message="All Finished!\n")
@dataclass
class Executor:
    arguments: Namespace = field(default_factory=Namespace)
    task_manager: TaskManager = field(default_factory=TaskManager)
    dispatcher: DispatcherTemplate = field(default_factory=DispatcherTemplate)
    task_group: str = field(default="")
    task_definitions: TaskDefinitions = field(default_factory=TaskDefinitions)
    path: str = field(init=False, default="")

    def __post_init__(self) -> None:
        self.set_path()
        self.initialize_task_manager()
        self.assign_task_group()
        self.initialize_task_dispatcher()
        self.execute_task_based_on_group()

    def execute_task_based_on_group(self) -> None:
        if self.task_group and self.task_group in self.dispatcher.collection:
            self.execute_single_task()
        else:
            self.execute_all_tasks()

    def set_path(self) -> None:
        assert hasattr(self.arguments, "path"), "Arguments must have 'path' attribute"
        self.path = self.arguments.path

    def initialize_task_manager(self) -> None:
        # self.task_manager.initialize_tasks(self.path)
        self.task_manager.initiate_task(self.path)

    def assign_task_group(self) -> None:
        try:
            if hasattr(self.arguments, "task_group"):
                self.task_group = self.arguments.task_group
            else:
                raise AttributeError("Arguments must have 'task_group' attribute")
        except Exception as e:
            print(f"Error processing arguments: {e}")
            print(CustomException("arguments", e))

    def initialize_task_dispatcher(self) -> None:
        dispatcher = MainDispatcher("task_group", self.task_definitions)
        self.dispatcher = dispatcher.get_dispatcher()

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
        for task_group_key in ["preparation", "migration", "application"]:
            self.execute_task(task_group_key)


@dataclass
class CustomException(Exception):
    operation: str
    error: Exception

    def __str__(self) -> str:
        return f"{Colors.error}Error processing {self.operation}: {self.error}"


if __name__ == "__main__":
    pass

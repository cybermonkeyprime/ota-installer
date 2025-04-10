from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple

import build.display as display
import build.variables as variables
from build.tasks.definitions import TaskDefinitions
from build.tasks.task_factory import TaskFactory
from build.variables import VariableManager
import build.exceptions.error_messages as error_messages


@dataclass
class TaskIteration(object):
    """
    Represents an iteration of tasks to be executed.

    Attributes:
        variable_manager: An instance of VariableManager to manage variables.
        task_group: A tuple of task names to be executed.
    """
    variable_manager: VariableManager = field()
    task_group: Tuple[str, ...] = field(default=("", ""))

    def execute_iteration(self, task_group: Tuple[str, ...]) -> None:
        task_director = TaskDirector()
        handle_task = task_director.handle_task
        try:
            [ handle_task(self.variable_manager, task_name) for task_name in task_group ]
        except TypeError as error:
            pass


@dataclass
class TaskDirector(object):
    """
    Directs the handling of tasks using a TaskFactory.
    """
    def handle_task(
        self, instance: variables.VariableManager, item: str
    ) -> TaskFactory:
        task_factory = TaskFactory(instance)
        request = task_factory.create_task(task_name=item)
        return request.perform_task()


@dataclass
class TaskManager(object):
    """
    Manages the execution of tasks based on a file name.

    Attributes:
        file_name: The name of the file to manage tasks for.
        sub_tasks: A collection of task definitions.
    """
    file_name: str = field(default="")
    sub_tasks: TaskDefinitions = field(default_factory=TaskDefinitions)

    @property
    def file_path(self) -> Path:
        return Path(self.file_name)

    @property
    def variable(self) -> variables.VariableManager:
        return variables.VariableManager(self.file_path)

    @property
    def iteration(self) -> TaskIteration:
        return TaskIteration(self.variable)

    def initiate_task(self, args: str) -> None:
        try:
            self.file_name = args
            self.list_vars()
        except Exception as error:
            print(f"{error_messages.ErrorMessage(error=error)}")

    def list_vars(self) -> None:
        try:
            display_processor = display.VariableProcessor(self.variable)
            display_processor.initiate_processing()
        except Exception as e:
            print(error_messages.CustomMessage(e))


@dataclass
class VariableControl:
    file_path: Path

    def variable(self):
        return variables.VariableManager(self.file_path)

    def iteration(self, variable):
        return TaskIteration(variable)

    def list_vars(self) -> None:
        try:
            display_processor = display.VariableProcessor(self.variable())
            display_processor.initiate_processing()
        except Exception as e:
            print(error_messages.CustomMessage(e))

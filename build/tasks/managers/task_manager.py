from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Tuple

from ..definitions import TaskDefinitions
from ..task_factory import TaskFactory

import build.display as display
import build.variables as variables


@dataclass
class TaskIteration:
    instance: variables.Manager = field()
    task_group: Tuple[str, str] = field(default=("", ""))

    def execute_iteration(self, task_group: Tuple[str, ...]) -> None:
        task_director = TaskDirector()
        try:
            stack = list(task_group)
            handle_task = task_director.handle_task
            while stack:
                handle_task(instance=self.instance, item=stack.pop(0))
        except TypeError as e:
            pass


@dataclass
class TaskDirector:
    def handle_task(self, instance: variables.Manager, item: str) -> TaskFactory:
        task_factory = TaskFactory(instance)
        request = task_factory.create_task(task_name=item)
        return request.perform_task()


@dataclass
class TaskManager:
    file_name: str = field(default="")
    function: Callable = field(default=Callable)
    iteration: TaskIteration | None = field(default=None)
    variable: variables.Manager = field(default=None)
    sub_tasks: TaskDefinitions = field(default_factory=TaskDefinitions)

    def initiate_task(self, args: str) -> None:
        try:
            self.file_name = args
            self.variable = variables.Manager(self.file_name)
            self.iteration = TaskIteration(self.variable)
            self.posix_path = Path(self.file_name)
            self.list_vars()
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_vars(self) -> None:
        try:
            display.VariableProcessor(self.variable).initiate_processing()
        except Exception as e:
            pass

from dataclasses import dataclass, field
from pathlib import Path

import build.display as display
import build.variables as variables
from build.tasks.definitions import TaskDefinitions
from build.tasks.task_factory import TaskFactory
from build.variables import VariableManager
import build.exceptions.error_messages as error_messages


@dataclass
class TaskIteration:
    # instance: variables.VariableManager = field()
    instance: VariableManager = field()
    task_group: tuple[str, str] = field(default=("", ""))

    def execute_iteration(self, task_group: tuple[str, ...]) -> None:
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
    def handle_task(
        self, instance: variables.VariableManager, item: str
    ) -> TaskFactory:
        task_factory = TaskFactory(instance)
        request = task_factory.create_task(task_name=item)
        return request.perform_task()


@dataclass
class TaskManager:
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
        except Exception as e:
            print(error_messages.ErrorMessage(error=e))

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

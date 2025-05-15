from dataclasses import dataclass, field
from pathlib import Path

from build.display import VariableProcessor as DisplayVariableProcessor
from build.exceptions.error_messages import ErrorMessage
from build.tasks.definitions import TaskDefinitions
from build.tasks.task_factory import TaskFactory
from build.variables import VariableManager


@dataclass
class TaskIteration(object):
    """
    Represents an iteration of tasks to be executed.

    Attributes:
        variable_manager: An instance of VariableManager to manage variables.
        task_group: A tuple of task names to be executed.
    """

    variable_manager: VariableManager = field()
    task_group: "tuple[str, ...]" = field(default=("", ""))

    def execute_iteration(self, task_group: "tuple[str, ...]") -> None:
        try:
            for task_name in task_group:
                task_factory = TaskFactory(self.variable_manager)
                request = task_factory.create_task(task_name)
                request.perform_task()
        except TypeError:
            print("Iteration skipped", end="\n\n")


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
    def variable(self) -> VariableManager:
        return VariableManager(self.file_path)

    @property
    def iteration(self) -> TaskIteration:
        return TaskIteration(self.variable)

    def initiate_task(self, file_name: str) -> None:
        self.file_name = file_name
        TaskInitiationManager(self.variable)


@dataclass
class TaskInitiationManager(object):
    variable: VariableManager

    def __post_init__(self) -> None:
        try:
            display_processor = DisplayVariableProcessor(self.variable)
            display_processor.initiate_processing()
        except Exception as error:
            print(f"{ErrorMessage(error=error)}")

    pass

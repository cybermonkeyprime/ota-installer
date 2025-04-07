from argparse import Namespace
from dataclasses import dataclass, field
from build.tasks import Executor as TaskExecutor


@dataclass
class TaskExecutionHandler(object):
    """
    Handles the execution of tasks using a given executor and arguments.

    Attributes:
        executor (TaskExecutor): The executor to run tasks.
        arguments (Namespace): The arguments to pass to the executor.
    """
    executor: type[TaskExecutor] = field(default_factory=TaskExecutor)
    arguments: Namespace = field(default_factory=Namespace)

    def execute(self) -> None:
        """Executes tasks using the provided executor and arguments."""
        try:
            self.executor(arguments=self.arguments)  # .initialize()
        except Exception as error:
            print(f"Task execution failed: {error}")

def main() -> None:
    excecutor = TaskExecutor
    arguments = None
    task_handler = TaskExecutionHandler(executor=excecutor)
    task_handler.execute()

if __name__ == "__main__":
    main()

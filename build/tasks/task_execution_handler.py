from argparse import Namespace
from dataclasses import dataclass, field
from build.tasks import Executor as TaskExecutor


@dataclass
class TaskExecutionHandler(object):
    executor: TaskExecutor = field(default_factory=TaskExecutor)
    arguments: Namespace = field(default_factory=Namespace)

    def execute(self) -> None:
        try:
            self.executor(arguments=self.arguments)  # .initialize()
        except Exception as error:
            print(f"Task execution failed: {error}")


if __name__ == "__main__":
    excecutor = TaskExecutor
    arguments = None
    task_handler = TaskExecutionHandler(executor=excecutor)
    task_handler.execute()

# src/ota_installer/handler/task_group_renderer.py
from collections.abc import Callable
from dataclasses import dataclass

from .task_group_pipelines import (
    ApplicationPipeline,
    MigrationPipeline,
    PreparationPipeline,
)


@dataclass(frozen=True, slots=True)
class TaskGroupRenderer:
    task_class: type
    task_name: str

    def __call__(self, *args, **kwargs) -> tuple:
        """
        Executes the task group's generation logic wrapped in the required UI
            decorators.
        """
        from ..style import decorator

        def result():
            return self.task_class.get_member_names()

        @decorator.PaddedFooterWrapper()
        def execute_pipeline():
            decorated_function: Callable = decorator.ConfirmationPrompt(
                char=" ", comment=f"perform the {self.task_name}s"
            )(result)

            return decorated_function()

        # 3. Fire the pipeline and hand back the final tuple payload
        return execute_pipeline()


# Signed off by Brian Sanford on 20260901

# src/ota_installer/task_group/task_group_renderer.py

from collections.abc import Callable
from dataclasses import dataclass

from ..log_setup import logger
from .task_group_pipeline import (
    APPLICATION,
    MIGRATION,
    PREPARATION,
    Pipeline,
)


@dataclass(frozen=True, slots=True)
class TaskGroupRenderer:
    pipeline: Pipeline
    task_name: str

    def __call__(self, *args, **kwargs) -> tuple[str, ...]:
        from ..style import decorator

        logger.debug(f"Rendering task group confirmation: {self.task_name}")

        def result() -> tuple[str, ...]:
            return tuple(step.name for step in self.pipeline.steps)

        @decorator.PaddedFooterWrapper()
        def execute_pipeline() -> tuple[str, ...]:
            decorated_function: Callable = decorator.ConfirmationPrompt(
                char=" ",
                comment=f"perform the {self.task_name}s",
            )(result)

            return decorated_function()

        return execute_pipeline()


TASK_GROUPS: dict[str, TaskGroupRenderer] = {
    "preparation": TaskGroupRenderer(
        pipeline=PREPARATION,
        task_name="Preparation Task",
    ),
    "migration": TaskGroupRenderer(
        pipeline=MIGRATION,
        task_name="Migration Task",
    ),
    "application": TaskGroupRenderer(
        pipeline=APPLICATION,
        task_name="Application Task",
    ),
}

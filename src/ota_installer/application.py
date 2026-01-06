# src/ota_installer/application.py
from . import decorators
from .display.show_display_components import (
    show_display_components,
)
from .exceptions.handlers import KeyboardInterruptHandler
from .program_versioning.constants.software_constants import SoftwareConstants
from .services import (
    ScreenManagerService,
)
from .tasks.execution.task_execution import CLIArguments, TaskExecutor


def run() -> None:
    screen_manager = ScreenManagerService()
    screen_manager.clear_screen()
    display_title()


def display_title():
    arguments = CLIArguments
    if not arguments.version:
        show_display_components()
        random_exit_message()


@decorators.StylizedIndentPrinter(indent=1, style="task", use_output=False)
def random_exit_message() -> str:
    from random import choice

    CELEBRATIONS = [
        "All tasks completed successfully!",
        "You did it, tech wizard!",
        "Mission complete—well done!",
        "Everything's in place.",
        f"{SoftwareConstants.TITLE.value} says: Great job!",
        f"{SoftwareConstants.TITLE.value} is complete!",
    ]

    emoji = choice(["🎉", "✅", "🚀", "✨", "🎯", "💻"])
    message = choice(CELEBRATIONS)

    return f"{message} {emoji}\n"


@KeyboardInterruptHandler
@decorators.FooterWrapper(message=random_exit_message())
def task_execution(arguments: CLIArguments):
    (
        TaskExecutor(arguments)
        .set_path()
        .initialize_task_manager()
        .assign_task_group()
        .initialize_task_dispatcher()
        .execute_task_based_on_group()
    )

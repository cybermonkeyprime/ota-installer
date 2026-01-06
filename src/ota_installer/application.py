# src/ota_installer/application.py
from . import decorators
from .display.components.clear_screen import clear_screen
from .display.show_display_header import show_display_header
from .exceptions.handlers.keyboard_interrupt_handler import (
    KeyboardInterruptHandler,
)
from .program_versioning.constants.software_constants import SoftwareConstants
from .tasks.execution.task_execution import CLIArguments, TaskExecutor


def run() -> None:
    clear_screen()
    display_title()


def display_title():
    arguments = CLIArguments
    if not arguments.version:
        show_display_header()
        random_exit_message()


@decorators.StylizedIndentPrinter(indent=1, style="task", use_output=False)
def random_exit_message() -> str:
    from secrets import choice

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

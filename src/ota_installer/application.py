# src/ota_installer/application.py
from dataclasses import dataclass, field

from . import decorators
from .display.configurations.display_configuration import (
    Configuration,
)
from .exceptions.handlers import KeyboardInterruptHandler
from .program_versioning.constants.software_constants import SoftwareConstants
from .services import (
    DisplayConfigurationService,
    ScreenManagerService,
)
from .tasks.execution.task_execution import CLIArguments, TaskExecutor


@dataclass
class Application(object):
    screen_manager: ScreenManagerService = field(
        default_factory=ScreenManagerService
    )
    display_configurator: DisplayConfigurationService = field(
        default_factory=DisplayConfigurationService
    )

    @property
    def display_config(self) -> Configuration:
        return self.display_configurator.get_display_configuration()

    def run(self) -> None:
        self.screen_manager.clear_screen()

        self.display_title()

    def display_title(self):
        arguments = CLIArguments
        if not arguments.version:
            self.display_config.create_version_display()
        else:
            print(self.display_config)


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

# src/ota_installer/application.py
from dataclasses import dataclass, field

from .decorators import FooterWrapper
from .display.configurations.display_configuration import (
    Configuration,
)
from .exceptions.handlers import KeyboardInterruptHandler
from .services import (
    DisplayConfigurationService,
    ScreenManagerService,
)
from .tasks.task_execution import CLIArguments, TaskExecutor


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
        if arguments.version:
            print(self.display_config)
        else:
            self.display_config.create_version_display()


@KeyboardInterruptHandler
@FooterWrapper(message="All Done!\n")
def task_execution(arguments: CLIArguments):
    (
        TaskExecutor(arguments)
        .set_path()
        .initialize_task_manager()
        .assign_task_group()
        .initialize_task_dispatcher()
        .execute_task_based_on_group()
    )

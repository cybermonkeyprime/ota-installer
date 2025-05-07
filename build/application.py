from dataclasses import dataclass, field

from build.services import (
    ArgumentParserService,
    DisplayConfigurationService,
    ScreenManagerService,
)
from build.tasks.task_execution import Executor as TaskExecutor
from build.tasks.task_execution_handler import TaskExecutionHandler


@dataclass
class Application(object):
    """Manages the main application logic and flow.

    Attributes:
        screen_manager: An instance of ScreenManagerService to manage screen operations.
        argument_parser: An instance of ArgumentParserService to parse CLI arguments.
        display_configurator: An instance of DisplayConfigurationService to manage display configurations.
        task_executor_cls: A class reference to TaskExecutor for executing tasks.
    """
    screen_manager: ScreenManagerService = field(default_factory=ScreenManagerService)
    argument_parser: ArgumentParserService = field(
        default_factory=ArgumentParserService
    )
    display_configurator: DisplayConfigurationService = field(
        default_factory=DisplayConfigurationService
    )
    task_executor_cli: TaskExecutor = field(default_factory=lambda: TaskExecutor)

    def run(self) -> None:
        """Executes the application logic."""
        try:
            arguments = self.argument_parser.parse_cli_arguments()
            self.screen_manager.clear_screen()
            display_config = self.display_configurator.fetch_configuration()

            if arguments.version:
                print(display_config)
            else:
                display_config.create_version_display()
                task_handler = TaskExecutionHandler(
                    executor=self.task_executor_cli, arguments=arguments
                )
                task_handler.execute()
        except Exception as error:
            raise ExceptionError(f"An error occurred: {error}")

class ExceptionError(Exception):
    pass

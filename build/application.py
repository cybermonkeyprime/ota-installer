from dataclasses import dataclass, field
from .tasks.task_execution import Executor as TaskExecutor
from .tasks.task_execution_handler import TaskExecutionHandler
from .services import (
    ScreenManagerService,
    ArgumentParserService,
    DisplayConfigurationService,
)


@dataclass
class Application(object):
    screen_manager: ScreenManagerService = field(default_factory=ScreenManagerService)
    argument_parser: ArgumentParserService = field(
        default_factory=ArgumentParserService
    )
    display_configurator: DisplayConfigurationService = field(
        default_factory=DisplayConfigurationService
    )
    task_executor_type: TaskExecutor = field(default_factory=lambda: TaskExecutor)

    def run(self) -> None:
        try:
            arguments = self.argument_parser.parse_cli_arguments()
            self.screen_manager.clear_screen()
            display_config = self.display_configurator.get_display_configuration()

            if arguments.version:
                print(display_config)
            else:
                display_config.create_version_display()
                task_handler = TaskExecutionHandler(
                    executor=self.task_executor_type, arguments=arguments
                )
                task_handler.execute()
        except Exception as error:
            print(f"An error occurred: {error}")

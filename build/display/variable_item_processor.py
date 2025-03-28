from dataclasses import dataclass, field

from dispatchers import MainDispatcher

import build.variables as variables
import build.display.base_classes as display_base_classes

VariableManager = variables.VariableManager


class VariableItemProcessor(object):
    processing_function: VariableManager = field(default_factory=VariableManager)
    title: str = field(default="")
    value: str = field(default="")
    dispatcher_type: str = field(default="variable")

    def __post_init__(self) -> None:
        self.process_item()

    @property
    def dispatch_handler(self) -> MainDispatcher:
        dispatch_handler = display_base_classes.DispatchHandler(
            self.dispatcher_type, self.processing_function
        )
        return dispatch_handler.create_dispatcher()

    def process_item(self) -> None:
        try:
            validation = display_base_classes.ValueValidation(
                dispatch_handler=self.dispatch_handler
            )
            value = validation.validate_value(key=self.value)

            variable_output = display_base_classes.OutputFormatter(
                title=self.title, value=value
            )
            variable_output.format_and_print()
        except Exception as error_msg:
            print(display_base_classes.ErrorMessage("variable", self.title, error_msg))

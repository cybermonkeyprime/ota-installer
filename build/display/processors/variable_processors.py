from dataclasses import dataclass, field
from pathlib import Path

from decorators import ColorizedIndentPrinter
from dispatchers import DispatcherManager

import build.variables as variables
from build.exceptions import error_messages


@dataclass
class VariableItemProcessor(object):
    """
    Processes a variable item by validating and outputting its value.

    Attributes:
        title (str): The title of the variable.
        value (str): The value of the variable.
        dispatcher_manager (DispatcherManager): The dispatcher manager instance
    """

    processing_function: type = field(
        default_factory=lambda: variables.VariableManager
    )
    title: str = field(default="")
    value: str = field(default="")
    dispatcher_type: str = field(default="variable")

    def __post_init__(self) -> None:
        self.process_item()

    @property
    def dispatch_handler(self) -> DispatcherManager:
        dispatch_handler = VariableDispatchHandler(
            self.dispatcher_type, self.processing_function
        )
        return dispatch_handler.retriever()

    def process_item(self) -> None:
        try:
            validation = VariableValueValidation(
                dispatch_handler=self.dispatch_handler
            )
            value = validation.evaluator(key=self.value)

            variable_output = VariableOutputProcessor(
                title=self.title, value=value
            )
            variable_output.parser()
        except Exception as error:
            print(
                error_messages.MessageWithTitleAndValue(
                    title="variable item", value=self.title, error=error
                )
            )


@dataclass
class VariableValueValidation(object):
    """Validates the value of a variable using a dispatcher.

    Attributes:
        dispatch_handler (DispatcherManager): The dispatcher manager instance.
        processing_function (type): The function used for processing the variable.
    """

    from build.dispatchers import CollectionDictionary, DispatcherTemplate

    dispatch_handler: DispatcherManager = field(
        default_factory=DispatcherManager
    )
    processing_function: type = field(
        default_factory=lambda: variables.VariableManager
    )

    def fetcher(self) -> DispatcherTemplate:
        return self.dispatch_handler.get_dispatcher()

    def evaluator(self, key: str) -> CollectionDictionary:
        value = self.fetcher().get_value(key=key)
        if value is None:
            print(f"{value=}")
        return value


@dataclass
class VariableOutputProcessor(object):
    """Processes and outputs the value of a variable.

    Attributes:
        title (str): The title of the variable.
        value (type | Path | None): The value of the variable, can be a type, Path, or None.
    """

    title: str = field(default="")
    value: type | Path | None = field(default=None)

    @ColorizedIndentPrinter(indent=1)
    def parser(self) -> str:
        return f"{self.title.upper()}: {self.value}"


@dataclass
class VariableDispatchHandler(object):
    """
    Handles the retrieval of a dispatcher based on the dispatcher type.

    Attributes:
        dispatcher_type (DispatcherType): The type of dispatcher to retrieve.
        variable_manager_cls (Type[Callable]): The variable manager class.
    """

    dispatcher_type: str = field(default="")
    processing_function: type = field(
        default_factory=lambda: variables.VariableManager
    )

    def retriever(self) -> DispatcherManager:
        return DispatcherManager(
            self.dispatcher_type, self.processing_function
        )

    def __str__(self) -> str:
        return f"{self.retriever()}"

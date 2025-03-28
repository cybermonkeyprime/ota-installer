from dataclasses import dataclass, field
from pathlib import Path

from decorators import ColorizedIndentPrinter
from dispatchers import MainDispatcher

import build.variables as variables
from build.dispatchers import (
    CollectionDictionary,
    DispatcherTemplate,
)
from build.exceptions import error_messages

VariableManager = variables.VariableManager


@dataclass
class VariableItemProcessor(object):
    processing_function: VariableManager = field(default_factory=VariableManager)
    title: str = field(default="")
    value: str = field(default="")
    dispatcher_type: str = field(default="variable")

    def __post_init__(self) -> None:
        self.process_item()

    @property
    def dispatch_handler(self) -> MainDispatcher:
        dispatch_handler = DispatchHandler(
            self.dispatcher_type, self.processing_function
        )
        return dispatch_handler.retriever()

    def process_item(self) -> None:
        try:
            validation = ValueValidation(dispatch_handler=self.dispatch_handler)
            value = validation.evaluator(key=self.value)

            variable_output = VariableOutputProcessor(title=self.title, value=value)
            variable_output.parser()
        except Exception as error:
            print(
                error_messages.MessageWithTitleAndValue(
                    title="variable item", value=self.title, error=error
                )
            )


@dataclass
class ValueValidation(object):
    dispatch_handler: MainDispatcher = field(default_factory=MainDispatcher)
    processing_function: VariableManager = field(default_factory=VariableManager)

    def fetcher(self) -> DispatcherTemplate:
        return self.dispatch_handler.receiver()

    def evaluator(self, key: str) -> CollectionDictionary:
        value = self.fetcher().get_value(key=key)
        if value is None:
            print(f"{value=}")
        return value


@dataclass
class VariableOutputProcessor(object):
    title: str = field(default="")
    value: type | Path | None = field(default=None)

    @ColorizedIndentPrinter(indent=1)
    def parser(self) -> str:
        return f"{self.title.upper()}: {self.value}"


@dataclass
class DispatchHandler(object):
    dispatcher_type: str = field(default="")
    processing_function: VariableManager = field(default_factory=VariableManager)

    def retriever(self) -> MainDispatcher:
        # return self.processing_function.get_dispatcher(self.dispatcher_type)
        return MainDispatcher(self.dispatcher_type, self.processing_function)

    def __str__(self) -> str:
        return f"{self.retriever()}"

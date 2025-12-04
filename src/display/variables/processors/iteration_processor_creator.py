# src/display/variables/processors/iteration_processor_creator.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Self

import src.dispatchers.mappings as dispatcher_mappings
import src.display.variables.functions as functions
import src.variables as variables
from src.logger import logger

DispatcherTypeMapping = dispatcher_mappings.DispatcherTypeMapping


class IterationProcessorCreator(object):
    processing_function: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )
    file_names: tuple = field(init=False)

    def set_title(self, title: str) -> Self:
        self.title = str(title).strip().lower().capitalize()
        return self

    def set_iteration(self, iteration: tuple) -> Self:
        self.iteration = tuple(iteration)
        return self

    def process_items(self) -> None:
        for items in self.iteration:
            try:
                data_enum = Enum(
                    "DataEnum",
                    {
                        "TITLE": "",
                        "VALUE": "",
                    },
                )
                functions.parse_output(data_enum)
            except Exception as e:
                name = type(self.iteration).__name__.capitalize()
                value = self.iteration
                logger.error(
                    f"[Error] Processing {self.title} {self.iteration} failed: {e}"
                )

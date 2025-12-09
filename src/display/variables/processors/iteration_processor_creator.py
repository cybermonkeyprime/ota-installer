# src/display/variables/processors/iteration_processor_creator.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Self

from rich.console import Console
from rich.table import Table

import src.dispatchers.mappings as dispatcher_mappings
import src.display.variables.functions as functions
import src.variables as variables
from src.logger import logger

DispatcherTypeMapping = dispatcher_mappings.DispatcherTypeMapping


@dataclass
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
        console = Console()
        table = Table(title="", box=None)
        table.add_column("Column 1", style="cyan", no_wrap=True)
        table.add_column("Column 2", justify="right", style="magenta")
        for _ in self.iteration:
            try:
                data_enum = Enum(
                    "DataEnum",
                    {
                        "TITLE": "",
                        "VALUE": "",
                    },
                )
                table.add_row(
                    f"B{data_enum.TITLE.value.upper()}:",
                    f"{data_enum.VALUE.value}",
                )
                # functions.parse_output(data_enum)
            except Exception as e:
                logger.error(
                    f"[Error] Processing {self.title} {self.iteration} failed: {e}"
                )
        console.print(table)

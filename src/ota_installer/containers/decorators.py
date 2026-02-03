# src/ota_installer/containers/decorators.py
from dependency_injector import containers, providers


class Decorators(containers.DeclarativeContainer):
    from ..decorators.colorizer import Colorizer
    from ..decorators.indent_wrapper import IndentWrapper
    from ..decorators.output_printer import OutputPrinter

    colorizer = providers.Factory(Colorizer)
    indent_wrapper = providers.Factory(IndentWrapper)
    output_printer = providers.Factory(OutputPrinter)

# src/ota_installer/display/variables/functions.py
from ...variables.variable_manager import VariableManager
from ..variables.processors import (
    DirectoryIterationProcessor,
    FileIterationProcessor,
    VariableFileProcessor,
)

""" directory names """


def set_ota_file_directory(
    processing_function: VariableManager,
) -> None:
    (
        VariableFileProcessor(processing_function)
        .set_title("ota_file_directory")
        .set_value("path.parent")
        .process_items()
    )


def set_magisk_image_directories(
    processing_function: VariableManager,
) -> None:
    (
        DirectoryIterationProcessor(processing_function)
        .set_directory_names(("local", "remote"))
        .set_directory_type("magisk")
        .set_variable_prefix("_")
        .process_items()
    )


def set_boot_image_directories(
    processing_function: VariableManager,
) -> None:
    (
        DirectoryIterationProcessor(processing_function)
        .set_directory_names(("stock", "magisk"))
        .set_directory_type("")
        .set_variable_prefix("")
        .process_items()
    )


""" file names """


def set_ota_file_name(processing_function: VariableManager) -> None:
    (
        VariableFileProcessor(processing_function)
        .set_title("ota_file_name")
        .set_value("path.name")
        .process_items()
    )


def set_image_file_names(
    processing_function: VariableManager,
) -> None:
    (
        FileIterationProcessor(processing_function)
        .set_file_names(("payload", "stock", "magisk"))
        .process_items()
    )


""" log files """


def set_log_file(processing_function: VariableManager) -> None:
    (
        VariableFileProcessor(processing_function)
        .set_title("log_file")
        .set_value("log_file")
        .process_items()
    )

import src.decorators as decorators
import src.display.variables.processors as dvp
import src.variables as variables

""" directory names """


def set_ota_file_directory(
    processing_function: variables.VariableManager,
) -> None:
    (
        dvp.VariableFileProcessor(processing_function)
        .set_title("ota_file_directory")
        .set_value("path.parent")
        .process_items()
    )


def set_magisk_image_directories(
    processing_function: variables.VariableManager,
) -> None:
    (
        dvp.DirectoryIterationProcessor(processing_function)
        .set_directory_names(("local", "remote"))
        .set_directory_type("magisk")
        .set_variable_prefix("_")
        .process_items()
    )


def set_boot_image_directories(
    processing_function: variables.VariableManager,
) -> None:
    (
        dvp.DirectoryIterationProcessor(processing_function)
        .set_directory_names(("stock", "magisk"))
        .set_directory_type("")
        .set_variable_prefix("")
        .process_items()
    )


""" file names """


def set_ota_file_name(processing_function: variables.VariableManager) -> None:
    (
        dvp.VariableFileProcessor(processing_function)
        .set_title("ota_file_name")
        .set_value("path.name")
        .process_items()
    )


def set_image_file_names(
    processing_function: variables.VariableManager,
) -> None:
    (
        dvp.FileIterationProcessor(processing_function)
        .set_file_names(("payload", "stock", "magisk"))
        .process_items()
    )


""" log files """


def set_log_file(processing_function: variables.VariableManager) -> None:
    (
        dvp.VariableFileProcessor(processing_function)
        .set_title("log_file")
        .set_value("log_file")
        .process_items()
    )


""" output """


@decorators.ColorizedIndentPrinter(indent=1)
def parse_output(data_enum: type) -> str:
    return f"{data_enum.TITLE.value.upper()}: {data_enum.VALUE.value}"

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Self

from loguru import logger
from rich.logging import RichHandler

LogMethod = Callable[[dict[str, str]], None]


def configure_logger() -> None:
    """Configure the logger with different handlers for console and file output."""

    logger.remove()  # Remove all default loggers

    """ Human-readable stderr for local console use (warnings or higher) """
    logger.add(
        RichHandler(
            markup=True,  # Enables rich text formatting
            rich_tracebacks=True,  # Beautiful, colorized tracebacks
            show_time=True,
            show_level=True,
            show_path=True,
        ),
        level="WARNING",
        format="{message}",
        backtrace=False,
    )


def enable_debug_logging() -> None:
    """Enable debug output to stderr."""
    logger.remove()  # remove default handler
    logger.add(
        RichHandler(
            markup=True,  # Enables rich text formatting
            rich_tracebacks=True,  # Beautiful, colorized tracebacks
            show_time=True,
            show_level=True,
            show_path=True,
        ),
    )


def structured_sink(message) -> None:
    log_data = message.record["extra"].get("log_data")

    if log_data is not None:
        print(log_data)


def add_structured_log_sink(path: Path) -> None:
    """Add a structured log sink to the specified path."""
    logger.add(
        str(path),
        format="{extra[log_data]}",
        level="DEBUG",
        serialize=False,
        backtrace=True,
        diagnose=True,
        rotation=None,  # No rotation, since filename is already unique
        retention=None,
    )


def log_messages() -> None:
    """Log various messages at different severity levels."""
    logger.trace("A trace message.")
    logger.debug("A debug message.")
    logger.info("An info message.")
    logger.success("A success message.")
    logger.warning("A warning message.")
    logger.error("An error message.")
    logger.critical("A critical message.")


configure_logger()


def fetch_logger_type(severity: str) -> LogMethod:
    """Fetches the corresponding logger method based on severity string."""
    return getattr(logger, severity.lower(), logger.info)


class LogType(StrEnum):
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

    @property
    def logger_type(self) -> LogMethod:
        return fetch_logger_type(self.value)

    def bind(self, log_data: dict[str, str]) -> LogMethod:
        bound_logger = logger.bind(log_data=log_data).opt(depth=3)
        return getattr(bound_logger, self.value)

    def handle_exception(
        self, exception_type: type[BaseException], response: str
    ):
        """Logs the error and raises the provided exception type."""
        (
            ExceptionHandler(self.value, exception_type, response)
            .log_report()
            .raise_error()
        )

    def write_log(self, response):
        """Writes a simple structured log message."""
        report_log = {"status": self.value, "response": response}

        self.bind(report_log)(response)


@dataclass(frozen=True, slots=True)
class ExceptionHandler:
    severity: str
    exception_type: type[BaseException] | None
    response: str

    @property
    def logger_type(self):
        return fetch_logger_type(self.severity)

    @property
    def report_log(self) -> dict[str, str]:
        struct = {"status": self.severity}

        if self.exception_type is not None:
            struct["exception_type"] = self.exception_type.__name__

        struct["response"] = self.response
        return struct

    def bind(self, log_data: dict[str, str]) -> LogMethod:
        bound_logger = logger.bind(log_data=log_data).opt(depth=1)
        return getattr(bound_logger, self.severity)

    def log_report(self) -> Self:
        self.bind(self.report_log)(self.response)

        return self

    def raise_error(self) -> Self:
        if self.exception_type:
            raise self.exception_type(self.report_log)
        return self


def main() -> None:
    from contextlib import suppress

    """Main entry point of the application."""
    configure_logger()

    # Test cases
    LogType.WARNING.write_log("This is a clean warning message!")

    with suppress(TypeError):
        LogType.ERROR.handle_exception(
            TypeError, "Uh Oh! This is not the right type!"
        )


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260920

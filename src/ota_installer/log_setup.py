import sys
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Self

from loguru import logger
from rich.logging import RichHandler


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
        # format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{function}:{line} - {message}",
        backtrace=False,
    )

    """ structured machine-readable stdout (for logs to file, piping, etc. """
    logger.add(
        sys.stdout,
        level="CRITICAL",  # Can lower to DEBUG for verbose JSON output
        serialize=True,
        colorize=True,
        backtrace=False,
        diagnose=True,
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
        #    sys.stderr,
        level="DEBUG",
        # format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{function}:{line} - {message}",
        format="{message}",
        serialize=False,
        # colorize=True,
        backtrace=True,
        # diagnose=True,
    )
    # Keep JSON logs (stdout)
    logger.add(
        sys.stdout,
        level="DEBUG",
        serialize=True,
        backtrace=True,
        diagnose=True,
    )


def add_structured_log_sink(path: Path) -> None:
    """Add a structured log sink to the specified path."""
    logger.add(
        str(path),
        level="DEBUG",
        serialize=True,
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


class LogType(StrEnum):
    TRACE = auto()
    DEBUG = auto()
    INFO = auto()
    SUCCESS = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

    def handle_exception(self, exception_type: Callable, response: str):
        (
            ExceptionHandler(self.value, exception_type, response)
            .log_report()
            .raise_error()
        )

    def write_log(self, response: str):
        getattr(logger, self.value)(
            {"status": self.value, "response": response}
        )


@dataclass(frozen=True, slots=True)
class ExceptionHandler:
    severity: str
    exception_type: Callable
    response: str

    @property
    def report(self) -> dict[str, str]:
        struct = {"status": self.severity}

        if self.exception_type is not None:
            struct["exception_type"] = self.exception_type.__name__

        struct["response"] = self.response
        return struct

    def log_report(self) -> Self:
        getattr(logger, self.severity.lower())(self.report)
        return self

    def raise_error(self) -> Self:
        if self.exception_type:
            raise self.exception_type(self.report)
        return self


def main() -> None:
    """Main entry point of the application."""
    log_messages()


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260920

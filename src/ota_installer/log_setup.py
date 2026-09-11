import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

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


@dataclass(frozen=True, slots=True)
class StatusReporter:
    status: str
    exception_type: Callable | None
    response: str

    @property
    def report(self) -> dict[str, str]:
        struct = {"status": self.status}
        if self.exception_type is not None:
            struct["exception_type"] = str(self.exception_type)
        struct["response"] = self.response
        return struct

    def log_report(self):
        getattr(logger, self.status.lower())(self.report)

    def raise_error(self) -> None:
        if self.exception_type:
            raise self.exception_type(self.report)

    def pipeline(self) -> None:
        self.log_report()
        self.raise_error()


def log_status(
    status: str, exception_type: Callable | None, response: str
) -> None:
    StatusReporter(status, exception_type, response).pipeline()


def main() -> None:
    """Main entry point of the application."""
    log_messages()


if __name__ == "__main__":
    main()

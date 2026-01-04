import sys
from pathlib import Path

from loguru import logger
from rich.logging import RichHandler

# Remove all default loggers
logger.remove()

# Human-readable stderr for local console use (warnings or higher)
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

# Structured machine-readable stdout (for logs to file, piping, etc.)
logger.add(
    sys.stdout,
    level="CRITICAL",  # Can lower to DEBUG for verbose JSON output
    serialize=True,
    colorize=True,
    backtrace=False,
    diagnose=True,
)


def show_debug() -> None:
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


def add_structured_log_sink(path: str | Path) -> None:
    logger.add(
        str(path),
        level="DEBUG",
        serialize=True,
        backtrace=True,
        diagnose=True,
        rotation=None,  # No rotation, since filename is already unique
        retention=None,
    )


def main():
    logger.trace("A trace message.")
    logger.debug("A debug message.")
    logger.debug("An info message.")
    logger.success("A success message.")
    logger.warning("A warning message.")
    logger.error("An error message.")
    logger.critical("A critical message.")


if __name__ == "__main__":
    main()

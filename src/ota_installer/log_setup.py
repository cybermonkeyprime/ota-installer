import sys

from loguru import logger

# Standard verbose format for ERROR and above
logger.add(
    sys.stderr,
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {module}:{function}:{line} - {message}",
    colorize=True,
)
logger.remove()  # remove default handler
logger.add(sys.stderr, level="WARNING")  # suppress INFO and DEBUG


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

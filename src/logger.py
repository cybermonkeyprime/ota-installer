import sys

from loguru import logger

logger.add(
    sys.stderr,
    format="{level} | {message} | {extra}",
)


def main():
    logger.trace("A trace message.")
    logger.debug("A debug message.")
    logger.info("An info message.")
    logger.success("A success message.")
    logger.warning("A warning message.")
    logger.error("An error message.")
    logger.critical("A critical message.")


if __name__ == "__main__":
    main()

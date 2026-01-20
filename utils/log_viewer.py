#!/usr/bin/env python3
# utils/log_viewer.py
import argparse
import json
from enum import Enum
from pathlib import Path


class LogLevel(str, Enum):
    DEBUG = "\033[36m"  # Cyan
    INFO = "\033[32m"  # Green
    WARNING = "\033[33m"  # Yellow
    ERROR = "\033[31m"  # Red
    CRITICAL = "\033[41m"  # Red BG
    RESET = "\033[0m"


def get_color(level: str) -> str:
    """Return the color code for the given log level."""
    return (
        LogLevel[level.upper()].value
        if level.upper() in LogLevel.__members__
        else LogLevel.RESET.value
    )


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Structured log viewer for Loguru JSON files"
    )
    parser.add_argument("file", help="Path to log file")
    parser.add_argument(
        "--level", help="Filter by log level (e.g. INFO, WARNING)"
    )
    parser.add_argument(
        "--task", help="Filter by bound task name (if using .bind(task=...))"
    )
    parser.add_argument(
        "--event", help="Filter by event name (if present in extra)"
    )
    parser.add_argument(
        "--pretty", action="store_true", help="Pretty-print full log lines"
    )
    return parser.parse_args()


def process_log_line(line: str, args: argparse.Namespace) -> None:
    """Process a single log line and print it if it matches the filters."""
    try:
        log = json.loads(line)
    except json.JSONDecodeError:
        return

    level = log.get("level", {}).get("name", "INFO")
    msg = log.get("message", "")
    time = log.get("time", "")[:19].replace("T", " ")
    extra = log.get("extra", {})

    # Filters
    if args.level and level.upper() != args.level.upper():
        return
    if args.task and extra.get("task") != args.task:
        return
    if args.event and extra.get("event") != args.event:
        return

    if args.pretty:
        print(json.dumps(log, indent=2))
    else:
        print(
            f"{get_color(level)}[{level:8}] {time} | {extra.get('task', ''):<16} | {msg}{LogLevel.RESET.value}"
        )


def main():
    """Main function to execute the log viewer."""
    args = parse_args()
    path = Path(args.file)

    if not path.exists():
        print(f"❌ File not found: {path}")
        return

    with path.open() as f:
        for line in f:
            process_log_line(line, args)


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260120

#!/usr/bin/env python3
# utils/log_viewer.py
import argparse
import json
from pathlib import Path


def color(level):
    return {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[41m",  # Red BG
    }.get(level.upper(), "\033[0m")


RESET = "\033[0m"


def parse_args():
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


def main():
    args = parse_args()
    path = Path(args.file)
    if not path.exists():
        print(f"❌ File not found: {path}")
        return

    with path.open() as f:
        for line in f:
            try:
                log = json.loads(line)
            except json.JSONDecodeError:
                continue

            level = log.get("level", {}).get("name", "INFO")
            msg = log.get("message", "")
            time = log.get("time", "")[:19].replace("T", " ")
            extra = log.get("extra", {})

            # Filters
            if args.level and level.upper() != args.level.upper():
                continue
            if args.task and extra.get("task") != args.task:
                continue
            if args.event and extra.get("event") != args.event:
                continue

            if args.pretty:
                print(json.dumps(log, indent=2))
            else:
                print(
                    f"{color(level)}[{level:8}] {time} | {extra.get('task', ''):<16} | {msg}{RESET}"
                )


if __name__ == "__main__":
    main()

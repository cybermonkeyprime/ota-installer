#! /usr/bin/env python
# utils/fix_error.py
import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path

import openai
from openai.types.chat.chat_completion import ChatCompletion

client = openai.OpenAI()


@dataclass
class ErrorTroubleshooter(object):
    """A class to troubleshoot Python script errors using OpenAI's API."""

    input_file: Path

    @property
    def error_message(self) -> str:
        """Retrieve the error message from the input file."""
        return subprocess.run(
            ["cat", self.input_file], capture_output=True, text=True
        ).stderr

    @property
    def prompt(self) -> str:
        """Create a prompt for the OpenAI API based on the error message."""
        return f"Explain and fix this Python error:\n\n{self.error_message}"

    @property
    def response(self) -> ChatCompletion:
        """Get the response from the OpenAI API."""
        return openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": self.prompt}],
        )

    @property
    def message(self) -> str | None:
        """Extract the message content from the API response."""
        return self.response.choices[0].message.content


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Fix Python script errors.")
    parser.add_argument(
        "script_path",
        type=str,
        help="Path to the Python script to fix errors in.",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the script."""
    arguments = parse_arguments()
    script_path = Path(arguments.script_path)
    error_troubleshooter = ErrorTroubleshooter(script_path)
    print(error_troubleshooter.message)


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260120

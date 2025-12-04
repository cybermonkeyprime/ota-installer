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
    input_file: Path

    @property
    def error_message(self) -> str:
        return subprocess.run(
            ["cat", self.input_file], capture_output=True, text=True
        ).stderr

    @property
    def prompt(self) -> str:
        return f"Explain and fix this Python error:\n\n{self.error_message}"

    @property
    def response(self) -> ChatCompletion:
        return openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": self.prompt}],
        )

    @property
    def message(self) -> str | None:
        return self.response.choices[0].message.content


def argument_definitions():
    parser = argparse.ArgumentParser(description="Fix Python script errors.")
    parser.add_argument(
        "script_path",
        type=str,
        help="Path to the Python script to fix errors in.",
    )
    return parser.parse_args()


def main() -> None:
    arguments = argument_definitions()
    script_path = Path(arguments.script_path)
    error_troubleshooter = ErrorTroubleshooter(script_path)
    print(error_troubleshooter.message)


if __name__ == "__main__":
    main()

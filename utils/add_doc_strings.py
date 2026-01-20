#! /usr/bin/env python
import argparse
import subprocess
from dataclasses import dataclass
from pathlib import Path

import openai
from openai.types.chat.chat_completion import ChatCompletion

client = openai.OpenAI()


@dataclass
class DocStringGenerator(object):
    input_file: Path

    @property
    def content(self) -> str:
        return subprocess.run(
            ["cat", self.input_file], capture_output=True, text=True
        ).stdout

    @property
    def prompt(self) -> str:
        return (
            "You are a senior Python developer. Add helpful docstrings to all "
            "classes, functions, and methods in the following Python code."
            "Keep all original code unchanged except for adding the docstrings."
            "Do not change code logic or structure. Here is the code:\n\n"
            f"{self.content}"
        )

    @property
    def response(self) -> ChatCompletion:
        return openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": self.prompt}],
        )

    @property
    def commented_code(self) -> str | None:
        return self.response.choices[0].message.content


def argument_definitions():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Add docstrings to Python code using OpenAI API."
    )
    parser.add_argument(
        "input_file", help="Path to the Python file to process."
    )
    return parser.parse_args()


def main():
    arguments: argparse.Namespace = argument_definitions()
    input_file: Path = Path(arguments.input_file)
    doc_string_generator = DocStringGenerator(input_file)

    print(doc_string_generator.commented_code)


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260120

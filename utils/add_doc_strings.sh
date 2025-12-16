#!/usr/bin/env zsh
file_name="$1"

request="create google style docstrings for each class/method and function in the following python script"

sgpt "$request: $(batcat -p --color=never $file_name)"

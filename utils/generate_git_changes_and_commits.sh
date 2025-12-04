#!/usr/bin/env zsh

append_git_diff_changes() {
  output_file="$1"
  shellgpt_request="$(get_shellgpt_request)"
  filter_pattern="Please provide the git diff output"

  echo "$shellgpt_request" | tee git_changes.sh
}

apply_git_diff_changes() {
  git_diff_report="$(get_git_diff_report)"

  if [[ "$git_diff_report" != "" ]]; then
    append_git_diff_changes
  else
    print_error_message
  fi
}

get_git_diff_report() {
  git diff
}

get_shellgpt_request() {
  git_diff_report="$(get_git_diff_report)"
  request_text="Generate git comments based off the following git diff,
  the output should be git add/rm and git commit -m commands,
  it should be verbose for each files, stating what was changed and on the affected line number,
  each file should only have one commit
  ignore files with a pyc extension"
  shellgpt --code "$request_text: $git_diff_report"
}

print_error_message() {
    echo "No changes in git diff report"
}

output_file="git_changes.txt"

apply_git_diff_changes "$output_file"

#!/usr/bin/env zsh
git_file_management_and_comments() {
	. ./git_changes.sh
}

get_git_diff() {
	git diff
}

git_upload() {
	git push origin main
}

git_file_management_and_comments

git_upload

#!/bin/bash -e
#
# GitLab API access helper functions.

gitlab() {
    COMMAND="$1"
    RESOURCE="$2"
    PROJECT_URL="https://gitlab.com/api/v4/projects/${GITLAB_PROJECT_NAME}"
    set -e
    curl --silent \
        --header "Authorization: Bearer $GITLAB_API_TOKEN" \
        --request $COMMAND \
        "${PROJECT_URL}/${RESOURCE}" "${@:3}"
}

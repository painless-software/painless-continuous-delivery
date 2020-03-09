#!/bin/bash -e
#
# GitLab API access helper functions.

gitlab() {
    COMMAND="$1"
    RESOURCE="$2"
    PROJECT_NAME="appuio%2Fexample-django"
    PROJECT_URL="https://gitlab.com/api/v4/projects/${PROJECT_NAME}"
    set -e
    curl --silent \
        --header "Authorization: Bearer $GITLAB_API_TOKEN" \
        --request $COMMAND \
        "${PROJECT_URL}/${RESOURCE}" "${@:3}"
}

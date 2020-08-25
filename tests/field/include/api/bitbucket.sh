#!/bin/bash -e
#
# Bitbucket API access helper functions.

bitbucket() {
    COMMAND="$1"
    RESOURCE="$2"
    PROJECT_URL="https://gitlab.com/api/v4/projects/${BITBUCKET_PROJECT_NAME}"
    set -e
    curl --silent \
        --header "Authorization: Bearer $BITBUCKET_API_TOKEN" \
        --request $COMMAND \
        "${PROJECT_URL}/${RESOURCE}" "${@:3}"
}

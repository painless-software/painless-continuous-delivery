#!/bin/bash -e
#
# ANSI colored logging for the CI pipeline.

log() {
    NOCOLOR='\033[0m'
    BLUE='\033[1;34m'
    echo -e "$1) ${BLUE}${@:2}${NOCOLOR} ..."
}

#!/bin/bash -e
#
# NOTE: For the very first deployment please follow
# the steps in the README for the target platform setup.
#
# The periodic regeneration is configured as a scheduled
# pipeline in GitLab > CI/CD > Schedules.
#
# To run this field test locally, see the instructions
# in the CONTRIBUTING.rst document.

BASEDIR=$(dirname $0)

source ${BASEDIR}/include/logging.sh
source ${BASEDIR}/include/api/bitbucket.sh

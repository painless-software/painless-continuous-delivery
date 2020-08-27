#!/bin/bash -e
#
# NOTE: For the very first deployment please follow
# the steps in the README for the target platform setup.
#
# The periodic regeneration is configured as a scheduled
# pipeline in GitLab > CI/CD > Schedules.
#
# To run this field test locally, see the instructions
# in the /tests/README.rst document.

BITBUCKET_PROJECT_NAME="appuio%2Fexample-bitbucket"

BASEDIR=$(dirname $0)

source ${BASEDIR}/include/logging.sh
source ${BASEDIR}/include/api/bitbucket.sh

log 1 'Delete existing merge requests, Git tags, etc.'
# TODO: Bitbucket API operations

log 2 'Create demo project from scratch and push it'
tox -e cookiecutter -- \
    project_name="Example Bitbucket" \
    project_description="Hello world on Bitbucket" \
    vcs_platform=Bitbucket.org \
    vcs_account=appuio \
    ci_service=bitbucket-pipelines.yml \
    cloud_platform=APPUiO \
    cloud_account="demo4501@appuio.ch" \
    environment_strategy=dedicated \
    cronjobs=complex \
    framework=Django \
    database=Postgres \
    monitoring=Sentry \
    license=GPL-3 \
    push=force \
    ${*} \
    --no-input

cd /tmp/painless-generated-projects/example-bitbucket

log 3 'Prepare feature branch'
# TODO: reuse existing code

log 4 'Add an untested feature'
# TODO: reuse existing code

log 5 'Create merge request'
# TODO: Bitbucket API operations

log 6 'Allow pipeline to build and push an image'
for minutes in $(seq 13 -1 1); do
    echo "- Waiting... ($minutes' remaining)"
    sleep 1m
done

log 7 'Trigger production release'
git checkout master
git tag 1.0.0
git push --tags --force

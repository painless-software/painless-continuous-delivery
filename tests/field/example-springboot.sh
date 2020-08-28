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

GITLAB_PROJECT_NAME="appuio%2Fexample-springboot"
BASEDIR=$(dirname $0)

source ${BASEDIR}/include/logging.sh
source ${BASEDIR}/include/api/gitlab.sh

log 1 'Delete existing merge requests, Git tags, etc.'
for IID in $(gitlab GET 'merge_requests?state=all&scope=all' \
           | sed -E -e 's/"iid":([0-9]*),/\n\1\n/g' | sed -e '/^[^0-9].*$/d'); do
    echo 'Delete MR !'${IID}' ...'
    gitlab DELETE merge_requests/$IID
done
for TAG in $(gitlab GET repository/tags \
           | sed -E -e 's/"name":"([^"]*)",/\n\1\n/g' | sed -E -e '/^(\[|")/d'); do
    echo 'Delete Git tag '${TAG}' ...'
    gitlab DELETE repository/tags/$TAG
done

log 2 'Create demo project from scratch and push it'
tox -e cookiecutter -- \
    project_name="Example SpringBoot" \
    project_description="Spring Boot Hello World" \
    vcs_platform=GitLab.com \
    vcs_account=appuio \
    ci_service=.gitlab-ci.yml \
    cloud_platform=APPUiO \
    cloud_account="demo4501@appuio.ch" \
    environment_strategy=dedicated \
    deployment_strategy=gitops \
    framework=SpringBoot \
    checks=kubernetes \
    tests=junit \
    license=GPL-3 \
    push=force \
    ${*} \
    --no-input

cd /tmp/painless-generated-projects/example-springboot

log 3 'Prepare feature branch'
# TODO: reuse existing code

log 4 'Add an untested feature'
# TODO: reuse existing code

log 5 'Create merge request'
# TODO: as existing code (see Example Django)

log 6 'Allow pipeline to build and push an image'
for minutes in $(seq 13 -1 1); do
    echo "- Waiting... ($minutes' remaining)"
    sleep 1m
done

log 7 'Trigger production release'
git checkout master
git tag 1.0.0
git push --tags --force

#!/bin/bash
#
# NOTE: For the very first deployment please follow
# the steps in the README for the target platform setup.
#
# The periodic regeneration is configured as a scheduled
# pipeline in GitLab > CI/CD > Schedules.
#
set -e

log() {
    NOCOLOR='\033[0m'
    BLUE='\033[1;34m'
    echo -e "$1) ${BLUE}${@:2}${NOCOLOR} ..."
}

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
    project_description="Hello world with Django" \
    project_name="Example Django" \
    container_platform=APPUiO \
    environment_strategy=shared \
    database=Postgres \
    framework=Django \
    vcs_account=appuio \
    license=GPL-3 \
    push=force \
    --no-input

cd /tmp/example-django

log 3 'Prepare feature branch'
git checkout -b feature/welcome-page

git mv -v tests/acceptance/features/{login-logout,welcome-page}.feature
cat > tests/acceptance/features/welcome-page.feature << EOF
Feature: Welcome page
  As a visitor of the website
  I want to be greeted nicely
  So that I know I'm in the right place

  Scenario: Visitor is greeted by simple text
    Given I am on the welcome page
    When I look at the page
    Then I can see the text "Hello APPUiO!"
EOF
sed -E \
    -e "s|pass|context.response = context.test.client.get('/')\n    assert context.response.status_code == 200|" \
    -i tests/acceptance/steps/given.py
sed -E \
    -e "s/^@when\(.*\)/@when(u'I look at the page')/" \
    -e "s|assert True, .*|context.body = str(context.response.content)|" \
    -i tests/acceptance/steps/when.py
sed -E \
    -e "s/^@then\(.*\)/@then(u'I can see the text \"{text}\"')/" \
    -e "s/(step_impl.context)/\1, text/" \
    -e "s/assert True, .*$/assert text in context.body, \\\\\n        \"No '%s' in '%s'.\" % (text, context.body)/" \
    -i tests/acceptance/steps/then.py

git add -v .
git commit -m 'Add tests for welcome page'

mkdir hello
touch hello/__init__.py
cat > hello/views.py << EOF
"""
Landing page app
"""
from django.http import HttpResponse


def index(request):
    """Show a simple welcome page"""
    return HttpResponse('Hello APPUiO!')
EOF
sed -E \
    -e "s/^(from django.urls import include, path)$/\1\n\nfrom hello import views/" \
    -e "s/^(    path.'admin.', admin.site.urls.,)$/\1\n    path('', views.index, name='hello')/" \
    -i application/urls.py

sed -E \
    -e "s/^(commands = pylint --rcfile tox.ini .posargs:application)/\1 hello/" \
    -i tox.ini

git add -v .
git commit -m 'Add friendly welcome page'
git push -u origin feature/welcome-page --force

log 4 'Create merge request'
gitlab POST merge_requests \
    --form "source_branch=feature/welcome-page" \
    --form "target_branch=master" \
    --form "title=Add friendly welcome page" \
    --form "description=A minimal Django application that shows some text. Tests are included." \
    > /dev/null

log 5 'Allow pipeline to build and push an image'
for minutes in $(seq 13 -1 1); do
    echo "- Waiting... ($minutes' remaining)"
    sleep 1m
done

log 6 'Trigger production relase'
git checkout master
git tag 1.0.0
git push --tags --force

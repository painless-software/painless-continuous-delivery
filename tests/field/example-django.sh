#!/bin/sh
#
# NOTE: For the very first deployment please follow
# the steps in the README for the target platform setup.
#
# The periodic regeneration is configured as a scheduled
# pipeline in GitLab > CI/CD > Schedules.
#
set -e

echo '1) Create demo project from scratch and push it ...'
tox -e cookiecutter -- \
    project_description="Hello world with Django" \
    project_name="Example Django" \
    container_platform=APPUiO \
    database=Postgres \
    framework=Django \
    vcs_account=appuio \
    license=GPL-3 \
    push=force \
    --no-input

cd /tmp/example-django

echo '2)a) Prepare feature branch ...'
git checkout -b feature/welcome-page

mkdir hello
touch hello/__init__.py
cat > hello/views.py << EOF
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello APPUiO!')
EOF
sed -E \
    -e "s/^(from django.urls import include, path)$/\1\n\nfrom hello import views/" \
    -e "s/^(    path.'admin.', admin.site.urls.,)$/\1\n    path('', views.index, name='hello')/" \
    -i application/urls.py

git add -v .
git commit -m 'Add friendly welcome page'
git push -u origin feature/welcome-page --force

echo '2)b) Create merge request ...'
curl --request POST --header "Authorization: Bearer $GITLAB_API_TOKEN" \
    https://gitlab.com/api/v4/projects/appuio%2Fexample-django/merge_requests \
    --form "source_branch=feature/welcome-page" \
    --form "target_branch=master" \
    --form "title=Add friendly welcome page"

echo '3) Allow pipeline to build and push an image ...'
for minutes in $(seq 11 -1 1); do
    echo "- Waiting... ($minutes' remaining)"
    sleep 1m
done

echo '4) Trigger production relase ...'
git checkout master
git tag 1.0.0
git push --tags --force
